tinyMCE.init({
	mode : "textareas",
	theme : "advanced",
    plugins: "safari,mnml",
	content_css : DOCBOX_MEDIA_URL + "/css/default.css", // CHANGE THIS
	editor_selector : "mceEditor",
	theme_advanced_buttons1_add : "mnml",
	theme_advanced_toolbar_location : "top",
	theme_advanced_toolbar_align : "left",
	theme_advanced_statusbar_location : "bottom",
	theme_advanced_resizing : true,
	theme_advanced_styles : "Pink box=pink_box;Pink text=pink_text;Header image=header_image;Big text=big_text;Small text=small_text;Weak link=weak_link;Inline code=inline_code;Grey box=grey_box;",
	setup : function(ed) {
		// Gets executed after DOM to HTML string serialization
		ed.onPostProcess.add(function(ed, o) {
			// State get is set when contents is extracted from editor
			if (o.get) {
				// Replace all strong/b elements with em elements
				o.content = o.content.replace(/<\/pre>\n<pre>/g, '\n');
				o.content = o.content.replace(/&amp;nbsp;/g, ' ');
			}
		});
	}
});
