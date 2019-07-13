<template>
  <div class="container-perso">
      <div :class="sx.register" class="h-100 d-flex justify-content-center align-items-center">
        <b-form class="m-3" :class="sx.registerForm" @submit.prevent="register">
          <h1 style="color: white;"> Créer un compte</h1>

          <b-form-group id="input-group-1" label="Username:" label-for="input-1">
            <b-form-input id="name" type="text" size="lg" v-model="username" required placeholder="Username" autofocus />
          </b-form-group>
          <b-form-group id="input-group-1" label="Adresse mail:" label-for="input-1">
            <b-form-input id="email" type="email" size="lg" v-model="email" placeholder="E-mail" required />
          </b-form-group>
          <b-form-group id="input-group-1" label="Pseudo:" label-for="input-1">
            <b-form-input id="pseudo" type="text"  size="lg" v-model="pseudo" placeholder="Pseudo" required />
          </b-form-group>
          <b-form-group id="input-group-1" label="Mot de passe:" label-for="input-1">
            <b-form-input id="password" type="password" size="lg" v-model="password" :state="validation" placeholder="Mot de passe" required />
            <b-form-invalid-feedback :state="validation"> Ton mot de passe doit contenir au moins 8 caractères. </b-form-invalid-feedback>
          </b-form-group>
          <b-button variant="primary" class="btn-principale px-4" type="submit">Inscription</b-button>
        </b-form>
      </div>
    </div>
</template>

<script>
    export default {
      data() {
        return {
          username : "",
          email : "",
          pseudo : "",
          password : "",
        }
      },
      methods: {
        register: function () {
          let payload = {
            username: this.username,
            email: this.email,
            pseudo: this.pseudo,
            password: this.password,
          }
          this.$store.dispatch('register', payload)
            .then(() => this.$router.push('/login'))
            .catch(err => {
               this.$bvToast.toast(`Veuillez réessayer`, {
                title: 'Oops!',
                solid: true,
                variant: 'danger',
                autoHideDelay: 4000
              })
            console.log(err)
          })
        }
      },
      computed: {
        validation() {
          return this.password.length > 7
        }
      }
    }
</script>

<style lang="scss" module="sx">
  .register {

    .registerForm {
      width: 350px;
      text-align: center;
    }
  }

</style>
