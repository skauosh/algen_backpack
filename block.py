import numpy as np
import regex as re

N = 2

class Block:
    def __init__(self, value, shape_init="default", dim=N):
        self.value = value
        self.init_hitbox = np.array([
            [ 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0],
            [ 0, 1, 1, 1, 0],
            [ 0, 0, 0, 1, 0],
            [ 0, 0, 0, 0, 0]
        ], dtype='int')
        self.offset=np.array([2,2])
        self.hitbox = self.init_hitbox
        self.X = np.zeros((N, ))
        self.rot = 0
        self.inside = False
        
    def __str__(self):
        out=f"value={self.value} "
        out+=f"X={self.X} "
        out+=f"rot={self.rot} "
        out+=f"inside={self.inside}\n"
        out+=f"{self.hitbox}"
        return out
        
    def SetRotation(self, rot):
        self.rot :int = rot
        self.hitbox = np.rot90(self.init_hitbox, k=self.rot)

class Backpack:
    def __init__(self, shape=tuple([10]*N)):
        self.shape=shape
        self.board=np.zeros(self.shape, dtype='int')
        self.ls = []
    def __str__(self):
        tab = '\n'.join(map(str, [''.join(map(str, self.board[i])) for i in range(self.shape[0])]))
        tab += f"\n{self.list}"
        return tab
    # def IsAvailable(self, block, coordinates, rotation):
    # def FillCells(self, block, coordinates, rotation):
    # def AddBlock(self, block, coordinates, rotation=0):
    #     block.SetRotation(rotation)
    #     self.ls.append(block)
    # def RemoveBlock
 

if __name__ == "__main__":
    block = Block(5)
    backpack=Backpack()
    block.SetRotation(2)
    print(block)
    print(backpack)