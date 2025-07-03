from langchain_community.document_loaders import PyPDFLoader,TextLoader,DirectoryLoader,WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma.vectorstores import Chroma
import pandas as pd
import os
import re



class KnowledgeBasePipeline:
    def __init__(self):
        self.documents = []
        self.chunks = []
        self.embeddings = OllamaEmbeddings(model="codellama")
        self.vectorstore = None # Vectorstore will be initialized dynamically

    def _get_sanitized_collection_name(self, file_path_or_url: str) -> str:
        # Generate a collection name based on the file path or URL
        # Replace non-alphanumeric characters with underscores, and limit length
        base_name = os.path.basename(file_path_or_url).split('.')[0] if not os.path.isdir(file_path_or_url) else os.path.basename(file_path_or_url)
        sanitized_name = re.sub(r'[^a-zA-Z0-9_]', '_', base_name)
        # Chroma collection names must start and end with a letter or number, and be between 3 and 63 characters
        collection_name = f"kb_{sanitized_name}"
        return collection_name[:63] # Ensure it's within Chroma's length limits

    def document_loader(self,file_path_or_url:str, file_type: str = None):
        if os.path.isdir(file_path_or_url):
            if file_type == "pdf":
                loader = DirectoryLoader(file_path_or_url, glob="**/*.pdf", loader_cls=PyPDFLoader)
            elif file_type == "txt":
                loader = DirectoryLoader(file_path_or_url, glob="**/*.txt", loader_cls=TextLoader, loader_kwargs={'encoding': 'utf-8'})
            else:
                raise ValueError("For directory loading, 'file_type' must be specified as 'pdf' or 'txt'.")
            loader_result = loader.load()

        else:
            file_extension = file_path_or_url.split(".")[-1].lower()
            if file_extension == "pdf":
                loader = PyPDFLoader(file_path_or_url, extract_images=True)
            elif file_extension == "txt":
                loader = TextLoader(file_path_or_url, encoding="utf-8")
            elif file_extension.startswith("http"): # Assuming web links start with http
                loader = WebBaseLoader(file_path_or_url)
            else:
                raise ValueError(f"Unsupported file type or invalid path: {file_path_or_url}")
            loader_result = loader.load()

        self.documents = loader_result
        return self.documents
    

    def document_splitter(self,documents:list[Document]):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 150,
            chunk_overlap = 20,
            length_function = len,
            is_separator_regex = False,
        )
        self.chunks = text_splitter.split_documents(documents)
        return self.chunks
    
    def document_embedder(self,chunks:list[Document]):
        if not self.vectorstore:
            raise ValueError("Vectorstore not initialized. Call process_document_intelligently first.")
        self.vectorstore.add_documents(chunks)

    def process_document_intelligently(self, file_path_or_url: str, file_type: str = None):
        collection_name = self._get_sanitized_collection_name(file_path_or_url)
        print(f"Attempting to process with collection name: {collection_name}")

        # Initialize vectorstore for this specific collection
        self.vectorstore = Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings,
            persist_directory="./chroma_langchain_db"
        )

        # Check if the collection already contains data for this document
        existing_ids = self.vectorstore.get()["ids"]
        if existing_ids:
            print(f"File '{file_path_or_url}' has already been processed and embedded in collection '{collection_name}'. Skipping.")
        else:
            print(f"Processing new file: {file_path_or_url} into collection '{collection_name}'.")
            documents = self.document_loader(file_path_or_url, file_type)
            print("Documents loaded successfully.")
            chunks = self.document_splitter(documents)
            print(f"Number of chunks created: {len(chunks)}")
            self.document_embedder(chunks)
            print("Chunks embedded and added to vector store successfully.")

    def reset_vectorstore_collection(self):
        # This method now needs to know which collection to reset, or clear all.
        # For now, let's keep it as is, but note it will only re-initialize the *current* vectorstore instance.
        # If you want to delete a specific collection, you'd need the collection name here.
        print("Resetting current Chroma collection instance...")
        self.vectorstore = Chroma(
            collection_name=self.vectorstore.collection_name if self.vectorstore else "example_collection", # Use current name or default
            embedding_function=self.embeddings,
            persist_directory="./chroma_langchain_db"
        )
        print("Current Chroma collection instance reset.")

    def get_vectorstore_data_as_dataframe(self):
        if not self.vectorstore:
            print("Vectorstore not initialized. No data to display.")
            return pd.DataFrame() # Return empty DataFrame

        # Retrieve all data from the vectorstore
        # We need to specify `include` to get all the data (documents, embeddings, metadata, and IDs)
        all_data = self.vectorstore.get(
            ids=self.vectorstore.get()["ids"], # Get all IDs to retrieve all data
            include=["documents", "embeddings", "metadatas"]
        )

        if not all_data["documents"]:
            print(f"No documents found in collection '{self.vectorstore.collection_name}'.")
            return pd.DataFrame() # Return empty DataFrame

        # Prepare data for DataFrame
        data_for_df = []
        for i in range(len(all_data["documents"])):
            chunk_content = all_data["documents"][i]
            embedding = all_data["embeddings"][i]
            metadata = all_data["metadatas"][i]
            data_for_df.append({
                "chunk_text": chunk_content,
                "embedding": embedding,
                "metadata": metadata
            })
        
        # Create DataFrame
        df = pd.DataFrame(data_for_df)
        return df


if __name__ == "__main__":
    pipeline = KnowledgeBasePipeline()

    file_path_pdf = os.path.join(os.path.dirname(__file__), "2408.15777v1.pdf")
    file_path_txt = os.path.join(os.path.dirname(__file__), "test_text.txt")

    # Process the text file intelligently
    print("\n--- Processing test_text.txt ---")
    pipeline.process_document_intelligently(file_path_txt)
    
    # Process the PDF file intelligently (uncomment to test with PDF)
    # print("\n--- Processing 2408.15777v1.pdf ---")
    # pipeline.process_document_intelligently(file_path_pdf)

    # New: Get and print vectorstore data as DataFrame for the *last processed* collection
    print("\n--- Vector Store Data as DataFrame for the last processed file ---")
    df_vectorstore = pipeline.get_vectorstore_data_as_dataframe()
    if not df_vectorstore.empty:
        print(df_vectorstore.to_string()) # Use to_string() to print full DataFrame without truncation

    # Example of how to reset a specific collection (if you know its name)
    # If you want to truly clear the disk, you might need to manually delete the 'chroma_langchain_db' folder
    # For instance, if you wanted to reset the 'kb_test_text' collection:
    # temp_pipeline = KnowledgeBasePipeline()
    # temp_pipeline.vectorstore = Chroma(collection_name="kb_test_text", embedding_function=pipeline.embeddings, persist_directory="./chroma_langchain_db")
    # temp_pipeline.vectorstore.delete_collection()

    # This part of the code is largely for demonstration and might need more robust error handling
    # in a production environment.

