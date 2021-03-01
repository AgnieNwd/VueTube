<template>
  <div class="container-perso">
    <div :class="sx.header">
       <b-row  class="my-3">
          <b-col style="margin: auto; color: #3f51b5;" sm="2">
          </b-col>
          <b-col sm="10">
            <div style="display: flex;">
              <div :class="sx.logo">
                <div :class="sx.user_logo"><font-awesome-icon icon="user" style="margin:auto;"/></div>
              </div>
              <div style="margin: auto; margin-left: 10px">
                <div :class="sx.title"> {{ user.username }}  <span> {{ user.pseudo }} </span></div>
                <div> A rejoint Youtube le {{ user.created_at | moment}}</div>
              </div>
            </div>
          </b-col>
        </b-row>
    </div>
    <b-card bg-variant="transparent" no-body>
      <b-tabs pills card vertical nav-wrapper-class="col-2" active-nav-item-class="font-weight-bold">
        <b-tab title="Mes vidéos" active>
          <div v-if="isLoaded" :class="sx.list" style="padding-bottom: 100px;">
            <div v-if="videos.length > 0" :class="sx.list" style="padding-bottom: 100px;">
              <div v-for="video in videos" :key="video.id">
                <div v-if="video.enabled == 1 || user.id == currentUser.id" :class="sx.video">
                  <b-card
                    bg-variant="transparent"
                    text-variant="white"
                    img-src="https://picsum.photos/600/300/?image=25"
                    img-top
                    style="max-width: 20rem;"
                    class="mb-2"
                    :class="sx.clickable"
                    @click="seeVideo(video.id)"
                  >
                      <b-card-text style="width: 200px;"> {{ video.name }} </b-card-text>
                      <b-card-text class="small text-white" >{{ video.view }} vues  •  {{ video.created_at | moment}}</b-card-text>
                  </b-card>
                  <div  v-if="user.id == currentUser.id" :class="sx.trash">
                    <span class="deleteVideo" @click="deleteVideo(video.id)"><font-awesome-icon icon="trash-alt"/></span>
                  </div>
                  <div  v-if="user.id == currentUser.id" :class="sx.engine">
                    <span class="updateVideo" @click="showModal=true, selectedItem=video"><font-awesome-icon icon="cog"/></span>
                  </div>
                </div>
              </div>
              <b-modal v-if="selectedItem" v-model="showModal" centered ok-only hide-header :body-class="sx.popup" :footer-class="sx.popup">
                <p class="text-center m-0 lead"> <strong>{{ selectedItem.name }} </strong></p>
                <div slot="modal-footer" class="w-100 text-center">
                  <b-form class="m-3" :class="sx.videoForm" @submit.prevent="submitUpdateVideo(selectedItem)">
                    <b-form-group id="input-group-1" label="Saisir le nouveau de la vidéo :" label-for="input-1">
                      <b-form-input id="name" type="text" size="lg" v-model="newNameVideo" required placeholder="Nouveau nom de la vidéo" autofocus />
                    </b-form-group>
                    <b-form-group label="Mettre en ligne la video : ">
                      <b-form-radio-group id="radio-group-2" v-model="selectedEnable" name="radio-sub-component">
                        <b-form-radio name="radio-inline" value="1">Oui 😎</b-form-radio>
                        <b-form-radio name="radio-inline" value="0">Non pas encore 🤔</b-form-radio>
                      </b-form-radio-group>
                    </b-form-group>
                  <b-button variant="primary" class="btn-principale px-4" type="submit">Valider</b-button>
                  <b-button variant="outline-secondary" @click="showModal=false">
                    Fermer
                  </b-button>
                  </b-form>
                </div>
              </b-modal>
            </div>
            <div v-else>
                Vous n'avez encore aucune vidéeo 😬
            </div>
          </div>
          <div v-else :class="sx.list" class="d-flex justify-content-center mb-3" style="height: 100%">
            <b-spinner type="grow" label="Spinning" style="width: 3rem; height: 3rem; margin: auto; color:#f44336"></b-spinner>
            <strong style="margin-left: 0">Loading...</strong>
          </div>
        </b-tab>
        <b-tab title="Mes commentaires" >
          <b-card-text>Mes commentaires</b-card-text>
        </b-tab>
      </b-tabs>
    </b-card>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      isLoaded: false,

      videos: [],
      comments: [],
      user: [],
      selectedItem: [],
      showModal: false,

      newNameVideo : "",
      selectedEnable: 1,

    }
  },

  mounted () {
    if (this.$store.getters.userInfo) {
      try {
        this.currentUser = JSON.parse(this.$store.getters.userInfo)
      } catch(e) {
        this.currentUser = this.$store.getters.userInfo
      }
    }

    this.getUser()
    this.getVideosByUser()
    this.getComments()
    // this.updateIndexES()
  },

  methods: {
    getVideosByUser() {
      this.isLoaded = false

      this.$http.get('user/' + this.$route.params.id + '/videos').then(response => {
        // get data
        this.videos = response.data.data
        this.isLoaded = true
      }, (response) => {
        // error callback
        console.log('erreur getVideosByUser', response)
      })
    },

    getComments() {
      this.$http.get('video/' + this.$route.params.id + '/comments').then(response => {
        // get data
        this.comments = response.data.data
      }, (response) => {
        // error callback
        console.log('erreur getComments', response)
      })
    },

    getUserById() {
      this.$http.get('user/' + this.$route.params.id).then(response => {
        this.user = response.data.data
      }, (response) => {
        console.log('erreur getUserById', response)
      })
    },

    getUser() {
      if (this.currentUser) {
        if (this.$route.params.id === this.currentUser.id) {
          this.user = this.currentUser
        } else {
          this.getUserById()
        }
      } else {
        this.getUserById()
      }
    },

    seeVideo(videoId) {
      this.$router.push({ name: 'VideoInfos', params: { id: videoId }})
    },

    deleteVideo (id) {
      if (confirm('Voulez-vous vraiment supprimer votre video, Vous ne pourrez plus la récupérer.')) {
        this.$http.delete('video/' + id, {headers: {'Authorization': localStorage.getItem('Authorization')}}).then(response => {
          // success toast
          this.$bvToast.toast(`Video supprimée`, {
            title: 'Succès!',
            solid: true,
            variant: 'success',
            autoHideDelay: 5000
          })
          this.getVideosByUser()
          this.updateIndexES()
        }, (response) => {
          // error toast
          this.$bvToast.toast(`Veuillez réessayer`, {
            title: 'Oops!',
            solid: true,
            variant: 'danger',
            autoHideDelay: 4000
          })
          console.log('erreur deleteVideo', response)
        })
      }
    },

    submitUpdateVideo(video) {
      this.isLoaded = false
      let payload = {
        name: this.newNameVideo,
        enable: this.selectedEnable
      }
      console.log("payload", payload, video)
      this.$http.put('video/' + video.id, payload, {headers: {'Authorization': localStorage.getItem('Authorization')}}).then(response => {
        // success toast
        this.$bvToast.toast(`Changement prit en compte !`, {
          title: 'Succès!',
          solid: true,
          variant: 'success',
          autoHideDelay: 5000
        })
        this.getVideosByUser()
        this.updateIndexES()
      }, (response) => {
        // error toast
        this.$bvToast.toast(`Veuillez réessayer`, {
          title: 'Oops!',
          solid: true,
          variant: 'danger',
          autoHideDelay: 4000
        })
        console.log('erreur submitUpdateVideo', response)
      })
      this.showModal = false;
      this.newNameVideo = "";
    },

    updateIndexES() {
      axios.get("http://localhost:5010/update")
        .then(response => {
          console.log('get /update', response);
        })
        .catch(err => {
          console.log(err);
        })
    },
  }
}
</script>

<style scoped lang="scss" module="sx">
  .logo{
    margin-right: 10px;

    .user_logo{
      background: #3f51b5;
      width:80px;
      height:80px;
      border-radius: 3em;
      display: flex;
    }
  }


  .header{
    margin: auto;
    padding: 35px;

    .title{
      color: white;
      font-size: 1.5rem;
      font-weight: 400;
    }

    .title span{
      color: #bbb;
      font-size: 1rem;
      margin-left: 5px;
      font-weight: 300;
    }
  }


  .list {
    display: flex;
    flex-wrap: wrap;

    .video {
      position: relative;
      margin: 5px;
      width: 267px;
      float: left;
    }
    .clickable:hover {
      opacity: 0.7;
      cursor: pointer;
    }

    .trash {
      position: absolute;
      right: 20px;
      top: 152px;
    }
    .trash:hover {
      cursor: pointer;
      color: #f44336;
    }

    .engine {
      position: absolute;
      right: 20px;
      bottom: 26px;
    }
    .engine:hover {
      cursor: pointer;
      color: #3f51b5;
    }
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

  .notOnline {
    color: red;
  }
</style>
