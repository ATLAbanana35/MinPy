import json
import time

from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode

class Chat(ShowBase):
    def __init__(self, showbase):
        self.showbase = showbase
        self.text1 = ""
        self.text2 = ""
        self.text3 = ""
        self.text4 = ""
        self.time = time.time()
        self.objectText1 = None
        self.objectText2 = None
        self.objectText3 = None
        self.objectText4 = None
        self.objectText1 = OnscreenText(self.text1, align=TextNode.ALeft, pos=(-1.3,0.3))
        self.objectText2 = OnscreenText(self.text2, align=TextNode.ALeft, pos=(-1.3,0.1))
        self.objectText3 = OnscreenText(self.text3, align=TextNode.ALeft, pos=(-1.3,-0.1))
        self.objectText4 = OnscreenText(self.text4, align=TextNode.ALeft, pos=(-1.3,-0.3))
    def update(self):
        self.objectText1.destroy()
        self.objectText2.destroy()
        self.objectText3.destroy()
        self.objectText4.destroy()
        if self.time+10 > time.time():
            self.objectText1 = OnscreenText(self.text1, align=TextNode.ALeft, pos=(-1.3,0.3))
            self.objectText2 = OnscreenText(self.text2, align=TextNode.ALeft, pos=(-1.3,0.1))
            self.objectText3 = OnscreenText(self.text3, align=TextNode.ALeft, pos=(-1.3,-0.1))
            self.objectText4 = OnscreenText(self.text4, align=TextNode.ALeft, pos=(-1.3,-0.3))
    def print(self, data):
        self.time = time.time()
        self.AText1 = self.text1
        self.AText2 = self.text2
        self.AText3 = self.text3
        self.text1 = str(data)
        self.text2 = self.AText1
        self.text3 = self.AText2
        self.text4 = self.AText3