$(document).ready(function(){
	//$('.log').append("Logging works");

	//Hold lookups in variables to save extra processing
	var welcome = $('.welcome');
	var socket = io.connect('http://' + document.domain + ':' + location.port + '/local');
	console.log(socket);
	
	
	socket.on('connect', function(socket) {
		console.log("Socket connected");
	});
	
	socket.on('event', function(event) {	
		console.log(event.type);
	});

});
	
