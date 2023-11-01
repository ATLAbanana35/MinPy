import json

from direct.showbase.ShowBase import ShowBase

class World_Saving(ShowBase):
    def __init__(self, showbase):
        self.showbase = showbase
    def save_to_file(self):
        print("Le monde à bien été enregistré")
        f = open("world.json", "w")
        f.write(json.dumps(self.showbase.blocks_for_file_simplet))
        f.close()
        exit()