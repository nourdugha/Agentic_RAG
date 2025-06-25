import { createRouter, createWebHistory } from 'vue-router'
import UserLoginView from '../views/UserLoginView.vue'
import UserSignupView from '../views/UserSignupView.vue'
import OnboardingView from '../views/OnboardingView.vue'
import HomeView from '../views/HomeView.vue'
import { useAuth } from '@/composables/useAuth';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'onboarding',
      component: OnboardingView
    },
    {
      path: '/login',
      name: 'login',
      component: UserLoginView
    },
    {
      path: '/signup',
      name: 'signup',
      component: UserSignupView
    },
    {
      path: '/home',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const { isAuthenticated } = useAuth();

  if (to.meta.requiresAuth && !isAuthenticated.value) {
    next({ name: 'login' });
  } else if ((to.name === 'login' || to.name === 'signup') && isAuthenticated.value) {
    next({ name: 'home' });
  } else {
    // signal to Vue Router, telling it to simply let the user go where they intended to go.
    next();
  }
});

export default router
