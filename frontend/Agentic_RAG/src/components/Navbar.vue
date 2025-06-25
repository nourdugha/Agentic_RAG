<script setup lang="ts">
import logo from '@/assets/logo.png'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { computed } from 'vue'
import { useAuth } from '@/composables/useAuth';

const route = useRoute()
const router = useRouter()
const { isAuthenticated, setToken } = useAuth();

const isActiveLink = (routePath: string) => {
  return route.path === routePath
}

const logout = () => {
  setToken(null);
  router.push('/login')
}
</script>

<template>
  <nav class=" bg-gray-900 border-b-2 border-gray-800 shadow-lg shadow-cyan-500/50">
    <div class="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
      <div class="flex h-17 items-center justify-between">
        <div class="flex flex-1 items-center justify-center md:items-stretch md:justify-start">
          <!-- Logo -->
          <RouterLink class="flex flex-shrink-0 items-center mr-4" to="/">
            <img class="h-15 w-auto" :src="logo" alt="Chatrix" />
            <span class="hidden md:block text-white text-2xl font-bold ml-2">CHARTIX</span>
          </RouterLink>
          <div class="md:ml-auto">
            <div class="flex space-x-2">
              <template v-if="!isAuthenticated">
                <RouterLink
                  to="/signup"
                  :class="[
                    'hover:text-gray-200',
                    isActiveLink('/signup') ? 'text-white scale-130' : 'text-white',
                    'font-bold',
                    'px-3',
                    'py-3',
                    'rounded-2xl',
                    'hover:scale-130',
                    'duration-300',
                  ]"
                  >SignUp</RouterLink
                >
                <RouterLink
                  to="/login"
                  :class="[
                    'hover:text-gray-200',
                    isActiveLink('/login') ? 'text-white scale-130' : 'text-white',
                    'font-bold',
                    'px-3',
                    'py-3',
                    'rounded-2xl',
                    'hover:scale-130',
                    'duration-300',
                  ]"
                  >LogIn</RouterLink
                >
              </template>
              <template v-else>
                <RouterLink
                  to="/login"
                  @click.prevent="logout"
                  :class="[
                    'hover:text-gray-200',
                    'text-white',
                    'font-bold',
                    'px-3',
                    'py-3',
                    'rounded-2xl',
                    'hover:scale-130',
                    'duration-300',
                  ]"
                >
                  Logout
                </RouterLink>
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>
