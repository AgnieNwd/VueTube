var client = require('./connexion.js');

client.indices.create({
    index: 'videos'
},function(err,resp,status) {
    if(err) {
        console.log(err);
    }
    else {
        console.log("create",resp);
    }
});