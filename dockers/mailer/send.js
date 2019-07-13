var express = require('express');
var jwt = require('jsonwebtoken')
var bodyParser = require('body-parser');

var app = express();

app.use(function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header('Access-Control-Allow-Methods', 'PUT, GET, POST, DELETE, OPTIONS');
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Authorization");
    next();
});
app.use(bodyParser.json());

const MailDev = require('maildev')
const nodemailer = require('nodemailer')
const maildev = new MailDev({
    smtp: 1025 // incoming SMTP port - default is 1025
})
const transport = nodemailer.createTransport({
    port: 1025,
    ignoreTLS: true,
    // other settings...
});

maildev.listen(function(err) {
    console.log('We can now sent emails to port 1025!')
})

function send_mail(type, email)
{
    subject = ""
    body = ""
    switch(type){
        case 'password':
            subject = "Modification mot de passe"
            body = "Votre mot de passe a bien été changé"
            break;
        case 'encoding':
            subject = "encoding video"
            body = "Encoding effectué"
            break;
    }

    var mail = {
        from: "no-reply@yt.com",
        to: email,
        subject: subject,
        html: body
    }
    transport.sendMail(mail, function(error, response){
        if(error){
            console.log("Erreur lors de l'envoie du mail!");
            console.log(error);
        }else{
            console.log("Mail envoyé avec succès!")
        }
        transport.close();
    });
}

function verifyToken(req, res, next) {
    const bearerHeaders = req.headers['authorization'];
    console.log('bearerHeaders>>', bearerHeaders)

    if (typeof bearerHeaders !== undefined) {
        const bearerToken = bearerHeaders.split(' ')[1];
        req.token = bearerToken
        next();
    } else {
        console.log('verifyToken flaseeee >>>>>>>>>>>>>>>>>', bearerHeaders)
        res.sendStatus(403);

    }
}

app.get('/send', verifyToken , function(req, res, next) {

    // jwt = jwt.replace('Bearer ','');
    // var base64Url = jwt.split('.')[1];
    // var decodedValue = JSON.parse(window.atob(base64Url));
    console.log('jwt tokeeeeeeeeen >>', req.token)
    let data = req['body'];
    let type = data.type;
    let email = data.email;
    
    send_mail(type, email);
    
    res.send('ok');

});

app.use(function(req, res) {
    res.sendStatus(404);
});

// Print new emails to the console as they come in
maildev.on('new', function(email){
    console.log('Received new email with subject: %s', email.subject)
})

// Get all emails
maildev.getAllEmail(function(err, emails){
    if (err) return console.log(err)
    console.log('There are %s emails', emails.length)
})

app.listen(5005, '0.0.0.0', function() {
    console.log('Your node.js server is running on PORT: 5005');
});
