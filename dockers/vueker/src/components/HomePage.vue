<template>
  <div class="container-perso">
    <div v-if="isLoaded" class="container">
      <div :class="sx.list">
        <div v-for="video in videos" :key="video.id">
          <div v-if="video.enabled == 1" :class="sx.video" >
            <router-link :to="'/video/' + video.id">
              <div class="card" style="max-width: 20rem; background-color: transparent" >

              <!-- <b-card
                bg-variant="transparent"
                text-variant="white"
                style="max-width: 20rem;"
                class="mb-2"
                :class="sx.clickable"
              > -->
                <video id="vid" class="card-img-top" style="max-height: 9.5rem;" :src="getVideoUrl(video)" muted stop></video>
              <div class="card-body">
                <b-card-text style="color: white;"> {{ video.name }} </b-card-text>
                <b-card-text class="small" style="color: #bbb;">{{ video.user.username }} <br> {{ video.view }} vues  •  {{ video.created_at | moment}}</b-card-text>
              <!-- </b-card> -->
              </div>
              </div>
            </router-link>
          </div>
        </div>
      </div>
      <div class="pagination">
        <div>
          <b-pagination
            v-model="currentPage"
            :total-rows="totalVideos.length"
            :per-page="perPage"
            aria-controls="my-table"
          ></b-pagination>
        </div>
          <div>
            <b-form-select v-model="perPage" :options="options"></b-form-select>
          </div>
        </div>
    </div>
    <div v-else class="container d-flex justify-content-center mb-3" style="height: 100%">
      <strong style="margin-left: 0">Loading...</strong>
      <b-spinner type="grow" label="Spinning" style="width: 3rem; height: 3rem; margin: auto; color:#3f51b5"></b-spinner>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      isLoaded: false,

      videos: [],
      totalVideos: [],

      body: "",
      currentPage: 1,
      perPage: '25',
      options: [
        { value: '5', text: '5' },
        { value: '25', text: '25' },
        { value: '100', text: '100' },
        { value: '200', text: '200' },
      ]
    }
  },

  mounted () {
    this.getNbPages()
    this.getVideos()
  },

  watch: {
    currentPage: function () {
      // on Change page
      this.getVideos();
    },
    perPage: function () {
      this.getVideos()
    }
  },

  methods: {
    getVideos() {
      this.isLoaded = false

      let payload = {
        page: this.currentPage,
        perPage: this.perPage
      }
      this.$http.get('videos', { params: payload }).then(response => {
        // get data
        this.videos = response.data.data
        this.isLoaded = true
      }, (response) => {
        // error callback
        console.log('erreur', response)
      })
    },

    getVideoUrl(video) {
      console.log('video <<<<<<<<<<<', video)
      const src = video.source.replace('/home/','');
      console.log('src <<<<<<<<<<<', src)

      if (video.source.includes(".")) {
        return require('../../../python/' + src)
      }

      // document.getElementById('vid').addEventListener('loadedmetadata', function() {
      //   this.currentTime = 50;
      // }, false);
    },

    getNbPages() {
      this.isLoaded = false

      this.$http.get('videos').then(response => {
        this.totalVideos = response.data.data
        this.nbPages = Math.ceil(this.totalVideos.length / this.perPage);
      }, (response) => { this.isLoaded = true })
    }
  }
}
</script>

<style scoped lang="scss" module="sx">
.list{
  display: flex;
  flex-wrap: wrap;
  // width: max-content;
  // margin: auto;
}

.clickable:hover {
  opacity: 0.5;
  filter: alpha(opacity=50);
  cursor: pointer;
}

.video {
  margin: 5px;
  width: 267px;
  float: left;
}

</style>
