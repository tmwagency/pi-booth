$(document).ready(function(){
$('#takepic').hide();
var key = 0;
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');

    socket.on('event', function(msg) {
	if (msg.response == '0') {
        	$('#log').html('<p>User ' + msg.data + 'does not exist.</p><p>Please try again.</p>');
		
	}
	else if (msg.response == '1') {
		$('#log').html('<p>Hello ' + msg.data + '</p>');
		$('#takepic').show();
	}
	
    });
    $('#usubmit').click(function(event) {
        socket.emit('user', {data: $('#uname_data').val()});
	$('#uname_data').val('');
	event.preventDefault();
	$('#takepic').hide();

        return false;
    });
    $('#takepic').click(function() {
	socket.emit('my event', { data: "takepic" });
	return false;
    });
});