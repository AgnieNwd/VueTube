var client = require('./connexion.js');

client.indices.delete({index: 'videos'},function(err,resp,status) {
    console.log("delete",resp);
});
