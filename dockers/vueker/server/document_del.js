var client = require('./connexion.js');

client.delete({
    index: 'videos',
    id: '1',
    type: 'video'
},function(err,resp,status) {
    console.log(resp);
});