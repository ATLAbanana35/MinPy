import json

from direct.showbase.ShowBase import ShowBase

class World_Saving(ShowBase):
    def __init__(self, showbase):
        self.showbase = showbase
    def save_to_file(self):
        print("Le monde à bien été enregistré")
        f = open("world.json", "w")
        self.showbase.nlib["entitys"]["User"] = self.showbase.JSON_World["entitys"]["User"]
        self.showbase.elib["entitys"]["User"] = self.showbase.JSON_World["entitys"]["User"]
        f.write(json.dumps({"lib": {"blocks": self.showbase.blocks_for_file_simplet, "entitys": self.showbase.enitiys}, "nlib": self.showbase.nlib, "elib": self.showbase.elib}))
        f.close()
        exit()
    def save_to_file_without_exit(self):
        print("Le monde à bien été enregistré")
        f = open("world.json", "w")
        self.showbase.nlib["entitys"]["User"] = self.showbase.JSON_World["entitys"]["User"]
        self.showbase.elib["entitys"]["User"] = self.showbase.JSON_World["entitys"]["User"]
        f.write(json.dumps({"lib": {"blocks": self.showbase.blocks_for_file_simplet, "entitys": self.showbase.enitiys}, "nlib": self.showbase.nlib, "elib": self.showbase.elib}))
        f.close()
