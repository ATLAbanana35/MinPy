import json

from direct.showbase.ShowBase import ShowBase

class World_Saving(ShowBase):
    def __init__(self, showbase):
        self.showbase = showbase
    def save_to_file(self):
        print("Le monde à bien été enregistré")
        f = open("../world.json", "w")
        f.write(json.dumps({"nlib": {"blocks": self.showbase.blocks_for_file_simplet, "entitys": self.showbase.enitiys}, "lib": self.showbase.lib, "elib": self.showbase.elib}))
        f.close()
        exit()