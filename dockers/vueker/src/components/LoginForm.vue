<template>
    <div class="container-perso">
        <div :class="sx.login" class="h-100 d-flex justify-content-center align-items-center">
          <b-form class="m-3" :class="sx.loginForm" @submit.prevent="handleLogin">
            <img class="mb-4" src="../assets/logo-YT.png" alt="" width="150" height="150">
            <b-form-group>
              <b-form-input v-model="form.login" size="lg" type="text" required placeholder="login" />
            </b-form-group>
            <b-form-group>
              <b-form-input v-model="form.password" size="lg" type="password" required placeholder="password" />
            </b-form-group>
            <b-form-group>
              <b-form-text :class="sx.forgetText">Mot de passe oublié? <a href="#" @click="showModal=true">Click here</a></b-form-text>
            </b-form-group>
            <b-form-group>
              <b-button type="submit" class="btn-principale px-4">Connexion</b-button>
            </b-form-group>
            <div v-if="auth.isConnected">{{ auth.user.firstName }}</div>
          </b-form>

          <b-modal v-model="showModal" centered ok-only hide-header :body-class="sx.popup" :footer-class="sx.popup">
            <p class="text-center m-0 lead">Comming Soon...</p>
            <div slot="modal-footer" class="w-100 text-center">
              <b-button variant="outline-secondary" @click="showModal=false">
                Fermer
              </b-button>
            </div>
          </b-modal>
        </div>
      </div>
</template>

<script>
import axios from 'axios'


export default {
  data () {
    return {
      users: [],
      auth: {
        isConnected: false,
        user: null,
      },
      form: {
        login: "",
        password: ""
      },
			showModal: false
    }
  },
  mounted () {

  },
  methods: {
		handleLogin() {
      const payload = {
        username: this.form.login,
        password: this.form.password
      }
      this.$store.dispatch('login', payload)
        .then(() => {
          this.$bvToast.toast(`Bienvenue`, {
              title: 'Success!',
              solid: true,
              variant: 'info',
              autoHideDelay: 5000
            })
          this.$router.push('/')
        })
        .catch(err => {
          this.$bvToast.toast(`Votre username ou mot de passe est incorrect  `, {
              title: 'Erreur!',
              solid: true,
              variant: 'danger',
              autoHideDelay: 5000
            })
          console.log('err', err)
        })
		}
	}
}
</script>

<style lang="scss" module="sx">
  .login {
    background-image: linear-gradient(to bottom, #293038, #14181d);

    .loginForm {
      width: 350px;
      text-align: center;
    }
   .logo {
      width: 100px;
      height: 100px;
      margin: 0 auto;
      border-radius: 15px;
      margin-bottom: 3rem;
      background-image: linear-gradient(to bottom, #ffa286, #ff6d78);
    }
   .forgetText {
      font-size: 1rem;
      text-align: center;
    }
    .popup {
      border-top: none;
    }
    .modal.fade .modal-dialog {
      opacity: 0;
      transform: translate(0, 0);
    }
    .modal.show .modal-dialog {
      opacity: 1;
    }
  }

</style>
