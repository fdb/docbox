media_url = '/media';

youTubeExpressions = Array(
	new RegExp('youtube\.com/watch\\?v=([a-zA-Z0-9\-]+)'),
	new RegExp('youtube\.com/v/([a-zA-Z0-9\-]+)'));
	
function load_audio_and_movies() {
	var images = document.getElementsByTagName('img');
	for (var i=0; i<images.length; i++) {
		var className = images[i].className;
		if (className == 'audio_file') {
			var mediaDiv = document.createElement('div');
			var mp3_url = images[i].title;
			mediaDiv.innerHTML = '' +
				'<object classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" width="150" height="20"' +
				'codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab">' +
				'<param name="movie" value="' + media_url + '/swf/mp3player.swf?showDownload=true&file=' +  mp3_url + '&autoStart=false&repeatPlay=false" />' +
				'<param name="wmode" value="transparent" />' +
				'<embed wmode="transparent" width="150" height="20" src="' + media_url + '/swf/mp3player.swf?showDownload=false&file=' +  mp3_url + '&autoStart=false&repeatPlay=false"' +
				'type="application/x-shockwave-flash" pluginspage="http://www.macromedia.com/go/getflashplayer" />' +
				'</object>';
			images[i].style.display = 'none';
			images[i].parentNode.insertBefore(mediaDiv, images[i]);
		} else if (className == 'movie_file') {
			var mediaDiv = document.createElement('div');
			var mov_url = images[i].title;
			width = images[i].width;
			height = parseInt(images[i].height) + 16;
			mediaDiv.innerHTML = '' +
				'<object classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B"' +
				'width="' + width + '" height="' + height + '"' +
				'codebase="http://www.apple.com/qtactivex/qtplugin.cab#version=6,0,2,0">' +
				'<param name="src" value="' + mov_url + '" />' +
				'<param name="autoplay" value="false" />' +
				'<param name="controller" value="true" />' +
				'<embed src="' + mov_url + '" width="' + width + '" height="' + height + '" ' +
				'pluginspage=http://www.apple.com/quicktime/download/' +
				'align="middle" autoplay="false" bgcolor="black" controller="true" > </embed>' +
				'</object>';
			images[i].style.display = 'none';
			images[i].parentNode.insertBefore(mediaDiv, images[i]);
		} else if (className == 'movie_embedded') {
			var mediaDiv = document.createElement('div');
			var mov_url = images[i].title;
			width = images[i].width;
			height = images[i].height;
			for (var j=0; j<youTubeExpressions.length; j++) {
				matchData = youTubeExpressions[j].exec(mov_url);
				if (matchData != undefined)
					break;
			}
			if (matchData != undefined) {
				movie_id = matchData[1];
				mediaDiv.innerHTML = '' +
					'<object classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" ' +
					'width="' + width + '" height="' + height + '">' + 
					'<param name="movie" value="http://www.youtube.com/v/' + movie_id + '&hl=en" />'+
					'<param name="wmode" value="transparent" />' +
					'<embed src="http://www.youtube.com/v/' + movie_id + '&hl=en" ' +
					'type="application/x-shockwave-flash" wmode="transparent" width="' + width + '" height="' + height + '"></embed>' +
					'</object>';
			}
			images[i].style.display = 'none';
			images[i].parentNode.insertBefore(mediaDiv, images[i]);
		}
	}
}
