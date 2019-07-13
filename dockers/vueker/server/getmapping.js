var client = require('./connexion.js');

client.indices.getMapping({
        index: 'videos',
        type: 'video',
        include_type_name: true,
    },
    function (error,response) {
        if (error){
            console.log(error.message);
        }
        else {
            console.log("Mappings:\n",response.videos.mappings.video.properties);
        }
    });