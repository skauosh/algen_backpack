import numpy as np

def terminationCondition():
    return True

#simpler block for testing
class Block2:
    def __init__(self, dim):
        self.rot = np.zeros((dim - 1, ))
        self.X = np.zeros((dim, ))
        self.isInside = 0

class Algorithm:
    def __init__(self, dimensionality):
        self.BlockPhenotype = [] # array of arrays of phenotypes in !!BINARY!!
        self.Dimensionality = dimensionality
        #rotation: 2 bits per dimension - 1 (since we do 0: 00 degrees, 01 = 90, 10 = 180, 11 = 270)
        #1 bit for if inside backpack or not
        #don't remember max backpack size, will assume it to be char, so 8 bits per coordinate
        self.rotationStride = 0 
        self.isInStride = (dimensionality - 1)*2
        self.coordinatesStride = self.isInStride + 1

    def translateBlockToBinary(self, block):
        binaryBlock = np.int64(0) #force 64 bit ints, max dimensionality is limited by this

        for i in range(self.Dimensionality-1): #set single rotation bits
            binaryBlock |= (block.rot[i] << 2*i) #i assume rotation is array,

        binaryBlock |= (block.isInside << self.isInStride)

        for i in range(self.Dimensionality):
            binaryBlock |= block.X[i] << (self.coordinatesStride + (i*8))

        return binaryBlock

    def translateBinaryToBlock(self, blockInt64):
        block = Block2(self.Dimensionality)
        block.X = np.zeros(self.Dimensionality, dtype=np.int8)
        block.rot = np.zeros(self.Dimensionality-1,  dtype=np.int8)
        block.isInside = 0

        for i in range(self.Dimensionality - 1, -1, -1): #set single rotation bits
           block.X[i] = (blockInt64 >> self.coordinatesStride + (i*8) ) & 0xFF # &0xFF masks out bits leftover to the left

        block.isInside = (blockInt64 >> self.isInStride) & 0b1

        for i in range(self.Dimensionality - 2, -1, -1): #set single rotation bits
           block.rot[i] = (blockInt64 >> (i*2)) & 0b11

        return block


if __name__ == "__main__":
    A = Algorithm(3)
    b = Block2(3)
    b.rot = [1, 2]
    b.X = [8, 97, 32]
    b.isInside = 1

    #should give us: 00100000 01100001 00001000 1 10 01, 2 coordinate double bits, 1 is inside bit and 1 rotation bit
    #in normal: 67903769
    print(bin(np.int64(A.translateBlockToBinary(b)))[2:].zfill(64) )
    print(A.translateBlockToBinary(b))

    #should give the same as block we put in
    c = A.translateBinaryToBlock(A.translateBlockToBinary(b))
    print(c.rot)
    print(c.isInside)
    print(c.X)