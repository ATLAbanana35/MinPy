from panda3d.core import Vec4, DirectionalLight, AmbientLight
def setup_world(showbase):
    mainLight = DirectionalLight("main light")
    mainLightNodePath = render.attachNewNode(mainLight)
    mainLightNodePath.setHpr(45, -45, 0)
    render.setLight(mainLightNodePath)

    ambientLight = AmbientLight("ambient light")
    ambientLight.setColor(Vec4(0.2, 0.2, 0.2, 1))
    ambientLightNodePath = render.attachNewNode(ambientLight)
    render.setLight(ambientLightNodePath)

    render.setShaderAuto()
    # showbase.scene = showbase.loader.loadModel("models/environment")
    # # Reparent the model to render.
    # showbase.scene.reparentTo(showbase.render)
    # # Apply scale and position transforms on the model.
    # showbase.scene.setScale(0.25, 0.25, 0.25)
    # showbase.scene.setPos(-8, 42, 0)
    return {
        "Sz": 2,
        "Sx": 15,
        "Sy": 15
    }