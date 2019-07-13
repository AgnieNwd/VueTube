var client = require('./connexion.js');

client.indices.putMapping({
    index: 'videos',
    type: 'video',
    include_type_name: true,
    body: {
        properties: {
            'name': {
                'type': 'text', // type is a required attribute if index is specified
                'index': 'not_analyzed'
            },
        }
    }
},function(err,resp,status){
    if (err) {
        console.log(err);
    }
    else {
        console.log(resp);
    }
});