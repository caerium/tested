from direct.showbase.DirectObject import DirectObject
from panda3d.core import CollisionTraverser, CollisionNode
from panda3d.core import CollisionHandlerQueue, CollisionRay
from panda3d.core import BitMask32
from panda3d.core import LPoint3f
from mapmanager import MapManager


class Editor(DirectObject):
    def __init__(self, map_manager):
        self.map_manager = map_manager
        self.edit_mode = True
        self.traverser = CollisionTraverser()
        self.collisQueue = CollisionHandlerQueue()
        collisionNode = CollisionNode('centerRay')
        collisionNode.setFromCollideMask(BitMask32.bit(1))
        collisionNode.setIntoCollideMask(BitMask32.allOff())
        self.collisRay = CollisionRay()
        collisionNode.addSolid(self.collisRay)
        collisCamNode = base.camera.attachNewNode(collisionNode)
        self.traverser.addCollider(collisCamNode, self.collisQueue)
        self.new_position = None
        self.selected_key = None
        self.selected_node = None

        taskMgr.doMethodLater(0.02, self.testBlocksSelection,
                              "test_block-task")

        self.accept('mouse1', self.addBlock)
        self.accept('mouse3', self.delBlock)

    def setEditMode(self, mode):
        self.edit_mode = mode
        if self.edit_mode:
            self.resetSelectedBlock()
            taskMgr.doMethodLater(0.02, self.testBlocksSelection,
                                  "test_block-task")
        else:
            taskMgr.remove("test_block-task")
            self.map_manager.deselectAllBlocks()

    def resetSelectedBlock(self):
        self.new_position = None
        self.selected_key = None
        self.selected_node = None

    def addBlock(self):
        if self.new_position:
            self.map_manager.addBlock(self.new_position)
            self.resetSelectedBlock()

    def delBlock(self):
        self.map_manager.deleteSelectedBlock()
        self.resetSelectedBlock()

    def testBlocksSelection(self, task):
        self.collisRay.setFromLens(base.camNode, 0, 0)
        self.traverser.traverse(base.render)

        if self.collisQueue.getNumEntries() > 0:
            self.collisQueue.sortEntries()
            collisionEntry = self.collisQueue.getEntry(0)
            key = collisionEntry.getIntoNodePath().getTag('key')

            if key != self.selected_key:
                self.selected_key = key
                self.selected_node = self.map_manager.selectBlock(key)

            if self.selected_node:
                selected_position = self.selected_node.getPos()
                normal = collisionEntry.getSurfaceNormal(self.selected_node)
                self.new_position = selected_position + normal
        else:
            self.map_manager.deselectAllBlocks()
            self.resetSelectedBlock()
        return task.again
