import os
from docbox.util import quicktime as quicktime_util

class Mob(object):
    """Mobs are Media OBjects linked to various types of objects."""
    def __init__(self, project, file_name, type):
        self.project = project
        self.file_name = file_name
        self.type = type
        
        if self.type == 'mov':
            self.width, self.height = quicktime_util.file_size_for_movie(os.path.join(self.project.file_path, self.file_name))

            if self.width == 0 or self.height == 0: # something probably went wrong in the encoding of the media object
                self.width, self.height = 320, 240
        else:
            self.width = self.height = 0
    
    def get_url(self):
        return "/project/%s/%s" % (self.project.identifier, self.file_name)

    def get_thumb_fname(self):
        if self.type == 'mov':          
            return "thumb-%s.gif" % os.path.splitext(self.file_name)[0]
        elif self.type == 'img':
            return "thumb-%s" % self.file_name        

    def get_thumb_url(self):
        return "/project/%s/%s" % (self.project.identifier, self.get_thumb_fname())
