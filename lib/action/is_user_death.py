from direct.showbase.ShowBase import ShowBase

class IsUserDead(ShowBase):
    def __init__(self, showbase):
        self.dead_fall = "Vous êtes mort de chute"
        self.showbase = showbase
    def update_dead(self):
        if self.showbase.character.getZ() < -1000:
            print(self.dead_fall)
            exit()