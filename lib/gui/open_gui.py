import json

from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import Vec3
class GUI_OPENING(ShowBase):
    def __init__(self, showbase):
        self.showbase = showbase
    def open_craft_gui(self, gui):
        imageObject = OnscreenImage(image = gui["image"], pos = (0,0,0), scale=Vec3(1, 1, 1))