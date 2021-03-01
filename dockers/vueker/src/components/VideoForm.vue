<template>
  <div class="container-perso" style="position: relative;">
      <div :class="sx.upload" class="h-100 d-flex justify-content-center align-items-center">
        <b-form class="m-3" :class="sx.videoForm" @submit.prevent="submitCreateVideo">
          <h1 style="color: white; text-align: center;"> Mettre en ligne une video</h1>
          <br>
          <b-form-group id="input-group-1" label="Nom de ta vidéo :" label-for="input-1">
            <b-form-input id="name" type="text" size="lg" v-model="name_video" required placeholder="Nom de la vidéo" autofocus />
          </b-form-group>
          <b-form-group id="input-group-1" label="Ta vidéo :" label-for="input-1">
            <div>
              <div class="custom-file b-form-file is-invalid" id="__BVID__24__BV_file_outer_">
                <input type="file" id="file" ref="file" accept="video/*" required="required"  aria-required="true" class="custom-file-input is-invalid" v-on:change="handleFileUpload()">
                <label v-if="this.file" data-browse="Browse" class="custom-file-label" for="__BVID__24"> {{ this.file.name }} </label>
                <label v-else data-browse="Browse" class="custom-file-label" placeholder="Choisi ton fichier à importer..." for="__BVID__24"> Choisi ton fichier à importer... </label>
              </div>
            </div>
          </b-form-group>
          <b-button variant="primary" class="btn-principale px-4" type="submit">Ajouter!</b-button>
        </b-form>
        <div v-if="!isLoaded" style="position: absolute; top: 30px; position: absolute; right: 30px;">
          <b-spinner type="grow" label="Spinning" style="width: 3rem; height: 3rem; margin: auto; color:#f44336"></b-spinner>
        </div>
      </div>
    </div>
</template>

<script>
import axios from 'axios'

    export default {
      data() {
        return {
          user: [],
          isLoaded: true,

          name_video : "",
          file: null,
        }
      },

      mounted () {
        this.getCurrentUser()
      },

      methods: {
        getCurrentUser() {
          if (this.$store.getters.userInfo) {
            try {
              this.user = JSON.parse(this.$store.getters.userInfo)
            } catch(e) {
              this.user = this.$store.getters.userInfo
            }
          }
          console.log('user ', this.user)
        },

        formatNames(files) {
          if (files.length === 1) {
            return files[0].name
          } else {
            return `${files.length} files selected`
          }
        },

        handleFileUpload(file) {
          this.file = this.$refs.file.files[0];
        },

        submitCreateVideo() {
          this.isLoaded = false

          let formData = new FormData();
          formData.append('source', this.file);
          formData.append('name', this.name_video);

          axios.post('http://localhost:5000/user/' + this.user.id + '/video', formData, { headers: {'Authorization': localStorage.getItem('Authorization'), 'Content-Type': 'multipart/form-data'} }).then(response => {
            // success toast
            this.$bvToast.toast(`Succès!`, {
              title: 'Votre video a bien été ajoutée',
              solid: true,
              variant: 'success',
              autoHideDelay: 5000
            })
            this.name_video = ''
            this.file = null
            this.isLoaded = true

            this.updateIndexES()
          }, (response) => {
            // error toast
            this.$bvToast.toast(`Veuillez réessayer`, {
              title: 'Oops!',
              solid: true,
              variant: 'danger',
              autoHideDelay: 4000
            })
          })
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
      },

      computed: {

      }
    }
</script>

<style lang="scss" module="sx">
  .upload {

    .videoForm {
      width: 550px;
      // text-align: center;
    }
  }

</style>
