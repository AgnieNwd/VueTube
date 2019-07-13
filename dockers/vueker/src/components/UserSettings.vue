<template>
  <div class="container-perso">
   <div :class="sx.set">
      <b-card bg-variant="transparent" style="height: 100vh;" no-body>
        <b-tabs pills card vertical nav-wrapper-class="col-2" active-nav-item-class="font-weight-bold">
          <b-tab title="Profile" active @click="isPasswordForm=false">
            <b-card-text>
              <div style="width: 65%; margin: auto;">
                <b-form @submit.prevent="handleSetUser">
                  <b-row class="my-3">
                    <b-col sm="3">
                      <label for="username">Username :</label>
                    </b-col>
                    <b-col sm="9">
                      <b-form-input id="username" type="text" v-model="user['username']" required></b-form-input>
                    </b-col>
                  </b-row>
                   <b-row class="my-3">
                    <b-col sm="3">
                      <label for="email">Addresse mail :</label>
                    </b-col>
                    <b-col sm="9">
                      <b-form-input id="email" type="email" v-model="user['email']" required></b-form-input>
                    </b-col>
                  </b-row>
                   <b-row class="my-3">
                    <b-col sm="3">
                      <label for="pseudo">Pseudo :</label>
                    </b-col>
                    <b-col sm="9">
                      <b-form-input id="pseudo" type="text" v-model="user['pseudo']"></b-form-input>
                    </b-col>
                  </b-row>
                <b-button class="btn-principale px-4" type="submit" style="float: right;">Valider</b-button>
                </b-form>
              </div>
            </b-card-text>

          </b-tab><br>
          <b-tab title="Mot de Passe" @click="isPasswordForm=true">
            <b-card-text>
              <div style="width: 65%; margin: auto;">
                <b-form @submit.prevent="handleSetUser">
                  <b-row class="my-3">
                    <b-col sm="4">
                      <label for="password">Nouveau mot de Passe :</label>
                    </b-col>
                    <b-col sm="8">
                      <b-form-input id="password" type="password" v-model="user['password']" :state="validation" required></b-form-input>
                      <b-form-invalid-feedback :state="validation"> Ton mot de passe doit contenir au moins 8 caractères. </b-form-invalid-feedback>
                    </b-col>
                  </b-row>
                   <b-row class="my-3">
                    <b-col sm="4">
                      <label for="handlePassword">Confirme le nouveau mot de passe :</label>
                    </b-col>
                    <b-col sm="8">
                      <b-form-input id="handlePassword" type="password" v-model="handlePassword" required></b-form-input>
                    </b-col>
                  </b-row>
                <b-button v-if="validation" class="btn-principale px-4" type="submit" style="float: right;">Valider</b-button>
                </b-form>
              </div>
            </b-card-text>
          </b-tab>
        </b-tabs>
        <div :class="sx.delete">
          <span @click="deleteUser()"> Supprimer mon compte</span>
        </div>
      </b-card>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      user: [],

      error: false,
      isPasswordForm: false,
      handlePassword: ''
    }
  },
  mounted () {
    if (this.$store.getters.userInfo) {
      try {
        this.user = JSON.parse(this.$store.getters.userInfo)
      } catch(e) {
        this.user = this.$store.getters.userInfo
      }
    }
  },
  methods: {
    handleSetUser() {
      if (this.isPasswordForm) {
      console.log('handlePassword', this.handlePassword)
      console.log('password', this.user.password)
        if (this.handlePassword !== this.user.password) {
          this.user.password = ''
          this.handlePassword = ''
          this.error = true
          this.$bvToast.toast(`Les mots de passe ne sont pas identiques`, {
            title: 'Oops!',
            solid: true,
            variant: 'danger',
            autoHideDelay: 4000
          })
        }
      } else {
        this.user.password = ''
        this.handlePassword = ''
      }
      let payload = {
        username: this.user.username,
        email: this.user.email,
        pseudo: this.user.pseudo,
        password: this.user.password ? this.user.password : '',
      }
      console.log('payload', payload)
      if (!this.error) {
        this.$http.put('user/' + this.user.id , payload, { headers: {'Authorization': localStorage.getItem('Authorization')} }).then(response => {
          // success toast
          this.$bvToast.toast(`Vos données ont bien été prise en compte`, {
            title: 'Success!',
            solid: true,
            variant: 'success',
            autoHideDelay: 5000
          })
          const user = JSON.stringify(response.data.data);
          localStorage.setItem('user', user)
          this.$router.go(0);
        }, (response) => {
          // error toast
          if(response.status != 403 && response.status != 401 && response.status != 404 ) {
            this.$bvToast.toast(`Un problème est survenu`, {
              title: 'Oops!',
              solid: true,
              variant: 'danger',
              autoHideDelay: 4000
            })
          }
        })
      }
      this.error = false

    },
    handleLogout() {
      this.$store.dispatch('logout')
        .then(() => {
          this.$router.push('/login')
        })
    },
    deleteUser() {
      if (confirm('Voulez-vous vraiment supprimer votre compte, toute vos données seront perdu.')) {
        this.$http.delete('user/' + this.user.id, {headers: {'Authorization': localStorage.getItem('Authorization')}}).then(response => {
          // success toast
          this.handleLogout()
        }, (response) => {
          // error toast
          this.$bvToast.toast(`Veuillez réessayer`, {
            title: 'Oops!',
            solid: true,
            variant: 'danger',
            autoHideDelay: 4000
          })
        })
      }
    }
  },
  computed: {
    validation() {
      if (this.user.password) {
        return this.user.password.length > 7
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss" module="sx">
.set{
  // display: flex;
  margin: auto;
}

.clickable:hover {
  opacity: 0.5;
  filter: alpha(opacity=50);
  cursor: pointer;
}

.video {
  margin: 5px;
}

.delete{
  margin: auto;
  cursor: pointer;
  color: red;
}
</style>
