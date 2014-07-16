$(document).ready(function(){
	
	//Hold lookups in variables to save extra processing
	var takepic = $('#takepic');
	var usubmit = $('#usubmit');
	var homebutton = $('#home-button');
	var log = $('#log');
	var messaging = $('#messaging');
	var uname = $('#uname_data');
	var instructions = $('#look');
	var imagecontrols = $('#image-controls');
	var photo = $('#photo');
	
	takepic.hide();
	
	    var socket = io.connect('http://' + document.domain + ':' + location.port + '/photo');
	
	    socket.on('event', function(msg) {
			
			if (msg.response == '0') {
				
				log.html('<p>User ' + msg.name + ' does not exist, please try again.</p>');	
				
			}
		
		else if (msg.response == '1') {
			
			messaging.html('<p class=\"welcome\">Hello ' + msg.name + '</p><p class=\"instructions\">Click the button below to snap a photo.</p>');
			log.html('')
			takepic.fadeIn(800);
			homebutton.show();
			usubmit.hide();
			
		}
		
	    });
	    
	    
		socket.on('timeout', function(msg) {
			
			if (msg.data == 'timeout') {
				alert("Timeout.");
			}
		});
	
		socket.on('event', function(event) {	
			console.log(event.type);
		});
	
	    socket.on('image', function(msg) {	
			
			instructions.hide();
			log.hide();
			var anticache = new Date().getTime();

			image_url = msg.data;
				photo.html('<img src=\"' + msg.data + "?" + anticache + '\" />');
			imagecontrols.show();
			homebutton.hide();
		
		});
		
		
	    usubmit.on('click', function(event) {
			
			usubmit.off();
	        socket.emit('user', { data: uname.val() });
			uname.hide();
			usubmit.hide();
			event.preventDefault();
			
	    });
	    
	    
	    takepic.on('click', function(event) {
			
			socket.emit('take_pic', { data: 'takepic' });
			takepic.hide();
			messaging.hide();
			instructions.fadeIn();
			event.preventDefault();
			
	    });
	
	
	    $('#try-button').click(function(event) {
			
			messaging.fadeIn(800);
			takepic.fadeIn(800);
			homebutton.fadeIn(800);
			imagecontrols.hide();
			photo.html('');
			event.preventDefault();
			
	    });
	
	
	    $('#confirm-button').click(function(event) {
			
			socket.emit('send_pic', {data: 'confirm'});
			
			$('#send-off').fadeIn(800);
			homebutton.fadeIn(800);
			imagecontrols.hide();
			photo.html('');
			event.preventDefault();
			
	    });
	
	
	    homebutton.click(function() {
			
			socket.emit('restart', { data: 'restart' });
			window.location.replace("/");
		
	    });
	    
	    
});
	
