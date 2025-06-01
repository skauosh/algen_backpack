import numpy as np
import random

MAX_PAIRING_ATTEMPTS = 100

def terminationCondition():
    return True

#simpler block for testing
class Block2:
    def __init__(self, dim):
        self.type = 0
        self.rot = np.zeros((dim - 1,), dtype=int) 
        self.X = np.zeros((dim,), dtype=int)

class Algorithm:
    def __init__(self, dimensionality, typeValueArray):
        self.typeValueArray = typeValueArray
        self.BlockPhenotype = [] # array of arrays of phenotypes in !!BINARY!!
        self.Dimensionality = dimensionality
        #rotation: 2 bits per dimension - 1 (since we do 0: 00 degrees, 01 = 90, 10 = 180, 11 = 270)
        #1 bit for if inside backpack or not
        #don't remember max backpack size, will assume it to be char, so 8 bits per coordinate
        self.rotationStride = 0 
        self.coordinatesStride =  (dimensionality - 1)*2 

        #collection that stores phenotypes (backpacks)
        #backpacks are an array of (blockBinary, type)
        self.Phenotypes = []
        self.PreviousGen = []

    #creates a backpack from [] of blocks
    def CreateAndAddPhenotype(self, blocks):
        backpack = []
        for b in blocks:
            backpack.append((self.__translateBlockToBinary(b), b.type))

        self.Phenotypes.append(backpack)

    def ListCurrentPhenotypes(self):
        for a in self.Phenotypes:
            print('Backpack:', end="")
            for b in a:
                c =  self.__translateBinaryToBlock(b[0])
                print(f' X:{c.X[0]} Y:{c.X[1]} R:{c.rot[0]} | ', end="")
            print('\n', end="")

    #biasParameter decides how "wide" the interval around quality of one specimen from which partner is accepted is
    def PairParentsUp(self, biasParameter, incestSwitch = 0):
        parentPairs = [] #format parentPairs[par1] = par2, int array
        
        highestSpecimenQuality = 0
        sum = 0
        for backpack in self.Phenotypes:
            a = self.QualityFunction(backpack)
            sum += a
            if a > highestSpecimenQuality:
                highestSpecimenQuality = a

        avgQuality = sum/len(self.Phenotypes)
        print(f'Average pop quality: {avgQuality}')

        print(f'HIGHEST QUALITY IN GENERATION: {highestSpecimenQuality}')


        if(incestSwitch == 0): #will write between-generation mating later
            for backpack in self.Phenotypes:
                chanceToMate = random.random()

                specimenQuality = self.QualityFunction(backpack)

                #if specimen is above average it has 70% chance to mate
                #if specimen is below, it has 30%
                #in general it should scale with quality, not simple 2 way like this
                if(specimenQuality < avgQuality):
                    if(chanceToMate > 0.7):
                        continue
                elif(chanceToMate > 0.3):
                    continue

                lowerRange = specimenQuality - specimenQuality*biasParameter
                higherRange = specimenQuality + specimenQuality*biasParameter

                i = 0
                while True:
                    potentialMateId = random.randint(0, len(self.Phenotypes)-1)
                    qualityOfPotMate = self.QualityFunction(self.Phenotypes[potentialMateId])

                    if((qualityOfPotMate > lowerRange) and (qualityOfPotMate < higherRange) and potentialMateId != self.Phenotypes.index(backpack)):
                        parentPairs.append(potentialMateId)
                        break
                    elif(i > MAX_PAIRING_ATTEMPTS):
                        parentPairs.append(-1) #-1 = no pair
                        break
                    i=i+1
        return parentPairs


    #checks how much value we store inside a backpack
    #takes negative values based on how much "illegal" the configuration is
    def QualityFunction(self, backpack): #typeValueArray is array that stores costs for given types
        quality = 0
        #here we need to check legality of a backpack
        for blockTuple in backpack:
            if(self.isInsideBackpack(blockTuple)):
                quality += self.typeValueArray[blockTuple[1]] 
            #generally, the alogorith will decide if the block is inside by moving coordinates
            #so no need for special bit for "isInsideBackpack"
        return quality

    #no sensical implementation for testing sake, HARDCODED FOR 2 DIM
    def isInsideBackpack(self, blockTuple):
        block = self.__translateBinaryToBlock(blockTuple[0])

        type = blockTuple[1]

        if(block.X[0] < 10 and block.X[0] > -10 and block.X[1] < 10 and block.X[1] > -10):
            return True
        else:
            return False

    #parentPairs - array[idOfParent1] = idOfParent2
    def OnePointCrossoverRecombination(self, parentPairs, probability):
        #probability = chance for each parent pair to create an offspring by crossover 
        #1 - probabilty = children will be copies of one of the parents
        #returns phenotypes
        newGen = []
        for i in range(0, len(parentPairs)):
            if(parentPairs[i] == -1): #skips if no pair
                continue
            rng = random.random()
            if (rng > probability):
                #crossover - we randomly copy one of the parents
                whichParent = random.random()
                if (whichParent > 0.5):
                    newOne = self.BitFlipMutation(self.Phenotypes[i], 0.01)
                    newGen.append(newOne)
                else:
                    newOne = self.BitFlipMutation(self.Phenotypes[parentPairs[i]], 0.01)
                    newGen.append(newOne)
            else: 
                #recombination - we take two parents, split them in a random point.
                combined = []
                length = min(len(self.Phenotypes[i]), len(self.Phenotypes[parentPairs[i]]))

                splitPoint = random.randint(0, length)

                for j in range(0, splitPoint):
                    combined.append(self.Phenotypes[i][j])
                for j in range(splitPoint, length):
                    combined.append(self.Phenotypes[parentPairs[i]][j])

                combined = self.BitFlipMutation(combined, 0.01)
                newGen.append(combined)
        return newGen

    #flips bits of a phenotype, probability shouldn't be too big
    def BitFlipMutation(self, phenotype, probability): 
        new_phenotype = []
        for i in range(0, len(phenotype)): #over blocks
            newBin = 0b0
            for j in range(int(phenotype[i][0]).bit_length()): #over bits of a block int(my_np_int64)
                bit = (phenotype[i][0] >> j) & 1
                rng = random.random()
                if (rng < probability):
                    bit ^= 1
                newBin |= (bit << j)
            if random.random() < probability: #since above mutation makes binary numbers smaller with many iterations, some chance to grow them
                newBin |= (1 << int(phenotype[i][0]).bit_length())
            new_phenotype.append((newBin, phenotype[i][1]))
        return new_phenotype


    def Iterate(self):
        self.PreviousGen = self.Phenotypes
        parentPair = self.PairParentsUp(0.35)
        print(parentPair)
        self.Phenotypes = self.OnePointCrossoverRecombination(parentPair, 0.75)


    def __translateBlockToBinary(self, block):
        binaryBlock = np.int64(0) #force 64 bit ints, max dimensionality is limited by this

        for i in range(self.Dimensionality-1): #set single rotation bits
            binaryBlock |= (block.rot[i] << 2*i) #i assume rotation is array,

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

        for i in range(self.Dimensionality - 2, -1, -1): #set single rotation bits
           block.rot[i] = (blockInt64 >> (i*2)) & 0b11

        return block

