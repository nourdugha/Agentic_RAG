<script setup lang="ts">
import Navbar from './components/Navbar.vue';
import { RouterView, useRoute } from 'vue-router'
import { computed } from 'vue';

const route = useRoute();
const showNavbar = computed(() => route.name !== 'onboarding');

</script>

<template>
      <div class="min-h-screen bg-slate-900 text-white">
     <Navbar v-if="showNavbar"/>
     <main class="bg-slate-900/60 min-h-screen">
      <RouterView/>
    </main>
      </div>
    

</template>


