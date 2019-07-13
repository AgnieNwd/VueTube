var client = require('./connexion.js');

//client.cluster.health({},function(err,resp,status) {
//    console.log("-- Client Health --",resp);
//});

client.count({index: 'videos',type: 'video'},function(err,resp,status) {
    console.log("videos",resp);
});
