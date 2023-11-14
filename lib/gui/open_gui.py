import json

from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectButton import DirectButton
from panda3d.core import Vec3
class GUI_OPENING(ShowBase):
    def __init__(self, showbase):
        self.showbase = showbase
    def open_craft_gui(self, gui):
        imageObject = OnscreenImage(image = gui["image"], pos = (0,0,0), scale=gui["scale"])
        textObject = OnscreenText(gui["Text"], pos=(0,0.9))
        for elements in gui["crafts"]:
            element = gui["crafts"][elements]
            def Give():
                witch_deleted = []
                for index in self.showbase.userInventory:
                    indexX = self.showbase.userInventory[index][0]
                    for Craft_Index in element:
                        number_needed = element[Craft_Index]
                        if Craft_Index == indexX["id"].replace("Item", ""):
                            if self.showbase.userInventory[index][1] >= number_needed:
                                self.showbase.userInventory[index][1] -= number_needed
                                if self.showbase.userInventory[index][1] <= 0:
                                    witch_deleted.append(index)
                            else:
                                print("Pas assez de", Craft_Index)
                                return 1
                for element_2s in witch_deleted:
                    del self.showbase.userInventory[element_2s]
                ObjectType = elements
                trne = 0
                for indexX_1234 in self.showbase.userInventory:
                    element_1234 = self.showbase.userInventory[indexX_1234]
                    if element_1234[0]["id"].replace("Item", "") == ObjectType:
                        self.showbase.userInventory[indexX_1234][1] += 1
                        trne = 1
                if trne == 0:
                    self.showbase.userInventory[len(self.showbase.userInventory)] = [self.showbase.mods_items[ObjectType], 1]

            string_x  = ""
            for element_2 in element:
                string_x = ", " + string_x + str(element[element_2]) + " of "+element_2
            button = DirectButton(pos=(-0.6,0,0), scale=0.1, command=Give, text=f"{elements} {string_x}")
        def Destroy():
            imageObject.destroy()
            textObject.destroy()
        self.showbase.accept("e", Destroy)
