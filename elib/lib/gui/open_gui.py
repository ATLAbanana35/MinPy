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
        imageObject = OnscreenImage(image = "../"+gui["image"], pos = (0,0,0), scale=gui["scale"])
        textObject = OnscreenText(gui["Text"], pos=(0,0.9))
        in_ = 0.8
        for elements in gui["crafts"]:
            element = gui["crafts"][elements]
            def create_give_function(elements=elements):
                def Give():
                    element = gui["crafts"][elements]
                    if element.get("shell") != None:
                        exec(element.get("shell"))
                        del element["shell"]
                    witch_deleted = []
                    witch_ok = 0
                    witch_added = []
                    for index in self.showbase.userInventory:
                        indexX = self.showbase.userInventory[index][0]
                        for Craft_Index in element:
                            number_needed = element[Craft_Index]
                            if Craft_Index == indexX["id"].replace("Item", "") and Craft_Index != "shell":
                                if self.showbase.userInventory[index][1] >= number_needed:
                                    witch_added.append([index, number_needed])
                                    witch_ok += 1
                                    if self.showbase.userInventory[index][1] <= 0:
                                        witch_deleted.append(index)
                                else:
                                    print("Pas assez de", Craft_Index, "pour faire un", elements)
                                    return 1
                    if len(element) != witch_ok:
                        print("Il manque un element!")
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
                        if len(self.showbase.userInventory) == 0:
                            self.showbase.userInventory[len(self.showbase.userInventory)] = [self.showbase.mods_items[ObjectType], 1]
                        else:
                            for indexX in range(0, 9):
                                if not indexX in self.showbase.userInventory and not str(indexX) in self.showbase.userInventory:
                                    self.showbase.userInventory[indexX] = [self.showbase.mods_items[ObjectType], 1]
                                    print(indexX, self.showbase.userInventory)
                                    break
                return Give
            string_x  = ""
            for element_2 in element:
                if element_2 != "shell":
                    string_x = string_x + ", " + str(element[element_2]) + " of "+element_2

            button = DirectButton(pos=(-0.5,0,0+in_), scale=0.05, command=create_give_function(), text=f"{elements} {string_x}")
            in_ -= 0.1
            self.elements.append(button)
        self.elements.append(textObject)
        self.elements.append(imageObject)