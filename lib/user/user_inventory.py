from panda3d.core import Vec3
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText


class UserInventory(ShowBase):
    def __init__(self, showbase):
        self.showbase = showbase
        self.imagesItemsList = []
        self.AText = []
        self.showbase.accept("1", self._1)
        self.showbase.accept("2", self._2)
        self.showbase.accept("3", self._3)
        self.showbase.accept("4", self._4)
        self.showbase.accept("5", self._5)
        self.showbase.accept("6", self._6)
        self.showbase.accept("7", self._7)
        self.showbase.accept("8", self._8)
        self.showbase.accept("9", self._9)
        textObject = OnscreenText(text ='^', pos = (-0.87,-1), scale = 0.3)
        self.AText = textObject

        if not "0" in self.showbase.userInventory:
            self.showbase.selectedBlockType = "nothing"
            return

        self.showbase.selectedBlockType = self.showbase.userInventory["0"][0]["id"].replace("Item", "")

    def refresh(self):
        index = 0
        for image in self.imagesItemsList:
            image.destroy()
        for indexx in self.showbase.userInventory:
            element = self.showbase.userInventory[indexx][0]
            imageObject = OnscreenImage(image = element["image_path"], pos = (-0.87+index,0,-0.7), scale=Vec3(0.07, 0.07, 0.07))
            self.imagesItemsList.append(imageObject)
            textObject = OnscreenText(text = str(self.showbase.userInventory[indexx][1]), pos = (-0.93+index,-0.75), scale=0.1, fg=(255, 255, 255, 1))
            self.imagesItemsList.append(textObject)
            self.showbase.enitiys["User"]["data"]["inventory"] = self.showbase.userInventory
            index+=0.22
    def _1(self):
        self.AText.destroy()
        textObject = OnscreenText(text ='^', pos = (-0.87,-1), scale = 0.3)
        self.AText = textObject
        print(self.showbase.userInventory);
        if not 0 in self.showbase.userInventory:
            self.showbase.selectedBlockType = "nothing"
            return
        self.showbase.selectedBlockType = self.showbase.userInventory[0][0]["id"].replace("Item", "")
    def _2(self):
        self.AText.destroy()
        textObject = OnscreenText(text ='^', pos = (-0.65,-1), scale = 0.3)
        self.AText = textObject

        if not 1 in self.showbase.userInventory:
            self.showbase.selectedBlockType = "nothing"
            return
        self.showbase.selectedBlockType = self.showbase.userInventory[1][0]["id"].replace("Item", "")
    def _3(self):
        self.AText.destroy()
        textObject = OnscreenText(text ='^', pos = (-0.43,-1), scale = 0.3)
        self.AText = textObject

        if not 2 in self.showbase.userInventory:
            self.showbase.selectedBlockType = "nothing"
            return
        self.showbase.selectedBlockType = self.showbase.userInventory[2][0]["id"].replace("Item", "")
    def _4(self):
        self.AText.destroy()
        textObject = OnscreenText(text ='^', pos = (-0.21,-1), scale = 0.3)
        self.AText = textObject

        if not 3 in self.showbase.userInventory:
            self.showbase.selectedBlockType = "nothing"
            return
        self.showbase.selectedBlockType = self.showbase.userInventory[3][0]["id"].replace("Item", "")
    def _5(self):
        self.AText.destroy()
        textObject = OnscreenText(text ='^', pos = (-0.01,-1), scale = 0.3)
        self.AText = textObject

        if not 4 in self.showbase.userInventory:
            self.showbase.selectedBlockType = "nothing"
            return
        self.showbase.selectedBlockType = self.showbase.userInventory[4][0]["id"].replace("Item", "")
    def _6(self):
        self.AText.destroy()
        textObject = OnscreenText(text ='^', pos = (0.23,-1), scale = 0.3)
        self.AText = textObject

        if not 5 in self.showbase.userInventory:
            self.showbase.selectedBlockType = "nothing"
            return
        self.showbase.selectedBlockType = self.showbase.userInventory[5][0]["id"].replace("Item", "")
    def _7(self):
        self.AText.destroy()
        textObject = OnscreenText(text ='^', pos = (0.45,-1), scale = 0.3)
        self.AText = textObject

        if not 6 in self.showbase.userInventory:
            self.showbase.selectedBlockType = "nothing"
            return
        self.showbase.selectedBlockType = self.showbase.userInventory[6][0]["id"].replace("Item", "")
    def _8(self):
        self.AText.destroy()
        textObject = OnscreenText(text ='^', pos = (0.67,-1), scale = 0.3)
        self.AText = textObject

        if not 7 in self.showbase.userInventory:
            self.showbase.selectedBlockType = "nothing"
            return
        self.showbase.selectedBlockType = self.showbase.userInventory[7][0]["id"].replace("Item", "")
    def _9(self):
        self.AText.destroy()
        textObject = OnscreenText(text ='^', pos = (0.89,-1), scale = 0.3)
        self.AText = textObject

        if not 8 in self.showbase.userInventory:
            self.showbase.selectedBlockType = "nothing"
            return
        self.showbase.selectedBlockType = self.showbase.userInventory[8][0]["id"].replace("Item", "")