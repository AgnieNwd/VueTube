import Vue from 'vue'
import Router from 'vue-router'
import store from '../store'
import HomePage from '@/components/HomePage'
import LoginForm from '@/components/LoginForm'
import RegisterForm from '@/components/RegisterForm'
import UserSettings from '@/components/UserSettings'
import VideoInfos from '@/components/VideoInfos'
import VideosList from '@/components/VideosList'
import VideoForm from '@/components/VideoForm'
import ChaineInfos from '@/components/ChaineInfos'
import AllUsers from '@/components/AllUsers'

Vue.use(Router)

let router = new Router({
  mode: 'history',
  routes: [
    { path: '/', name: 'HomePage', component: HomePage },
    { path: '/login', name: 'LoginForm', component: LoginForm },
    { path: '/register', name: 'RegisterForm', component: RegisterForm },
    { path: '/settings', name: 'UserSettings', component: UserSettings, meta: { requiresAuth: true } },
    { path: '/video/:id', name: 'VideoInfos', component: VideoInfos },
    { path: '/results/:query', name: 'VideosList', component: VideosList },
    { path: '/upload', name: 'VideoForm', component: VideoForm },
    { path: '/chaine/:id', name: 'ChaineInfos', component: ChaineInfos },
    { path: '/users', name: 'AllUsers', component: AllUsers },

    { path: '*', redirect: '/' }
  ]
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (store.getters.isLoggedIn) {
      next()
      return
    }
    next('/login')
  } else {
    next()
  }
})

export default router
