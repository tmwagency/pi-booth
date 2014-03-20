$(document).ready(function(){

$('#takepic').hide();

    var key = 0;
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');

    socket.on('event', function(msg) {
	if (msg.response == '0') {
        	$('#log').html('<p>User ' + msg.data + ' does not exist, please try again.</p>');
		
	}
	else if (msg.response == '1') {
		$('#messaging').html('<p class=\"welcome\">Hello ' + msg.name + '</p><p class=\"instructions\">Click the button below to snap a photo.</p>');
		$('#log').html('')
		$('#takepic').fadeIn(800);
		$('#home-button').show();
		$('#user_submit').hide();
	}
	
    });

    socket.on('image', function(msg) {	
	$('#look').hide();
	$('#log').hide();
	var anticache = new Date().getTime();
	console.log('anticache run: ' + anticache);
	image_url = msg.data;
        $('#photo').html('<img src=\"' + msg.data + "?" + anticache + '\" />');
	$('#image-controls').show();
	$('#home-button').hide();
	
	});
    $('#usubmit').click(function(event) {
	
        socket.emit('user', {data: $('#uname_data').val()});
	$('#uname_data').val(''); 
	event.preventDefault();
	
    });
    $('#takepic').click(function(event) {
	socket.emit('take_pic', { data: "takepic" });
	$('#takepic').hide();
	$('#messaging').hide();
	$('#look').fadeIn();
	event.preventDefault();
    });

    $('#try-button').click(function(event) {
	$('#messaging').fadeIn(800);
	$('#takepic').fadeIn(800);
	$('#home-button').fadeIn(800);
	$('#image-controls').hide();
	$('#photo').html('');
	event.preventDefault();
    });

    $('#confirm-button').click(function(event) {
	socket.emit('send_pic', {data: 'confirm'});
	$('#send-off').fadeIn(800);
	$('#home-button').fadeIn(800);
	$('#image-controls').hide();
	$('#photo').html('');
	event.preventDefault();
    });

    $('#home-button').click(function() {
	window.location.replace("/");
	
    });
});