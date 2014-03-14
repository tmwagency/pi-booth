$(document).ready(function(){
var key = 0;
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    socket.on('event', function(msg) {
	
	var myindex = parseInt(msg.count);
	console.log(myindex);
        $('#log').append('<p>Received #' + msg.count + ': ' + msg.data + '</p>');
	
	$('.column:eq('+myindex+')').find('.key').addClass('active');
    });
    $('form#emit').submit(function(event) {
        socket.emit('my event', {data: $('#emit_data').val()});
        return false;
    });
    $('form#broadcast').submit(function(event) {
        socket.emit('my broadcast event', {data: $('#broadcast_data').val()});
        return false;
    });
});