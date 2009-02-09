import Image

def size_for(width, height, maxwidth=None, maxheight=None):
    """Returns a new width and height pair that fall inside of the given maximum width/height.
    Note that if the given width and height are both smaller than maxwidth and maxheight,
    they are simply returned.
    """
    if maxheight is None or (maxwidth is not None and width > maxwidth and width > height):
        scale = float(maxwidth) / width
        return ( int(width * scale), int(height * scale) )
    elif maxwidth is None or (maxheight is not None and height > maxheight and height >= width):
        scale = float(maxheight) / height
        return ( int(width * scale), int(height * scale) )
    else:
        return width, height        

def universal_resize(img, maxwidth, maxheight):
    """Given a target PIL image, returns a resized version up to the maximum width and height.
    Will only scale images down, not enlarge them.
    - img: original image
    - maxwidth: maximum width of the new image
    - maxheight: maximum height of the new image
    """
    width, height = img.size
    new_width, new_height = size_for(width, height, maxwidth, maxheight)
    resized_img = img.resize( (new_width, new_height), Image.ANTIALIAS )
    return resized_img
