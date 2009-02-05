"""File name cleaning and file renaming operations"""

import os
import string
import random

ALLOWED_CHARS = string.lowercase + string.digits + "- "

def squeeze(s, filter="- "):
    """Removes double appearance of one of the given characters.
    
    e.g. "a-------b" -> "a-b" """
    out = ""
    last_char = None
    for c in s:
        if c not in filter or c != last_char:
            out += c
            last_char = c
    return out

def strip_dashes(s):
    return s.strip("-")

def filter_allowed_chars(s):
    """Return a string that contains only characters from ALLOWED_CHARS."""
    out = ""
    for c in s:
        if c in ALLOWED_CHARS:
            out += c
    return out

def replace_spaces_with_dashes(s):
    return s.replace(" ", "-")
    
def assure_filename(s):
    """Assure there is still a filename left."""
    if len(s) > 0:
        return s
    else:
        return str(random.randint(1000, 9999))

def truncate(s, maxlength=32):
    """Truncate the given string if it is too long.
    
    This function cuts out the middle part."""
    if len(s) <= maxlength:
        return s
    else:
        begin = maxlength / 2
        end = begin - maxlength
        return s[:begin] + s[end:]
                
def clean_filename(fname):
    """Clean the filename.
    
    This will always return a clean filename of at least 1 character,
    but the extension might be missing (if none is given)."""
    
    fname = fname.lower()
    base, ext = os.path.splitext(fname)
    base = filter_allowed_chars(base)
    base = replace_spaces_with_dashes(base)
    base = strip_dashes(base)
    base = squeeze(base)
    base = assure_filename(base)
    base = truncate(base)

    if len(ext) > 0:        
        return "%s%s" % (base, ext)
    else:
        return base
        
def clean_rename(fname):
    clean_fname = clean_filename(fname)
    os.rename(fname, clean_fname)
    return clean_fname    

