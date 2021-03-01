<template>
<div>
  <b-navbar :class="sx.nav" type="dark" toggleable="lg">
    <b-navbar-brand to="/">
      <img src="../assets/logo-YT.png" width="30" height="30" class="d-inline-block align-top" alt="Kitten">
      OurYoutube
    </b-navbar-brand>

    <b-navbar-brand to="/users">
      Rechercher utilisateur
    </b-navbar-brand>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav class="mx-auto">
        <b-nav-form @submit.prevent="handleSearch">
          <b-form-input size="sm" width="100" class="mr-sm-2" placeholder="nom de la vidéo" v-model="query"></b-form-input>
          <b-button size="sm" class="my-2 my-sm-0" type="submit"><font-awesome-icon icon="search"/></b-button>
        </b-nav-form>
      </b-navbar-nav>

      <b-navbar-nav v-if="isLoggedIn">
        <b-nav-item :class="sx.navItem" to="/upload" v-b-popover.hover="'Mettre en ligne une vidéo'"><font-awesome-icon icon="plus-square"/></b-nav-item>
        <b-nav-item-dropdown right>
          <template slot="button-content" :class="sx.navItem">{{user.username}}</template>
          <b-dropdown-item :to="'/chaine/' + user.id"><font-awesome-icon icon="user" style="margin-right:10px;"/>Ma chaine</b-dropdown-item>
          <b-dropdown-item to="/settings"><font-awesome-icon icon="cog" style="margin-right:10px;"/>Paramètre</b-dropdown-item>
          <b-dropdown-item to="/" @click="handleLogout()" ><font-awesome-icon icon="sign-out-alt" style="margin-right:10px;"/>Deconnexion</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>

      <b-navbar-nav v-if="!isLoggedIn">
        <b-nav-item :class="sx.navItem" to="/register" >Inscription</b-nav-item>
        <b-nav-item :class="sx.navItem" to="/login">Connexion</b-nav-item>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</div>
</template>

<script>
// import { isLoggedIn, login, logout } from '../../utils/auth';
export default {
  name: 'app-nav',
  computed : {
    isLoggedIn : function(){ return this.$store.getters.isLoggedIn}
  },
  data () {
    return {
      user: [],
      query: ''
    }
  },

  beforeUpdate () {
    this.getCurrentUser()
  },

  mounted () {
    this.getCurrentUser()
  },

  methods: {
    handleLogout() {
      this.$store.dispatch('logout')
      .then(() => {
        this.$router.push('/login')
      })
    },

    getCurrentUser() {
      if (this.$store.getters.userInfo) {
        try {
          this.user = JSON.parse(this.$store.getters.userInfo)
        } catch(e) {
          this.user = this.$store.getters.userInfo
        }
      }
    },

    handleSearch() {
      console.log('see results', this.query)
      this.$router.push({ name: 'VideosList', params: { query: this.query }})
    }
  },
};
</script>

<style lang="scss" module="sx">
.nav {
  background-color: #3f51b5;

	.navItem a {
		font-size: 1.2rem;
		color: #ffffff;
  }


	//$small-layout-width: map-get($grid-breakpoints, xl);
	// @media (max-width: $small-layout-width) {
	// 	@include setNav(50px);
	// }
}

</style>
