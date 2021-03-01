<template>
  <div class="container-perso">
    <div class="container" v-if="isLoaded">
      <div :class="sx.list" v-if="videos.length > 0">
        <div v-for="video in videos" :key="video.id">
          <div v-if="video._source.enabled == 1" :class="sx.video" >
            <router-link :to="'/video/' + video._source.id">
              <b-card
                bg-variant="transparent"
                text-variant="white"
                img-src="https://picsum.photos/600/300/?image=25"
                img-top
                style="max-width: 20rem;"
                class="mb-2"
                :class="sx.clickable"
              >
                <b-card-text style="color: white;"> {{ video._source.name }} </b-card-text>
                <b-card-text class="small" style="color: #bbb;"> {{ video._source.user.username }}<br>{{ video._source.view }} vues  •  {{ video._source.created_at | moment}}</b-card-text>
              </b-card>
            </router-link>
          </div>
        </div>
      </div>
      <div v-else>
        <span> Il semble que rien ne correspond à votre recherche 🤷‍</span>
      </div>
    </div>
    <div v-else class="container d-flex justify-content-center mb-3" style="height: 100%">
      <strong style="margin-left: 0">Loading...</strong>
      <b-spinner type="grow" label="Spinning" style="width: 3rem; height: 3rem; margin: auto; color:#3f51b5"></b-spinner>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      isLoaded: false,
      query: '',
      videos: [],

    }
  },

  mounted () {
    // console.log('parammmmmmmmmmmm ', this.$route.params.query)
    this.query = this.$route.params.query;
    this.getVideos()
  },

  watch: {
    '$route' (to, from) {
      this.query = this.$route.params.query;
      this.getVideos()
    }
  },

  methods: {
    getVideos() {
      this.isLoaded = false

      axios.get("http://localhost:5010/search?q=" + this.query)
      .then(response => {
        this.videos = response.data
        this.isLoaded = true
      })
      .catch(err => {
        console.log("getVideos err", err);
        this.isLoaded = true

      })

    },

  }
}
</script>
<style>
video {
  width: 100%!important;
}
</style>

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
