from PIL import Image
import image_utility

# TO DO-- Needs Testing on a different machine

# what is needed at initialization?
#   --location in GUI
#   --default dimensions x
# what is needed to operate?
#   --image x
#   --dimensions--derived from image x
#   --toggle lock input


# test the functionality by randomly selecting a file
# from a folder with a unique number in it
class DisplayFrame:

    # Maximum size of Image
    # TO DO -- convert to height and width, keep aspect ratio of original image
    frame_limit = (1600, 1280)
    frame_default = (800, 640)
    img_blank = Image.new(mode='RGB', size=frame_default, color='black')

    def __init__(self, tags=None, current_image=img_blank,
                 frame_size=frame_default):
        self.current_image_ = current_image
        self.frame_size_ = frame_size
        self.locked = False
        self.tags_ = tags
        self.image_pool = []        # Property DP
        self.previous_images = []

    # Adds images to image_pool,
    def roll_image(self):
        try:
            self.image_pool = image_utility.list_images()
            return image_utility.random_image(self.image_pool)
        except IndexError:
            print('No images found!')

    def toggle_lock(self):
        # Toggles lock status of display image, preventing or allowing rerolls
        self.locked = not self.locked

    @property
    def tags(self):
        return self.tags_

    # Tags Property
    @tags.setter
    def tags(self, current_tags):
        # if tags are not the same as existing tags:
        if self.tags != current_tags:
            self.tags = current_tags
            # self.image_pool = image.util.list_images with new tags
        else:
            pass

    @tags.deleter
    def tags(self):
        self.tags_ = []

    # Current Image Property
    @property
    def current_image(self):
        return self.current_image_

    @current_image.setter
    def current_image(self, current_image):
        if not self.locked:
            self.previous_images.append(self.current_image_)
            self.current_image = self.roll_image(self)
        else:
            pass

    @current_image.deleter
    def current_image(self):
        self.previous_images.append(self.current_image)
        self.current_image = self.img_blank             # Property DP'

    # Frame Size Property
    @property
    def frame_size(self):
        return self.frame_size_

    @frame_size.setter
    def frame_size(self, frame_size):
        if self.Image.current_image.size > self.frame_limit:
            self.frame_size_ = self.frame_limit
        else:
            self.frame_size_ = self.Image.current_image.size

    # methods:
    # import from prebuilt functions
    # toggle_lock x
    # export image -- should work at a larger level,
        # the container for the 2 display frames

    # build from scratch...
    # set_image x
    # --use property design pattern
    # set_dimensions x
