<script setup lang="ts">
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const serverUrl = 'http://localhost:8000'; // Assuming your backend runs on this URL

onMounted(async () => {
  const token = localStorage.getItem('token');

  if (token) {
    try {
      // Verify token with backend
      await axios.get(`${serverUrl}/users/me/`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      // If successful, token is valid, wait 3 seconds then redirect to home
      setTimeout(() => {
        router.push('/home');
      }, 3000);
    } catch (error) {
      // If token is invalid or expired, remove it, wait 3 seconds then redirect to login
      console.error('Token validation failed:', error);
      localStorage.removeItem('token');
      setTimeout(() => {
        router.push('/login');
      }, 3000);
    }
  } else {
    // No token found, wait 3 seconds then redirect to login
    setTimeout(() => {
      router.push('/login');
    }, 3000);
  }
});
</script>



<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-900 text-white">
    <div class="text-center">
      <img src="@/assets/logo.png" alt="Agentic RAG Logo" class="mx-auto h-48 w-48 animate-pulse" />
      <h1 class="text-5xl font-extrabold mt-8 tracking-wider">CHARTIX</h1>
      <p class="mt-4 text-xl text-gray-400">Loading your personalized experience...</p>
      <div class="mt-12">
        <div class="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-purple-500 mx-auto"></div>
      </div>
    </div>
  </div>
</template>

