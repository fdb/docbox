import os

class Mob(object):
    """Mobs are Media OBjects linked to various types of objects."""
    def __init__(self, project, file_name, type):
        self.project = project
        self.file_name = file_name
        self.type = type
        self.width = 320
        self.height = 240
    
    def get_url(self):
        return "/project/%s/%s" % (self.project.identifier, self.file_name)

    def get_thumb_fname(self):
        if self.type == 'mov':          
            return "thumb-%s.gif" % os.path.splitext(self.file_name)[0]
        elif self.type == 'img':
            return "thumb-%s" % self.file_name        

    def get_thumb_url(self):
        return "/project/%s/%s" % (self.project.identifier, self.get_thumb_fname())
