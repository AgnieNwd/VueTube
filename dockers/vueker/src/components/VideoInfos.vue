<template>
  <div class="container-perso">
    <div class="container" v-if="isLoaded">
    <!-- <h4>Recommendation</h4> -->
      <div :class="sx.video">
        <div v-if="video.enabled == 1 || user.id == video.user_id">
          <div :class="sx.info_video" style="position: relative;">
            <div :class="sx.frame" class="embed-responsive">
                <!-- <b-embed aspect="16by9" type="iframe" class="embed-responsive-item"     src="https://www.youtube.com/embed/zpOULjyy-n8?rel=0" allowfullscreen ></b-embed> -->
                <b-embed id="id_iframe"  ref="iframeContent"  aspect="16by9" type="iframe" class="embed-responsive-item" :src="urlVideo" allowfullscreen @load="iframeStyles"></b-embed>
            </div>
            <div :class="sx.title" style="display: flex; justify-content: space-between;">
              <div style="position: absolute;top: 0px;right: 0;">
                <b-form-select v-model="selectedFormat" :options="format" @change="generateNewUrl(video)"></b-form-select>
              </div>
              <div>
                <span> {{ video.name }} </span>
                <div :class="sx.sub_title"> {{ video.view }} vues </div>
              </div>
              <div style="display:flex;">
                <div style="text-align: right; margin-right: 10px">
                  <span style="font-size: smaller"> {{ video.user.username }} </span>
                  <div :class="sx.sub_title" style="font-size: small;"> {{ video.created_at | moment}} </div>
                </div>
                <div style="margin:auto;">
                  <div style="background: #3f51b5; width:40px; height:40px; border-radius: 2em;display: flex;"><font-awesome-icon icon="user" style="margin:auto;"/></div>
                </div>
              </div>
            </div>
          </div>
          <hr>
          <div :class="sx.info_comments">
            <div :class="sx.input_create">
              <b-form @submit.prevent="handleCreateComment" v-if="isLoggedIn">
                <b-row  class="my-3">
                  <b-col style="margin: auto; color: #3f51b5;" sm="1">
                    <font-awesome-icon icon="comment-alt" size="2x" />
                  </b-col>
                  <b-col sm="11">
                    <b-form-textarea id="body" type="text" v-model="body" rows="3" max-rows="6" required placeholder="Ajouter un commentaire public "></b-form-textarea>
                  </b-col>
                </b-row>
                <b-button class="btn-principale px-4" type="submit" style="float: right;">Ajouter</b-button>
              </b-form>
            </div>
            <div v-if="comments.length !== 0" :class="sx.list_comments">
              <div :class="sx.comments" v-for="comment in comments" :key="comment.id">
                <div style="margin:auto;">
                  <div style="background: #f44336; width:40px; height:40px; border-radius: 2em;display: flex;"><font-awesome-icon icon="user" style="margin:auto;"/></div>
                </div>
                <div style="margin-left:20px;">
                  <div style="color: white; font-size: 0.9rem; font-weight: 500;"> {{ comment.user.username }} </div>
                  <div style="color: #ffffffe0; font-size: 1rem; font-weight: 400;"> {{ comment.body }} </div>
                </div>
              </div>
            </div>
            <div v-else-if="isLoggedIn" :class="sx.list_comments">
              Soyez le premier à commenter cette vidéo 🙃
            </div>
            <div v-else :class="sx.list_comments">
              Pas de commentaire pour cette vidéo.. 😔 ( Connecte toi pour être le premier à poster un commentaire sous cette vidéo 😉)
            </div>
            <div class="pagination">
              <div>
                <b-pagination
                  v-model="currentPage"
                  change="updateComments()"
                  :total-rows="totalComments.length"
                  :per-page="perPage"
                  aria-controls="my-table"
                ></b-pagination>
              </div>
              <div>
                <b-form-select v-model="perPage" :options="options"></b-form-select>
              </div>
                <!-- vvvvvv  juste pour voir si le endpoint retourne bien les données correspondant à la page  vvvvvv -->
                <!-- <b-table
                  class="table-dark"
                  id="my-table"
                  :items="totalComments"
                  :per-page="perPage"
                  :current-page="currentPage"
                  small
                ></b-table> -->
                <!--  ^^^^^^  juste pour voir si le endpoint retourne bien les données correspondant à la page   ^^^^^^ -->
            </div>
          </div>
          <br/>

        </div>
        <div v-else> Vidéo indisponible.</div>
      </div>
    </div>
    <div v-else class="container d-flex justify-content-center mb-3" style="height: 100%">
      <strong style="margin-left: 0">Loading...</strong>
      <b-spinner type="grow" label="Spinning" style="width: 3rem; height: 3rem; margin: auto; color:#3f51b5"></b-spinner>
    </div>
  </div>
</template>

<script>
import Media from '@dongido/vue-viaudio';

