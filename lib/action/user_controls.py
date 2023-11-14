from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec4, WindowProperties, Point3, TransformState
from direct.showbase.DirectObject import DirectObject
from panda3d.core import Vec2

class UserMovement(ShowBase):
    def __init__(self, showbase):
        self.showbase = showbase
        self.showbase.verticalSpeed = 1.0
        showbase.disableMouse()
        # 
        # showbase.character = render.attachNewNode("character")
        # showbase.character.setPos(0, 0, 0)
        self.showbase = showbase

        showbase.cameraNode = showbase.character.attachNewNode("camera node")
        showbase.cameraNode.setPos(0, 10,0)
        # Position initiale de la souris
        self.lastMouseX = 0
        self.lastMouseY = 0

        base.camera.reparentTo(showbase.cameraNode)

        # Configuration de la caméra FPS
        self.accept("w", self.moveForward)
        self.accept("w-up", self.stopForward)
        self.accept("s", self.moveBackward)
        self.accept("s-up", self.stopBackward)
        self.accept("a", self.strafeLeft)
        self.accept("a-up", self.stopLeft)
        self.accept("d", self.strafeRight)
        self.accept("d-up", self.stopRight)

        self.accept("space", self.jump)

        # Gestion des déplacements et des rotations
        self.movingForward = False
        self.movingBackward = False
        self.strafingLeft = False
        self.strafingRight = False
        self.rotatingLeft = False
        self.rotatingRight = False
        self.rotatingUp = False
        self.rotatingDown = False
        # Démarrer la tâche de mise à jour de la souris
        taskMgr.add(self.mouseUpdateTask, "mouseUpdateTask")

    def startMouseRotation(self):
        self.mouseRotation = True
        taskMgr.add(self.mouseRotationTask, "mouseRotationTask")


    def startMousePan(self):
        self.mousePan = True
        taskMgr.add(self.mousePanTask, "mousePanTask")


    def mouseUpdateTask(self, task):
        try:
            # Récupérer les mouvements de la souris
            deltaX = base.mouseWatcherNode.getMouseX()
            deltaY = base.mouseWatcherNode.getMouseY()

            # Ajuster la rotation en fonction des mouvements de la souris
            rotateSpeed = 0.5
            self.showbase.character.setH(-deltaX*200)
            self.showbase.cameraNode.setP(deltaY*200)

            # Limiter la rotation de la caméra sur l'axe vertical
            # Mettre à jour les positions de la souris
            self.lastMouseX = base.mouseWatcherNode.getMouseX()
            self.lastMouseY = base.mouseWatcherNode.getMouseY()

        except AssertionError:
            oxyz = False
        return task.cont
    def jump(self):
        self.showbase.objectif = self.showbase.userShape.getTransform().getPos().getZ()+10
        self.showbase.Isjump = True  # Ajustez la valeur de la vitesse du saut selon vos besoin
    def moveForward(self):
        self.movingForward = True

    def stopForward(self):
        self.movingForward = False

    def moveBackward(self):
        self.movingBackward = True

    def stopBackward(self):
        self.movingBackward = False

    def strafeLeft(self):
        self.strafingLeft = True

    def stopLeft(self):
        self.strafingLeft = False

    def strafeRight(self):
        self.strafingRight = True

    def stopRight(self):
        self.strafingRight = False

    def update(self):
            # Vitesse de déplacement
            moveSpeed = 1
            # Déplacement en vue FPS
            if self.movingForward:
                tr=self.showbase.userShape.getTransform().getPos()
                self.showbase.userShape.setTransform(TransformState.makePos(tr + self.showbase.cameraNode.getNetTransform().getMat().getRow3(1) * moveSpeed))
            if self.movingBackward:
                tr=self.showbase.userShape.getTransform().getPos()
                self.showbase.userShape.setTransform(TransformState.makePos(tr - self.showbase.cameraNode.getNetTransform().getMat().getRow3(1) * moveSpeed))
            if self.strafingLeft:
                tr=self.showbase.userShape.getTransform().getPos()
                self.showbase.userShape.setTransform(TransformState.makePos(tr + self.showbase.cameraNode.getNetTransform().getMat().getRow3(0) * moveSpeed))
            if self.strafingRight:
                tr=self.showbase.userShape.getTransform().getPos()
                self.showbase.userShape.setTransform(TransformState.makePos(tr - self.showbase.cameraNode.getNetTransform().getMat().getRow3(0) * moveSpeed))

            # Rotation de la caméra
            rotateSpeed = 1.0
            if self.rotatingLeft:
                self.showbase.character.setH(self.showbase.character.getH() + rotateSpeed)
            if self.rotatingRight:
                self.showbase.character.setH(self.showbase.character.getH() - rotateSpeed)
            if self.rotatingUp:
                self.showbase.cameraNode.setP(self.showbase.cameraNode.getP() - rotateSpeed)
            if self.rotatingDown:
                self.showbase.cameraNode.setP(self.showbase.cameraNode.getP() + rotateSpeed)