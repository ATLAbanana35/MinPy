import json

from direct.showbase.ShowBase import ShowBase

class World_Saving(ShowBase):
    def __init__(self, showbase):
        self.showbase = showbase
    def save_to_file(self):
        print("Le monde à bien été enregistré")
        f = open(self.showbase.worldPath, "w")
        self.showbase.lib["entitys"]["User"] = self.showbase.JSON_World["entitys"]["User"]
        self.showbase.elib["entitys"]["User"] = self.showbase.JSON_World["entitys"]["User"]
        self.showbase.glib["lib"] = "elib"

        f.write(json.dumps({"nlib": {"blocks": self.showbase.blocks_for_file_simplet, "entitys": self.showbase.enitiys}, "lib": self.showbase.lib, "elib": self.showbase.elib, "glib": self.showbase.glib}))
        f.close()
        exit()

    def save_to_file_without_exit(self, lib):
        print("Le monde à bien été enregistré")
        f = open(self.showbase.worldPath, "w")
        self.showbase.lib["entitys"]["User"] = self.showbase.JSON_World["entitys"]["User"]
        self.showbase.elib["entitys"]["User"] = self.showbase.JSON_World["entitys"]["User"]
        self.showbase.glib["lib"] = lib

        f.write(json.dumps({"nlib": {"blocks": self.showbase.blocks_for_file_simplet, "entitys": self.showbase.enitiys}, "lib": self.showbase.lib, "elib": self.showbase.elib, "glib": self.showbase.glib}))
        f.close()