export default {
  data () {
    return {
      isLoaded: false,

      video: [],
      urlVideo: '',
      format: [],
      selectedFormat: 240,
      comments: [],
      totalComments: [],
      user: [],

      body: "",

      currentPage: 1,
      nbPages: 1,
      perPage: '5',
        options: [
          { value: '5', text: '5' },
          { value: '15', text: '15' },
          { value: '50', text: '50' },
          { value: '100', text: '100' },
        ]
    }
  },

  watch: {
    // on Change page
    currentPage: function () {
      this.getComments()
    },
    perPage: function () {
      this.getComments()
    }
  },

  computed : {
    isLoggedIn : function() {return this.$store.getters.isLoggedIn}
  },

  mounted () {
    if (this.$store.getters.userInfo) {
      try {
        this.user = JSON.parse(this.$store.getters.userInfo)
      } catch(e) {
        this.user = this.$store.getters.userInfo
      }
    }
    this.getNbPages()
    this.getVideoById()
    this.getComments()
  },

  methods: {
    // Just a method to append a simple style to video tag in iframe. yea..
    iframeStyles() {
        var iframe = document.getElementById('id_iframe')

        var css = document.createElement('style');
        css.type = 'text/css';

        var styles = 'video {' +
            'width: 100%;' +
        '}';

        css.appendChild(document.createTextNode(styles));

        iframe.contentDocument.head.appendChild(css);
    },

    getVideoById() {
      this.isLoaded = false

      this.$http.get('video/' + this.$route.params.id).then(response => {
        // get data
        this.video = response.data.data
        this.format = Object.keys(this.video.format)
        this.selectedFormat = this.format[this.format.length - 1]
        console.log('format', this.format)
        this.getVideoUrl(this.video)
        this.isLoaded = true
        // console.log(' video', this.video)
      }, (response) => {
        // error callback
        this.isLoaded = true
        console.log('erreur getVideoById()', response)
      })
    },

    getVideoUrl(video) {
      // if (video.source.includes(".")) {
      //   // console.log('../assets/'+ this.selectedFormat + '/' + video.source)
      //   this.urlVideo =  require('../assets/'+ this.selectedFormat + '/' + video.source)
      // } else {
      //   this.urlVideo = require('../assets/240/unevideo.mp4')
      // }

      console.log('video <<<<<<<<<<<', video)
      const src = video.source.replace('/home/','');
      console.log('src <<<<<<<<<<<', src)
      const srcOUTMP4 = src.replace('.mp4','');
      const srcVIDEO = srcOUTMP4.replace('videos/','');
      console.log('src <<<<<<<<<<<', srcVIDEO)

      if (video.source.includes(".")) {
        this.urlVideo = require('../../../python/' + srcOUTMP4 + '/' + srcVIDEO + '_' + this.selectedFormat + 'p.mp4')
        // this.urlVideo = require('../../../python/' + src)
      }
    },

    generateNewUrl(video) {
      var iframe = document.getElementById('id_iframe');
      var innerDoc = iframe.contentDocument || iframe.contentWindow.document
      var video_tag = innerDoc.getElementsByTagName('video')
      video_tag[0].pause();
      this.getVideoUrl(video)
      setTimeout(function(){
        video_tag[0].load();
        video_tag[0].play();
      }, 1000);
    },

    getComments() {
      let payload = {
        page: this.currentPage,
        perPage: this.perPage
      }
      this.$http.get('video/' + this.$route.params.id + '/comments', { params: payload }).then(response => {
        // get data
        this.comments = response.data.data
      }, (response) => {
        // error callback
        console.log('erreur getComments()', response)
      })
    },

    handleCreateComment() {
      let payload = {
        body: this.body
      }
      this.$http.post('video/' + this.video.id + '/comment', payload, { headers: {'Authorization': localStorage.getItem('Authorization')} }).then(response => {
        this.getComments();
        // success toast
        this.$bvToast.toast(`Succès!`, {
          title: 'Votre commentaire a bien été ajouté',
          solid: true,
          variant: 'success',
          autoHideDelay: 5000
        })
        this.body = '';
      }, (response) => {
        // error toast
        if(response.status != 403 && response.status != 401 && response.status != 404 ) {
          this.$bvToast.toast(`Veuillez réessayer`, {
            title: 'Oops!',
            solid: true,
            variant: 'danger',
            autoHideDelay: 4000
          })
        }
        console.log('erreur createComment()', response)

      })
    },

    getNbPages() {
      this.$http.get('video/' + this.$route.params.id + '/comments').then(response => {
        this.totalComments = response.data.data
        this.nbPages = Math.ceil(this.totalComments.length / this.perPage);
      }, (response) => { })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss" module="sx">
  .video{
    width: 80%;
    display: flex;
    margin: 25px 0;

    .info_video .frame {
      width: 1000px;
      height: auto;
    }
    .title{
      padding: 20px 0;

      span{
        color: white;
        font-size: larger;
      }

      .sub_title{
        font-size: smaller;
      }
    }
  }

  .info_comments{

    .list_comments{
      margin: 85px 0;
    }

    .comments{
      display: flex;
      margin-top: 20px;
      width: max-content;
    }
  }

</style>
