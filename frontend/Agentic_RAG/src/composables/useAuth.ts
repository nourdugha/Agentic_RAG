import { ref, computed } from 'vue';

// Initialize with the current token from localStorage
const authToken = ref(localStorage.getItem('token'));

export function useAuth() {
  const isAuthenticated = computed(() => authToken.value !== null);

  const setToken = (token: string | null) => {
    if (token) {
      localStorage.setItem('token', token);
    } else {
      localStorage.removeItem('token');
    }
    authToken.value = token; // Update the reactive ref
  };

  return {
    isAuthenticated,
    setToken,
  };
} 