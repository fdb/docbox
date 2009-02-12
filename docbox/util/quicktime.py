"""Module for finding the movie size of a QuickTime movie."""

from struct import unpack, calcsize

class TrackHeader(object):
    def __init__(self, f, pos):
        self.f = f
        self.pos = pos
        self.read()
        
    def read(self):
        f = self.f
        f.seek(self.pos)
        # Unpacking string for the data. "x" means padding, "I" means unsigned int,
        # "i" means signed int, "h" means short.
        # All "I", "i" and "h"'s are converted to variables by unpack.
        # We are interested in the data at the end, which contains the frame size.
        header_string = '>xxxxIIixxxxxxxxixxxxxxxxhxxIIIIIIIIIhhhh'
        bytes = f.read(calcsize(header_string))
        creat_date, lastmod_date, track_id, duration, video_layer, \
            geom_a, geom_b, geom_u, geom_c, geom_d, geom_v, geom_x, geom_y, geom_w, \
            frame_size_width_i, frame_size_width_f, frame_size_height_i, frame_size_height_f = \
            unpack(header_string, bytes)
        self.width, self.height = frame_size_width_i, frame_size_height_i

class Atom(object):

    def __init__(self, f, type=None, pos=0, size=None):
        self.f = f
        self.type = type
        self.pos = pos
        self.size = size
        self.read()

    def read(self):
        f = self.f
        pos = self.pos
        self.atoms = []
        while True:
            if self.size is not None and pos >= self.size:
                return self.atoms
            f.seek(pos)
            size_bytes = f.read(4)
            if len(size_bytes) == 4:
                atom_size = unpack('>i', size_bytes)[0]
                atom_type = f.read(4)
                self.atoms.append( (atom_type, pos, atom_size) )
                pos += atom_size
            else:
                return self.atoms
                
    def find_by_type(self, type):
        return [Atom(self.f, atom[0], atom[1] + 8, atom[2] - 8) for atom in self.atoms if atom[0] == type]
        
    def __repr__(self):
        return "Atom(%s, %s, %s)" % (self.type, self.pos, self.size)

def file_size_for_movie(f):
    """Given a file name or file object, returns the movie width and height.
    If no size can be found, returns (0,0).
    If multiple tracks with multiple sizes are found, returns the maximum width and height."""

    # QuickTime movies are structured as atoms containing other atoms or data.
    # The movie contains a list of tracks (both audio and video).
    # Each track has a header, which contains width and height for the track.
    # The track headers are contained in the following hierarchy:
    # - moov
    #   - trak
    #     - tkhd
    # We loop through each of the "trak"s and parse their headers.
    # Audio tracks have a width/height of zero, that's why we take the maximum sizes.
    if isinstance(f, (str, unicode)):
        f = open(f, 'rb')
    try:
        root = Atom(f)
        # There should be only one "moov"
        moov = root.find_by_type('moov')[0]
        # Inside, get all the "trak"s
        traks = moov.find_by_type('trak')
        width, height = 0, 0
        for trak in traks:
            tkhd = trak.find_by_type('tkhd')[0]
            th = TrackHeader(f, tkhd.pos)
            width = max(width, th.width)
            height = max(height, th.height)
        return width, height
    except: # Global except catcher.
        return 0, 0