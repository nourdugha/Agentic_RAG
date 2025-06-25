<script setup lang="ts">
import {ref} from 'vue' 
import { useRouter } from 'vue-router';
import axios from 'axios'

const username = ref('')
const full_name = ref('')
const email = ref('')
const password = ref('')
const router = useRouter()

async function register(){
    try{
    const response = await axios.post('http://localhost:8000/register', {
        username: username.value,
        full_name:full_name.value,
        email: email.value,
        password: password.value
    }, {
        headers: {
            'Content-Type': 'application/json'
        }
    })
      console.log(response.data)
      router.push('/login')
    }
    catch(error){
        console.error(error)
    }
}
</script>



<template>
    <div class="container mx-auto p-6 bg-slate-800 rounded-lg shadow-xl mt-10 max-w-md">
      <h2 class="text-3xl font-bold text-center mb-6 text-white">Register</h2>
      <form @submit.prevent="register">
        <div class="mb-4">
          <label for="username" class="block text-sm font-medium text-gray-300 mb-1">Username:</label>
          <input type="text" id="username" v-model="username" class="block w-full px-3 py-2 border border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm bg-slate-700 text-white placeholder-gray-400">
        </div>
        <div class="mb-4">
          <label for="full_name" class="block text-sm font-medium text-gray-300 mb-1">Full name:</label>
          <input type="text" id="full_name" v-model="full_name" class="block w-full px-3 py-2 border border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm bg-slate-700 text-white placeholder-gray-400">
        </div>
        <div class="mb-4">
          <label for="email" class="block text-sm font-medium text-gray-300 mb-1">Email:</label>
          <input type="email" id="email" v-model="email" class="block w-full px-3 py-2 border border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm bg-slate-700 text-white placeholder-gray-400">
        </div>
        <div class="mb-6">
          <label for="password" class="block text-sm font-medium text-gray-300 mb-1">Password:</label>
          <input type="password" id="password" v-model="password" class="block w-full px-3 py-2 border border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm bg-slate-700 text-white placeholder-gray-400">
        </div>
        <button type="submit" class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 hover:scale-95
                    duration-300">
          Register
        </button>
      </form>
    </div>
  </template>
  

  