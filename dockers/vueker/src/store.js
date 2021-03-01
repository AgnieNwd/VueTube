import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    status: '',
    token: localStorage.getItem('Authorization') || '',
    user: localStorage.getItem('user') || {}
  },
  mutations: {
    auth_request (state) {
      state.status = 'loading'
    },
    auth_success (state, payload) {
      state.status = 'success'
      state.token = payload.token
      state.user = payload.user
      console.log('state.user', state.user)
    },
    auth_error (state) {
      state.status = 'error'
    },
    logout (state) {
      state.status = ''
      state.token = ''
    }
  },
  actions: {
    login ({commit}, user) {
      return new Promise((resolve, reject) => {
        commit('auth_request')
        axios({ url: 'http://localhost:5000/auth', data: user, method: 'POST' })
          .then(resp => {
            const token = resp.data.data.token
            const user = resp.data.data.user
            // let date = new Date()
            // console.log('date now',  new Date().getTime())
            // const expiToken = Date.now() + (4*60*60*1000)
            // console.log('expiToken',  new Date())
            localStorage.setItem('Authorization', token)
            let parsedUser = JSON.stringify(user);
            localStorage.setItem('user', parsedUser)
            axios.defaults.headers.common['Authorization'] = token
            commit('auth_success', resp.data.data)
            resolve(resp)
          })
          .catch(err => {
            commit('auth_error')
            localStorage.removeItem('Authorization')
            localStorage.removeItem('user')
            reject(err)
          })
      })
    },
    register ({commit}, user) {
      return new Promise((resolve, reject) => {
        commit('auth_request')
        console.log('register user', user)
        axios({ url: 'http://localhost:5000/user', data: user, method: 'POST' })
          .then(resp => {
            // const user = resp.data.data.user
            resolve(resp)
          })
          .catch(err => {
            commit('auth_error', err)
            localStorage.removeItem('Authorization')
            localStorage.removeItem('user')
            reject(err)
          })
      })
    },
    logout ({commit}) {
      return new Promise((resolve, reject) => {
        commit('logout')
        localStorage.removeItem('Authorization')
        localStorage.removeItem('user')
        delete axios.defaults.headers.common['Authorization']
        resolve()
      })
    }
  },
  getters: {
    isLoggedIn: state => !!state.token,
    authStatus: state => state.status,
    userToken: state => state.token,
    userInfo: state => state.user
  }
})
