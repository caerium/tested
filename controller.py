from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionTraverser, CollisionHandlerQueue
from panda3d.core import CollisionNode, CollisionSphere, BitMask32

class Controller():
    def __init__(self):
        self.key_step = 0.2
        self.mouse_step = 0.2

        self.x_center = base.win.getXSize()//2
        self.y_center = base.win.getYSize()//2
        base.win.movePointer(0, self.x_center, self.y_center)
        base.disableMouse()
        base.camLens.setFov(80)
        base.camLens.setNear(0.2)

        self.heading = 0
        self.pitch = 0

        taskMgr.doMethodLater(0.02, self.controlCamera, "camera-task")
        base.accept("escape", base.userExit)

        self.keys = dict()
        for key in ['a', 'd', 'w', 's', 'q', 'e', 'space']:
            self.keys[key] = 0
            base.accept(key, self.setKey, [key, 1])
            base.accept(key+'-up', self.setKey, [key, 0])

        self.traverser = CollisionTraverser()
        self.collisQueue = CollisionHandlerQueue()
        self.collisNode = CollisionNode('CameraSphere')
        self.collisNode.setFromCollideMask(BitMask32.bit(1))
        self.collisNode.setIntoCollideMask(BitMask32.allOff())
        collisSphere = CollisionSphere(0, 0, 0, 0.95)
        self.collisNode.addSolid(collisSphere)
        self.collisCamNode = base.camera.attachNewNode(self.collisNode)
        self.traverser.addCollider(self.collisCamNode, self.collisQueue)

        self.fall_acceleration = 0.015
        self.jump_power = 0.21

        self.fall_speed = 0
        self.ground = False
        self.edit_mode = True
        self.setEditMode(self.edit_mode)

    def setEditMode(self, mode):
        self.edit_mode = mode

        if self.edit_mode:
            self.key_step = 0.2
        else:
            self.key_step = 0.1
            self.fall_speed = 0
            self.ground = False
            base.camera.setZ(20)

    def setKey(self, key, value):
        self.keys[key] = value

    def controlCamera(self, task):
        if self.edit_mode:
            move_x = self.key_step * (self.keys['d'] - self.keys['a'])
            move_y = self.key_step * (self.keys['w'] - self.keys['s'])
            move_z = self.key_step * (self.keys['e'] - self.keys['q'])
            base.camera.setPos(base.camera, move_x, move_y, move_z)
        else:
            old_pos = base.camera.getPos()
            move_x = self.key_step * (self.keys['d'] - self.keys['a'])
            move_y = self.key_step * (self.keys['w'] - self.keys['s'])
            pitch = base.camera.getP()
            base.camera.setP(0)
            base.camera.setPos(base.camera, move_x, move_y, 0)
            base.camera.setP(pitch)

            if self.collisionTest():
                base.camera.setPos(old_pos)

            old_z = base.camera.getZ()

            if self.keys['space'] and self.ground:
                self.fall_speed = -self.jump_power
                self.ground = False

            base.camera.setZ(old_z - self.fall_speed)

            if self.collisionTest():
                base.camera.setZ(old_z)
                self.fall_speed = 0
                self.ground = True
            else:
                self.fall_speed += self.fall_acceleration

        new_mouse_pos = base.win.getPointer(0)
        new_x = new_mouse_pos.getX()
        new_y = new_mouse_pos.getY()
        if base.win.movePointer(0, self.x_center, self.y_center):
            self.heading = self.heading - (new_x - self.x_center) * self.mouse_step
            self.pitch = self.pitch - (new_y - self.y_center) * self.mouse_step
            base.camera.setHpr(self.heading, self.pitch, 0)
        
        return task.again

    def collisionTest(self):
        self.traverser.traverse(base.render)
        if self.collisQueue.getNumEntries() > 0:
            return True
        else:
            return False

if __name__ == '__main__':
    class MyApp(ShowBase):
        def __init__(self):
            ShowBase.__init__(self)
            self.model = loader.loadModel('models/environment')
            self.model.reparentTo(render)
            self.model.setScale(0.1)
            self.model.setPos(-2, 15, -3)
            self.controller = Controller()
    app = MyApp()
    app.run()