const express = require('express');
const app = express();

const elasticsearch = require('elasticsearch');

const cors = require('cors');
const bodyParser = require('body-parser');
const axios = require('axios');

app.set('port', process.env.PORT || 5010 );
// app.use(cors());
app.use(function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header('Access-Control-Allow-Methods', 'PUT, GET, POST, DELETE, OPTIONS');
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, authorization");
    next();
});
app.use(bodyParser.json());

var client = new elasticsearch.Client( {
    hosts: [
        'http://localhost:9200',
    ]
});

client.ping({ requestTimeout: 30000 }, function(error) {
    if (error) {
        console.error('elasticsearch cluster is down!');
    } else {
        console.log('Everything is ok');
    }
});

app.get('/update', function(req, res) {
    client.indices.delete({index: 'videos'},function(err,resp,status) {
        console.log("delete", resp);
        if (resp) {
            client.indices.create({
                index: 'videos'
            }, function(err,resp,status) {
                if (err) {
                    console.log(err);
                }
                else {
                    console.log("create", resp);
                    var bulk = [];
                    axios({ url: 'http://0.0.0.0:5000/videos', method: 'GET' })
                        .then(resp => {
                            console.log('add resppppppp', resp.data.data)
                            data = resp.data.data
                            data.forEach(video => {
                                bulk.push({
                                    index:
                                        {
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

                            res.send(true);
                        })
                        .catch(err => {
                            console.log('errrrrrrrrr', err)
                        })
                }
            });
        }
    });
});

app.get('/search', function (req, res) {
    let body = {
        'size': 100,
        'from': 0,
        'query': {
          'bool': {
            'should': [
              { 'query_string': { 'query': "*"+req.query['q']+"*", 'fields': ['name'] }},
              { 'query_string': { 'query': req.query['q']+"~", 'fields': ['name'] }},
              { 'multi_match': { 'query':  req.query['q'], 'fields': ['name'] }},
            ]
          }
        },
    }

    setTimeout(function() {
        client.search({index:'videos', body:body, type:'video'})
            .then(results => {
                console.log('resuuuuuuuuults /search', results)
                res.send(results.hits.hits);
            })

            .catch(err=>{
                console.log('errrrrrrrrrrr /search', err)
                res.send([]);
            });
    }, 1000);

})

app.listen(app.get('port'), function() {
    console.log('Your node.js server is running on PORT: ',app.get('port'));
});

module.exports = client;
