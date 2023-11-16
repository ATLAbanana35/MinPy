import json

from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectButton import DirectButton
from panda3d.core import Vec3
class GUI_OPENING(ShowBase):
    def __init__(self, showbase):
        self.showbase = showbase
        self.elements = []
    def closeAllMenus(self):
        for element_to_destroy in self.elements:
            element_to_destroy.destroy()
        self.elements = []
        self.showbase.isGUIopen = False
        return
    def open_craft_gui(self, gui):
        if len(self.elements) != 0:
            for element_to_destroy in self.elements:
                element_to_destroy.destroy()
            self.elements = []
            self.showbase.isGUIopen = False
            return
        self.showbase.isGUIopen = True
        imageObject = OnscreenImage(image = gui["image"], pos = (0,0,0), scale=gui["scale"])
        textObject = OnscreenText(gui["Text"], pos=(0,0.9))
        for elements in gui["crafts"]:
            element = gui["crafts"][elements]
            def Give():
                witch_deleted = []
                witch_ok = 0
                witch_added = []
                for index in self.showbase.userInventory:
                    indexX = self.showbase.userInventory[index][0]
                    for Craft_Index in element:
                        number_needed = element[Craft_Index]
                        if Craft_Index == indexX["id"].replace("Item", ""):
                            if self.showbase.userInventory[index][1] >= number_needed:
                                witch_added.append([index, number_needed])
                                witch_ok += 1
                                if self.showbase.userInventory[index][1] <= 0:
                                    witch_deleted.append(index)
                            else:
                                print("Pas assez de", Craft_Index)
                                return 1
                if len(element) != witch_ok:
                    return 1
                else:
                    for Xelement in witch_added:
                        self.showbase.userInventory[Xelement[0]][1] -= Xelement[1]
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
            self.elements.append(button)
        self.elements.append(textObject)
        self.elements.append(imageObject)