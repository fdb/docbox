(function() {

    var Mnml = {
    	initInstance : function(inst) {
    		// Insert the link and image div at the top of the page.
    		divTag = document.createElement('div');
    		divTag.innerHTML = Mnml._getLinkDiv(inst) + 
    			Mnml._getImageDiv(inst);
    		bodyTag = document.getElementsByTagName('body')[0];
    		bodyTag.insertBefore(divTag, bodyTag.firstChild);
    	},
    	_getLinkDiv : function(inst) {
    		var editor_id = inst.editorId;
    		var html = '';
    		html += '<div id="' + editor_id + '_link_div" class="_ml_link_div" style="background:#ccc;position:absolute;display:none;top:0;left:0;width:500px">';
    		html += '<a href="#" class="lbCloseButton" onclick="tinyMCE.execInstanceCommand(\'' + editor_id + '\', \'mlLinkCancel\');"><img src="' + DOCBOX_MEDIA_URL + '/js/tiny_mce/plugins/mnml/img/close.gif" alt="Close" /></a>';
    		html += '<div id="' + editor_id + '_link_pages"></div>';
    		html += '</div>';		
    		return html;
    	},
    	_getImageDiv : function(inst) {
    		var editor_id = inst.editorId;
    		var html = '';
    		html += '<div id="' + editor_id + '_image_div" class="_ml_img_div" style="background:#ccc;position:absolute;display:none;top:0;left:0;width:500px">';
    		html += '<a href="#" class="lbCloseButton" onclick="tinyMCE.execInstanceCommand(\'' + editor_id + '\', \'mlImageCancel\');"><img src="' + DOCBOX_MEDIA_URL + '/js/tiny_mce/plugins/mnml/img/close.gif" alt="Close" /></a>';
    		html += '<div id="' + editor_id + '_image_inner"></div>';
    		html += '</div>';
    		return html;
    	},
    };

	// Load plugin specific language pack
	tinymce.PluginManager.requireLangPack('mnml');

	tinymce.create('tinymce.plugins.MNMLPlugin', {
		init : function(ed, url) {
			// Register the command so that it can be invoked by using tinyMCE.activeEditor.execCommand('mceMNML');
            Mnml.initInstance(ed);
		    var editor_id = ed.editorId;
			ed.addCommand('mlImage', function() {
				var image_div = document.getElementById(editor_id + '_image_div');
				var project_id = _mlGetProjectIdentifier();
				var img_url = '/mnml/mobs/' + project_id + '/?editor_id=' + editor_id;
				new Ajax.Updater(editor_id + "_image_inner", img_url, {asynchronous:true, method:'get'});
				lbShow(image_div);
			});
			
			ed.addCommand('mlUploadDone', function() {
			   ed.execCommand('mlImage'); 
			});

			ed.addCommand('mlImageCancel', function() {
    		    var editor_id = ed.editorId;
				var image_div = document.getElementById(editor_id + '_image_div');
				lbHide(image_div);
			});
			
			ed.addCommand('mlImageCreate', function(value) {
                ed.execCommand('insertimage', false, value);
                ed.execCommand('mlImageCancel');
                return true;
			});

			ed.addCommand('mlDocCreate', function(value) {
				var url_parts = value.split('/');
				var fname = url_parts[url_parts.length-1];
				var doc_html = '<a class="doclink" href="' + value + '"><img src="' + DOCBOX_MEDIA_URL + '/images/doc.gif" alt="Document" width="9" height="11">' + fname + '</a>';
				ed.execCommand('inserthtml', false, doc_html);
				ed.execCommand('mlImageCancel');
				return true;
			});

			ed.addCommand('mlAudioCreate', function(value) {
				var doc_html = '<img class="audio_file" src="' + DOCBOX_MEDIA_URL + '/images/blank.gif" title="' + value + '" />\n';
				ed.execCommand('inserthtml', false, doc_html);
				ed.execCommand('mlImageCancel');
				return true;
			});
			
			ed.addCommand('mlMovieEmbed', function(value) {
    		    var editor_id = ed.editorId;
				var movie_url = document.getElementById('id_' + editor_id + '_movie_url').value;
				if (movie_url.match(/^http:\/\/\S+\.youtube\.com/)) {
					// Standard YouTube format.
					var width = 480;
					var height = 395;
					var full_url = movie_url;
					var html = ''
						+ '<img class="movie_embedded" src="' + DOCBOX_MEDIA_URL + '/images/blank.gif" title="' + full_url + '" '
						+ 'width="' + width + '" height="' + height + '" />\n';
					ed.execCommand('inserthtml', false, html);
    				ed.execCommand('mlImageCancel');
				} else {
					alert('This is not a valid YouTube URL.');
					var el = document.getElementById('id_' + editor_id + '_movie_url');
					el.value = '';
					el.focus();
				}
				return true;
			});
			
			ed.addCommand('mlMovieCreate', function(value) {
				var width = value.width;
				var height = value.height;
				var html = ''
					+ '<img class="movie_file" src="' + DOCBOX_MEDIA_URL + '/images/blank.gif" title="' + value.url + '" '
					+ 'width="' + width + '" height="' + height + '" />\n';
				ed.execCommand('inserthtml', false, html);
				ed.execCommand('mlImageCancel');
				return true;
			});

			// Register mnml button
			ed.addButton('mnml', {
				title : 'mnml.desc',
				cmd : 'mlImage',
				image : url + '/img/image.gif'
			});

			// Add a node change handler, selects the button in the UI when a image is selected
			ed.onNodeChange.add(function(ed, cm, n) {
				cm.setActive('mnml', n.nodeName == 'IMG');
			});
		},

		createControl : function(n, cm) {
			return null;
		},

		getInfo : function() {
			return {
				longname : 'MNML plugin',
				author : 'Stefan Gabriels',
				version : "1.0"
			};
		}
	});

	// Register plugin
	tinymce.PluginManager.add('mnml', tinymce.plugins.MNMLPlugin);
})();

function _mlGetProjectIdentifier() {
	// Split URL like this:
	// ["http:","","localhost:8000","writer","project","projectid","page","pagename", ""]
	var url_parts = document.location.href.split('/');
	// Project identifier is fourth from the right: "projectid" 
	return url_parts[url_parts.length - 4]; 
}

function _ml_tab_switch(new_tab_id) {
    var content_el = document.getElementById("_ml_content_" + new_tab_id);    
    var content_nodes = content_el.parentNode.getElementsByTagName('div');
    for(var i=0;i<content_nodes.length;i++) {
        if (content_nodes[i].className == '_ml_tab_content') {
            content_nodes[i].style.display = 'none';
        }
    }
    content_el.style.display = 'block';

    var tab_el = document.getElementById("_ml_tab_" + new_tab_id);    
    var tab_nodes = tab_el.parentNode.getElementsByTagName('li');
    for(var i=0;i<tab_nodes.length;i++) {
        tab_nodes[i].className = 'none';
    }
    tab_el.className = '_ml_current';
    
}
