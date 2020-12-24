from direct.showbase.ShowBase import ShowBase
from panda3d.core import LPoint3f
from random import randint, random
import pickle
from block import Block

def getRandomColor():
    return (random()*0.3+0.7,
            random()*0.3+0.7,
            random()*0.3+0.7, 1)

def getSelectColor(color):
    if color is None:
        return (0.15, 0.15, 0.15, 0.9)
    else:
        return (color[0]*0.4,
                color[1]*0.4,
                color[2]*0.4, 0.9)


class MapManager():
    def __init__(self):
        self.blocks = list()
        self.selected_block = None
        self.color = None
        self.selected_color = getSelectColor(self.color)

    def addBlock(self, position, color=None):
        for block in self.blocks:
            if block.getPos() == position:
                return

        if color is None:
            if self.color is None:
                color = getRandomColor()
            else:
                color = self.color

        block = Block(position, color)
        self.blocks.append(block)

    def setColor(self, color):
        self.color = color
        self.selected_color = getSelectColor(self.color)

        if self.selected_block:
            self.selected_block.updateColor(self.selected_color)

    def basicMap(self):
        self.clearAll()

        for i in range(-7,8):
            for j in range(-7,8):
                pos = (i, j, -2)
                self.addBlock(pos, (1,1,1,1))
    
    def generateRandomMap(self):
        self.clearAll()
        for i in range(-8,9):
            for j in range(-8,9):
                pos = (i, j, randint(-4,-2))
                self.addBlock(pos)

        for i in range(-8,9):
            for j in range(-8,9):
                if -5 < i < 5 and -5 < j < 5:
                    continue
                pos = (i, j, randint(-1,6))
                self.addBlock(pos)

    def createMap(self, colors, matrix, shift):
        self.clearAll()

        for z in range(len(matrix)):
            for y in range(len(matrix[z])):
                for x in range(len(matrix[z][y])):
                    key = matrix[z][y][x]
                    if key in colors and colors[key]:
                        pos = (x + shift[0],
                               - y - shift[1],
                               z + shift[2])
                        self.addBlock(pos, colors[key])

    def deselectAllBlocks(self):
        for block in self.blocks:
            block.setSelected(False)

    def selectBlock(self, key):
        self.selected_block = None

        for block in self.blocks:
            if block.getKey() == key:
                self.selected_block = block
                block.setSelected(True, self.selected_color)
            else:
                block.setSelected(False)

        if self.selected_block:
            return self.selected_block.getNode()
        else:
            return None

    def deleteSelectedBlock(self):
        if self.selected_block:
            self.selected_block = None

            for i in range(len(self.blocks)):
                if self.blocks[i].getSelected():
                    self.blocks[i].remove()
                    del self.blocks[i]
                    break
                    
    def clearAll(self):
        self.selected_block = None
        for block in self.blocks:
            block.remove()
        self.blocks.clear()

    def saveMap(self, filename):
        if not self.blocks:
            return
        fout = open(filename, 'wb')
        pickle.dump(len(self.blocks), fout)

        for block in self.blocks:
            pickle.dump(block.getPos(), fout)
            pickle.dump(block.getColor(), fout)
        fout.close()

    def loadMap(self, filename):
        self.clearAll()
        fin = open(filename, 'rb')
        lenght = pickle.load(fin)

        for i in range(lenght):
            pos = pickle.load(fin)
            color = pickle.load(fin)
            self.addBlock(pos, color)
        fin.close()


if __name__ == '__main__':
    from direct.showbase.ShowBase import ShowBase
    from controller import Controller

    class MyApp(ShowBase):

        def __init__(self):
            ShowBase.__init__(self)

            self.controller = Controller()

            self.map_manager = MapManager()

            self.accept('f1', self.map_manager.basicMap)
            self.accept('f2', self.map_manager.generateRandomMap)
            self.accept('f3', self.map_manager.saveMap, ["testmap.dat"])
            self.accept('f4', self.map_manager.loadMap, ["testmap.dat"])
            self.accept('f5', self.createMap)

            print("'f1' - создать базовую карту")
            print("'f2' - создать случайную карту")
            print("'f3' - сохранить карту")
            print("'f4' - загрузить карту")
            print("'f5' - создать карту по вложенному списку")

            self.map_manager.generateRandomMap()

        def createMap(self):
            colors = {'R':(1.0, 0, 0, 1),
                      'G':(0, 1.0, 0, 0.5),
                      'B':(0, 0, 1.0, 0.5),
                      'Y':(1.0, 1.0, 0, 1),
                      'O':(1.0, 0.5, 0.0, 1),
                      'W':(1.0, 1.0, 1.0, 1),
                      '-':None}

            blocks = [
                [['G','O','O','O','G'],
                 ['O','-','-','-','O'],
                 ['O','-','W','-','O'],
                 ['O','-','-','-','O'],
                 ['G','O','O','O','G']],

                [['G','-','-','-','G'],
                 ['-','-','-','-','-'],
                 ['-','-','W','-','-'],
                 ['-','-','-','-','-'],
                 ['G','-','-','-','G']],

                [['G','-','R','-','G'],
                 ['-','-','R','-','-'],
                 ['R','R','W','R','R'],
                 ['-','-','R','-','-'],
                 ['G','-','R','-','G']],

                [['G','-','-','-','G'],
                 ['-','-','-','-','-'],
                 ['-','-','W','-','-'],
                 ['-','-','-','-','-'],
                 ['G','-','-','-','G']],

                [['G','Y','Y','Y','G'],
                 ['Y','-','-','-','Y'],
                 ['Y','-','W','-','Y'],
                 ['Y','-','-','-','Y'],
                 ['G','Y','Y','Y','G']],
                ]

            self.map_manager.createMap(colors, blocks, (-2,-10,-2))


    app = MyApp()
    app.run()
