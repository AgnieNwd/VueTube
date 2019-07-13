var client = require('./connexion.js');

client.search({
    index: 'videos',
    type: 'video',
    body: {
        query: {
          wildcard: { "name": "*now*" }
        },
    }
},function (error, response,status) {
    if (error){
        console.log("search error: "+error)
    }
    else {
        console.log("--- Response ---");
        console.log(response);
        console.log("--- Hits ---");
        response.hits.hits.forEach(function(hit){
            console.log(hit);
        })
    }
});
