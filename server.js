'use strict';

const express = require("express");
const path = require("path");

var http = require('http');
var port = process.env.PORT || 1337;

const app=express();

const siteData = {
    title: "googlepopchecker"
}

express().use(require('express-ejs-layouts'));

//http.createServer(function (req, res) {
//    res.writeHead(200, { 'Content-Type': 'text/plain' });
//    res.end('Hello World\n');
//}).listen(port);

//Static pages
app.use(express.static(path.join(__dirname, 'public')));

//View template set
app.set('views', path.join(__dirname, 'views')) // View file path
    .set('view engine', 'ejs')                  // View engine
    .use(require('express-ejs-layouts'))        // Layout package
    .set('layout', 'layouts/layout');           // Layout path

app.listen(port, ()=>console.log('Listening on http://localhost:${port}'));

//Route Rendering
// Index
app.get('/', (req, res) => {app.locals.styleNo = 0; res.render('pages/index', {title:"Home | " + siteData.title})});

