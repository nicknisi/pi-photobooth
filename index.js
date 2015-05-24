/*jshint node:true*/
var express = require('express');
var stylus = require('stylus');
var fs = require('fs');
var app = express();

var photosDir = __dirname + '/photos';

app.set('view engine', 'jade');
app.use('/photos', express.static('photos'));
app.use(stylus.middleware({
	src: __dirname + '/views/stylesheets',
	dest: __dirname + '/public/stylesheets',
	compile: function (str, path) {
		return stylus(str).set('filename', path).set('compress', true);
	}
}));
app.use(express.static('public'));

app.get('/', function (req, res) {
	fs.readdir(photosDir, function (error, photos) {
		if (error) {
			console.error('there was an error', error);
		}

		res.render('index', { title: 'hi', message: '#glissmante Wedding Gallery', photos: photos });
	});
});

app.get('/view/:photo', function (req, res) {
	var photo = req.params.photo;
	// res.sendfile(photo, { root: photosDir });
	res.render('view', { photo: photo });
});

app.get('/random', function (req, res) {
	fs.readdir(photosDir, function (error, photos) {
		if (error) {
			console.error('there was an error', error);
		}

		var photo = photos[Math.floor(Math.random() * photos.length)];

		res.render('view', { photo: photo, refresh: true });
	});
});

var server = app.listen(3000, function () {
	var address = server.address();
	var host = address.address;
	var port = address.port;

	console.log('App listening at http://%s:%s', host, port);
});
