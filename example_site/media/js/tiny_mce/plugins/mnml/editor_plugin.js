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
    		html += '<a href="#" class="lbCloseButton" onclick="tinyMCE.execInstanceCommand(\'' + editor_id + '\', \'mlLinkCancel\', false);"><img src="/media/js/tiny_mce/plugins/mnml/img/close.gif" alt="Close" /></a>';
    		html += '<div id="' + editor_id + '_link_pages"></div>';
    		html += '</div>';		
    		return html;
    	},
    	_getImageDiv : function(inst) {
    		var editor_id = inst.editorId;
    		var html = '';
    		html += '<div id="' + editor_id + '_image_div" class="_ml_img_div" style="background:#ccc;position:absolute;display:none;top:0;left:0;width:500px">';
    		html += '<a href="#" class="lbCloseButton" onclick="tinyMCE.activeEditor.execCommand(\'mlImageCancel\');"><img src="/media/js/tiny_mce/plugins/mnml/img/close.gif" alt="Close" /></a>';
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
			ed.addCommand('mceMNML', function() {
				var image_div = document.getElementById(editor_id + '_image_div');
				var project_id = _mlGetProjectIdentifier();
				var img_url = '/mnml/mobs/' + project_id + '/?editor_id=' + editor_id;
				new Ajax.Updater(editor_id + "_image_inner", img_url, {asynchronous:true, method:'get'});
				lbShow(image_div);
			});

			ed.addCommand('mlImageCancel', function() {
				var image_div = document.getElementById(editor_id + '_image_div');
				lbHide(image_div);
			});

			// Register mnml button
			ed.addButton('mnml', {
				title : 'mnml.desc',
				cmd : 'mceMNML',
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