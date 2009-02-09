"""Universal embedding"""

import os
from django import template
from docbox import mnml
register = template.Library()

def embed(mob):
    if not isinstance(mob, Mob):
        raise template.TemplateSyntaxError, "%r tag needs a Mob as argument" % mob

    if mob.type == 'img':
        return embed_image(mob)
    elif mob.type == 'mov':
        return embed_movie(mob)
    elif mob.type == 'aud':
        return embed_audio(mob)
    return "<strong>mob '%s' invalid type '%s'</strong>!" % (mob.file_name, mob.type)
register.simple_tag(embed)
    
def embed_image(mob):
    return """<img src="%s" />""" % mob.get_url()
  
def embed_movie(mob):
    return """<object type="application/x-shockwave-flash" width="%s" height="%s" 
    	wmode="transparent" data="%s/swf/flvplayer.swf?file=%s">
    	<param name="movie" value="%s/swf/flvplayer.swf?file=%s" />
    	<param name="wmode" value="transparent" />
    </object><img src="%s" />""" % (mob.width, mob.height, settings.MEDIA_URL, mob.get_url(), settings.MEDIA_URL, mob.get_url(), mob.get_thumb_url())

def embed_audio(mob):
    return """<object 
    classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" 
    width="160" height="16" 
    codebase="http://www.apple.com/qtactivex/qtplugin.cab">
	<param name="src" value="%s">
	<param name="autoplay" value="false">
	<param name="loop" value="false">
	<param name="controller" value="true">
	<param name="type" value="audio/x-mpeg">
	<param name="pluginspage" value="http://www.apple.com/quicktime/download/indext.html">
	<param name="target" value="myself">
	<embed 
	src="%s" 
    width="160" "
    height="16" 
	target="myself" 
	autoplay="false" 
	loop="false" 
	controller="true" 
	type="audio/x-mpeg" "
	pluginspage="http://www.apple.com/quicktime/download/indext.html"
	></embed>
    </object>""" % (mob.get_url(), mob.get_url())


    return """<img src="%s" />""" % mob.get_url()

def embed_thumb(mob):
    if not isinstance(mob, Mob):
        raise template.TemplateSyntaxError, "%r tag needs a Mob as argument" % token.contents[0]

    if mob.type == 'img':
        return embed_thumb_image(mob)
    elif mob.type == 'mov':
        return embed_thumb_movie(mob)
    elif mob.type == 'aud':
        return embed_thumb_audio(mob)
    elif mob.type == 'doc':
        return embed_thumb_doc(mob)
    return "<strong>mob '%s' invalid type '%s'</strong>!" % (mob.file_name, mob.type)
register.simple_tag(embed_thumb)

def embed_thumb_image(mob):
    return """<img src="%s" />""" % mob.get_thumb_url()

def embed_thumb_audio(mob):
    return """%s""" % mob.file_name
embed_thumb_movie = embed_thumb_audio
    
def embed_thumb_doc(mob):
    return """<img src="%s/js/tiny_mce/themes/mnml/images/doc.gif" alt="Document" width="9" height="11" />&nbsp;%s""" % (settings.MEDIA_URL, mob.file_name)

def embed_audio_preview(fname):
    if fname is None:
        return ""
    fname = os.path.basename(fname)
    preview_folder = settings.MEDIA_ROOT + 'audio/previews/'
    audio_url = "%s/audio/previews/%s" % (settings.MEDIA_URL, fname)
    return """<object classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" width="25" height="20"
    codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab">
    <param name="movie" value="%s/swf/mp3player.swf?showDownload=true&file=%s&autoStart=false&repeatPlay=false" />
    <param name="wmode" value="transparent" />
    <embed wmode="transparent" width="25" height="20" src="%s/swf/mp3player.swf?showDownload=false&file=%s&autoStart=false&repeatPlay=false"
    type="application/x-shockwave-flash" pluginspage="http://www.macromedia.com/go/getflashplayer" />
    </object>""" % (settings.MEDIA_URL, audio_url, settings.MEDIA_URL, audio_url)
register.simple_tag(embed_audio_preview)

def embed_newsletter_image(fname):
    if fname is None:
        return ""
    fname = os.path.basename(fname)
    preview_folder = settings.MEDIA_URL + '/newsletters/'
    return """<img src="%s%s" class="newsletter-image" />""" % (preview_folder, fname)
register.simple_tag(embed_newsletter_image)
