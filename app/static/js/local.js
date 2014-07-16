$(document).ready(function(){
	
	//Hold lookups in variables to save extra processing
	var welcome = $('#welcome');
	var socket = io.connect('http://' + document.domain + ':' + location.port + '/local');
	    
	socket.on('event', function(event) {	
		if (event.type == 'client_connect') {
			welcome.show()
		}
	});
	    
});
	
