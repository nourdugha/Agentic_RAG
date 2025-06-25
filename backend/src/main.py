from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database import tables
from src.database.db import engine
from src.Auth.auth import router as auth_router
import uvicorn


class App():
    def __init__(self):
        self.app = FastAPI()
        self.configure_cors()
        self.configure_database()
        self.include_routes()
    
    def configure_cors(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def configure_database(self):
        tables.Base.metadata.create_all(bind=engine)
    
    def include_routes(self):
        self.app.include_router(auth_router,tags=["Authentication"])
    
    def get_app(self) -> FastAPI:
        return self.app

obj = App()
app = obj.get_app()

if __name__ == '__main__':
    uvicorn.run("src.main:app",host="127.0.0.1",port=8000, reload=True)
 