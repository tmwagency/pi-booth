$(document).ready(function(){
$('#takepic').hide();
var key = 0;
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');

    socket.on('event', function(msg) {
	if (msg.data.indexOf("err:") != -1) {
		$('#log').append('<p>ooga</p>');
        	$('#log').append('<p>Received #' + msg.count + ': ' + msg.data + '</p>');
		$('#takepic').show();
	}
	else {
		$('#log').append('<p>Received #' + msg.count + ': ' + msg.data + '</p>');
	}
    });
    $('#usubmit').click(function(event) {
        socket.emit('user', {data: $('#uname_data').val()});
	$('#uname_data').val('');
	event.preventDefault();
	
        return false;
    });
    $('#takepic').click(function() {
	socket.emit('my event', { data: "takepic" });
	return false;
    });
});