<template>
  <div id="app" class="dark-theme h-100">
    <div :class="sx.app">
    <app-navbar></app-navbar>
    <router-view></router-view>
    </div>
  </div>
</template>

<script>
import AppNavbar from "./components/Navbar";
import axios from 'axios'

export default {
  components: { AppNavbar },
  mounted () {
    this.updateIndexES()
  },
  methods: {
    updateIndexES() {
      console.log('updateIndexES in App.vue')
      axios.get("http://localhost:5010/update")
        .then(response => {
          console.log('get /update', response);
        })
        .catch(err => {
          console.log(err);
        })
    }
  }
};
</script>

<style lang="scss" module="sx">
// @import "style/main.scss";

  html, body {
    margin : auto;
    height: 100%;
  }

  .app {
    width: 100%;
    height: 100vh;
    position: fixed;
  }
</style>
