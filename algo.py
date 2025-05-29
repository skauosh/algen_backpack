import numpy as np
import random

def terminationCondition():
    return True

#simpler block for testing
class Block2:
    def __init__(self, dim):
        self.type = 0
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

        #collection that stores phenotypes (backpacks)
        #backpacks are an array of (blockBinary, type)
        self.Phenotypes = []

    #creates a backpack from [] of blocks
    def CreatePhenotype(self, blocks):
        backpack = []
        for b in blocks:
            backpack.append((self.__translateBlockToBinary(b), b.type))

        self.Phenotypes.append(backpack)

    def ListCurrentPhenotypes(self):
        for a in self.Phenotypes:
            print(a)

    #checks how much value we store inside a backpack
    #takes negative values based on how much "illegal" the configuration is
    def QualityFunction(self, backpack, typeValueArray): #typeValueArray is array that stores costs for given types
        quality = 0
        #here we need to check legality of a backpack
        for blockTuple in backpack:
            quality += typeValueArray[blockTuple[1]]
        return quality

    #parentPairs - array[idOfParent1] = idOfParent2
    def OnePointCrossoverRecombination(self, parentPairs, probability):
        #probability = chance for each parent pair to create an offspring by crossover 
        #1 - probabilty = children will be copies of one of the parents
        #returns phenotypes
        newGen = []
        for i in range(0, len(parentPairs)):
            rng = random.random()
            if (rng > probability):
                #crossover - we randomly copy one of the parents
                whichParent = random.random()
                if (whichParent > 0.5):
                    for a in self.Phenotypes[i]:
                        self.BitFlipMutation(a, 0.1)
                    newGen.append(self.Phenotypes[i])
                else:
                    for a in self.Phenotypes[i]:
                        self.BitFlipMutation(a, 0.1)
                    newGen.append(self.Phenotypes[parentPairs[i]])
            else: 
                #recombination - we take two parents, split them in a random point.
                combined = []
                length = min(len(self.Phenotypes[i]), len(self.Phenotypes[parentPairs[i]]))

                splitPoint = random.randint(0, length)
                for j in range(0, splitPoint):
                    combined.append(self.Phenotypes[i][j])
                for j in range(splitPoint, length):
                    combined.append(self.Phenotypes[parentPairs[i]][j])

                for a in combined:
                    self.BitFlipMutation(a, 0.1)
                newGen.append(combined)
        return newGen

    #flips bits of a phenotype, probability shouldn't be too big
    def BitFlipMutation(self, phenotype, probability): 
        new_phenotype = []
        for i in range(0, len(phenotype)): #over blocks
            newBin = 0b0
            for j in range(phenotype[i][0].bit_length()): #over bits of a block
                bit = (phenotype[i][0] >> j) & 1
                rng = random.random()
                if (rng < probability):
                    bit ^= 1
                newBin |= (bit << j)
            if random.random() < probability: #since above mutation makes binary numbers smaller with many iterations, some chance to grow them
                newBin |= (1 << phenotype[i][0].bit_length())
            new_phenotype.append((newBin, phenotype[i][1]))
        return new_phenotype


    def __translateBlockToBinary(self, block):
        binaryBlock = np.int64(0) #force 64 bit ints, max dimensionality is limited by this

        for i in range(self.Dimensionality-1): #set single rotation bits
            binaryBlock |= (block.rot[i] << 2*i) #i assume rotation is array,

        binaryBlock |= (block.isInside << self.isInStride)

        for i in range(self.Dimensionality):
            binaryBlock |= block.X[i] << (self.coordinatesStride + (i*8))

        return binaryBlock

    def __translateBinaryToBlock(self, blockInt64):
        block = Block2(self.Dimensionality)
        block.X = np.zeros(self.Dimensionality, dtype=np.int8)
        block.rot = np.zeros(self.Dimensionality-1, dtype=int)
        block.isInside = 0

        for i in range(self.Dimensionality - 1, -1, -1): #set single rotation bits
           block.X[i] = (blockInt64 >> self.coordinatesStride + (i*8) ) & 0xFF # &0xFF masks out bits leftover to the left

        block.isInside = (blockInt64 >> self.isInStride) & 0b1

        for i in range(self.Dimensionality - 2, -1, -1): #set single rotation bits
           block.rot[i] = (blockInt64 >> (i*2)) & 0b11

        return block


if __name__ == "__main__":
    Algo = Algorithm(3)

    #test block
    b = Block2(3)
    b.type = 4
    b.rot = [1, 2]
    b.X = [8, 97, 32]
    b.isInside = 1

    #test value array
    valueArray = [1,2,3,4,5,6]

    Algo.CreatePhenotype([b])
    Algo.ListCurrentPhenotypes()
    print(Algo.QualityFunction(Algo.Phenotypes[0], valueArray)) #should give 5