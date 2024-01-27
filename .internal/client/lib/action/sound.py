from panda3d.core import AudioSound
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3, Point3
class Sound(ShowBase):
    def __init__(self, showbase):
        self.showbase = showbase
    def play(self, path, pos=None):
        # Charger le fichier audio
        sound_path = "ressources/sound/"+path  # Remplacez cela par le chemin de votre fichier audio
        self.sound = loader.loadSfx(sound_path)
        if pos == None:
            pos = Vec3(self.showbase.enitiys["User"]["pos"]["x"], self.showbase.enitiys["User"]["pos"]["y"], self.showbase.enitiys["User"]["pos"]["z"])
        # Position initiale du son
        self.sound.set3dAttributes(pos.x, pos.y, pos.z, 0, 0, 0)

        # Jouer le son
        self.sound.play()
        return self.sound
