var client = require('./connexion.js');
const axios = require('axios');
var bulk = [];
axios({ url: 'http://localhost:5000/videos', method: 'GET' })
    .then(resp => {
        console.log('resppppppp', resp.data.data)
        data = resp.data.data
        data.forEach(video =>{
            bulk.push({index:{
                    _index:"videos",
                    _type:"video",
                    _id: video.id
                }

            })
            bulk.push(video)
        })
        client.bulk({
            index: 'videos',
            type: 'video',
            body: bulk
        })
    })
    .catch(err => {
        console.log('errrrrrrrrr', err)
    })
