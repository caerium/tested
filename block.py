from panda3d.core import Texture, TextureStage
from panda3d.core import BitMask32
from panda3d.core import TransparencyAttrib

class Block():
    current_index = 0

    def __init__(self, position=(0, 0, 0), color=(1, 1, 1, 1)):
        self.key = str(Block.current_index)
        Block.current_index += 1
        self.selected = False
        self.block = loader.loadModel('block')
        tex = loader.loadTexture('block.png')
        self.block.setTexture(tex)
        self.block.setTransparency(TransparencyAttrib.MAlpha)
        self.block.reparentTo(render)
        self.block.setPos(position)
        self.color = color
        self.block.setColor(self.color)

        collisionNode = self.block.find("*").node()
        collisionNode.setIntoCollideMask(BitMask32.bit(1))
        collisionNode.setTag('key', self.key)

    def getKey(self):
        return self.key

    def getColor(self):
        return self.color

    def getPos(self):
        return self.block.getPos()

    def getNode(self):
        return self.block

    def setSelected(self, selected, color = (0, 0, 1, 1)):
        if self.selected != selected:
            self.selected = selected
            if self.selected:
                self.block.setColor(color)
            else:
                self.block.setColor(self.color)

    def updateColor(self, color):
        self.block.setColor(color)

    def getSelected(self):
        return self.selected

    def remove(self):
        self.block.removeNode()


if __name__ == '__main__':
    from direct.showbase.ShowBase import ShowBase

    class MyApp(ShowBase):

        def __init__(self):
            ShowBase.__init__(self)

            b1 = Block((0,10,0), (0.5,1,0.5,0.2))
            b2 = Block((1,10,0), (1,1,0.5,1))
            b3 = Block((0,10,2), (0.5,1,1,1))
            b4 = Block((-2,15,-2), (1,0.5,1,1))

    app = MyApp()
    app.run()


