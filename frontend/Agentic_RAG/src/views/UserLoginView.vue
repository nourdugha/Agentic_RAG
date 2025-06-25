<script setup lang="ts">
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  import axios from 'axios';
  import { useAuth } from '@/composables/useAuth';
  
  const username = ref('');
  const password = ref('');
  const router = useRouter();
  const isLoading = ref(false);
  const { setToken } = useAuth();
  
  async function login() {
    isLoading.value = true;
    try {
      const params = new URLSearchParams();
      params.append('username', username.value)
      params.append('password', password.value)
  
      const response = await axios.post('http://localhost:8000/token', params)
      setToken(response.data.access_token);
      router.push('/home')
      console.log("Login success")

    } catch (error) {
      console.error(error)
    } finally {
      isLoading.value = false;
    }
  }
  </script>
  



<template>
    <div class="container mx-auto p-6 bg-slate-800 rounded-lg shadow-xl mt-10 max-w-md">
      <h2 class="text-3xl font-bold text-center mb-6 text-white">Login</h2>
      <form @submit.prevent="login">
        <div class="mb-4">
          <label for="username" class="block text-sm font-medium text-gray-300 mb-1">Username:</label>
          <input type="text" id="username" v-model="username" class="block w-full px-3 py-2 border border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm bg-slate-700 text-white placeholder-gray-400">
        </div>
        <div class="mb-6">
          <label for="password" class="block text-sm font-medium text-gray-300 mb-1">Password:</label>
          <input type="password" id="password" v-model="password" class="block w-full px-3 py-2 border border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm bg-slate-700 text-white placeholder-gray-400">
        </div>
        <button type="submit" :disabled="isLoading" class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 hover:scale-95
                    duration-300">
          <span v-if="isLoading" class="flex items-center">
            <div class="animate-spin rounded-full h-5 w-5 border-t-4 border-b-4 border-white-500 mr-3"></div>
            Logging in...
          </span>
          <span v-else>Login</span>
        </button>
      </form>
    </div>
  </template>
  
  