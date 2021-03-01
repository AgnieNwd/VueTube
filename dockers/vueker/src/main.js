// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import VueResource from 'vue-resource'
import VueBootstrap from 'bootstrap-vue'
import Vuex from 'vuex'
import store from './store'
import Axios from 'axios'

import moment from 'moment'

import App from './App'
import router from './router'

import { library } from '@fortawesome/fontawesome-svg-core'
import { faCog, faUser, faSignOutAlt, faTrashAlt, faCommentAlt, faPlusSquare, faSearch } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

import './style/custom.scss'
import './style/main.scss'
// import 'font-awesome/css/font-awesome.css'

Vue.use(VueResource)
Vue.use(VueBootstrap)
Vue.use(Vuex)

// Vue.http.options.root = 'http://jsonplaceholder.typicode.com'
// Vue.http.headers.common['Access-Control-Allow-Origin'] = 'http://127.0.0.1:5000 | *'

// Vue.http.interceptors.push(function (request, next) {
//   request.headers.set('Access-Control-Allow-Origin', '*')
//   request.headers.set('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')
//   next()
// })

Vue.http.options.root = 'http://127.0.0.1:5000'

Vue.http.interceptors.push(function(request, next) {
  next(function(response) {
    // console.log('response', response)
      if(response.status == 401) {
        //this.$store.dispatch('logout')
        //.then(() => {
        //  this.$router.push('/login')
        //})
        this.$bvToast.toast(`Vous devez être connecté pour accéder à cette ressource`, {
          title: 'erreur 401',
          solid: true,
          variant: 'danger',
          autoHideDelay: 4000
        })
      }
    if(response.status == 403) {
      this.$bvToast.toast(`Vous n'avez pas les droits pour accéder à cette ressource`, {
        title: 'erreur 403',
        solid: true,
        variant: 'danger',
        autoHideDelay: 4000
      })
    }
    if(response.status == 404) {
      this.$bvToast.toast(`Le lien ou la page n'existe pas`, {
        title: 'erreur 404',
        solid: true,
        variant: 'danger',
        autoHideDelay: 4000
      })
    }
  })
})


export default Axios.create({
  baseURL: 'http://localhost:5000',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': localStorage.getItem('Authorization')
  }
})

// const token = localStorage.getItem('token')
// if (token) {
//   Vue.prototype.$http.defaults.headers.common['Authorization'] = token
// }

// Include FontAwesome icons
library.add(faCog, faUser, faSignOutAlt, faTrashAlt, faCommentAlt, faPlusSquare, faSearch)
Vue.component('font-awesome-icon', FontAwesomeIcon)

// Filter for date format
Vue.filter('moment', function (value) {
  if (!value) return ''
  moment.locale('fr');
  return moment(value).format('LL')
})

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  Axios,
  components: { App },
  template: '<App/>'
})
