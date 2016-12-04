'''
Created on Oct 2, 2016

@author: Ramin
'''
import math
import sys

from treeNode import TreeNode
from utilities import utilities


class MerkleError(Exception):
    pass

class MerkleTree:
    def __init__(self):
        self.root = None
        self.dbCounter = 0
        self.tmpSubTreelstLeaves = []
        self.lstLeaves = []
        self.tmpSubTreelstDataBlock = []
        self.lstDataBlocks = []
        self._lastRootHash = 0

    def _getPathFromRoot(self, leaf):
        if leaf != None:
            return self._getPathFromRoot(leaf.parentNode) + [leaf]
        else: return []
                    
    def getDataBlocks(self):
        lstResult = []
        for lstData in self.lstDataBlocks:
            for data in lstData:        
                lstResult.append(data)
        return lstResult
    
    def getDataIndices(self, pathIndex):
        if self.root == None:
            return -1, -1
        
        layerIndex = 0
        leafIndex = pathIndex
        blockCounter = 0
        
        for i in range(len(self.lstLeaves)):
            blockCounter += len(self.lstLeaves[i])
            if leafIndex >= len(self.lstLeaves[i]):
                leafIndex -= len(self.lstLeaves[i])
                layerIndex += 1
            else:
                break
        
        if blockCounter <= pathIndex:
            return -1, -1
        return layerIndex, leafIndex
    
    def getPathData(self, curNode):
        pathData = []
        while curNode != None:
            pathData.append((curNode.nodeSide, curNode.data.hex()[0:5]))
            curNode = curNode.parentNode
        return pathData
   
    def getAllPathsData(self):
        lstTmp = []
        for pathIndex in range(len(self.lstLeaves)):
            lstTmp.append([self.getPathData(sLeaf) for sLeaf in self.lstLeaves[pathIndex]])
        return lstTmp

    def printPath(self, layerIndex, leafIndex):
        if layerIndex < len(self.lstLeaves):
            if leafIndex < len(self.lstLeaves[layerIndex]):
                print(self.lstDataBlocks[layerIndex][leafIndex], '=>', self.getPathData(self.lstLeaves[layerIndex][leafIndex]))      
        else:
            print('>>> Error: Given index is out of range!!!')
            
    def __makeSubTree(self, parNode, curLevel, treeLevel, dataBlocks):
        left = TreeNode(parentNode = parNode, nodeSide = 'L')
        if curLevel < treeLevel:
            self.__makeSubTree(left, curLevel + 1, treeLevel, dataBlocks)
        else:
            #left.setData(self.__getSHA256(dataBlocks[self.dbCounter]))
            left.setData(dataBlocks[self.dbCounter])
            self.tmpSubTreelstLeaves.append(left)
            self.tmpSubTreelstDataBlock.append(dataBlocks[self.dbCounter])
            self.dbCounter += 1
        
        right = TreeNode(parentNode = parNode, nodeSide = 'R')
        if curLevel < treeLevel:
            self.__makeSubTree(right, curLevel + 1, treeLevel, dataBlocks)
        else:
            right.setData(dataBlocks[self.dbCounter])
            self.tmpSubTreelstLeaves.append(right)
            self.tmpSubTreelstDataBlock.append(dataBlocks[self.dbCounter])
            self.dbCounter += 1
        
        parNode.setData(left.data + right.data)
        parNode.leftChild = left
        parNode.rightChild = right
        #parNode.setData(str(left) + str(right))
    
    def createTree(self, dataBlocks = [], setAsMainTree = False):
        if setAsMainTree:
            if self.root != None:
                del self.root
                del self.lstDataBlocks
                del self.lstLeaves
                self.lstLeaves = []
                self.lstDataBlocks = []
            
        thisRoot = None
        self.dbCounter = 0
        self.counter = 0
        dbCount = len(dataBlocks)
        subTreesHeight = []
        leafsCount = []
        # Calculating sub trees information
        while dbCount > 0:
            subTreesHeight.append(int(math.log2(dbCount)) + 1)
            leafCount = 2 ** int(math.log2(dbCount))
            leafsCount.append(leafCount)
            dbCount -= leafCount
        
        # Generating subtrees of merkle tree
        roots = []
        for s in subTreesHeight:
            tNode = TreeNode(nodeSide = 'Root')
            roots.append(tNode)
            self.tmpSubTreelstLeaves = []
            self.tmpSubTreelstDataBlock = []
            if s > 1:
                self.__makeSubTree(roots[len(roots) - 1], 1, s - 1, dataBlocks)
                self.lstLeaves.append(self.tmpSubTreelstLeaves)
                self.lstDataBlocks.append(self.tmpSubTreelstDataBlock)
            else:
                self.tmpSubTreelstLeaves.append(tNode)
                self.tmpSubTreelstDataBlock.append(dataBlocks[self.dbCounter])
                tNode.setData(dataBlocks[self.dbCounter])
                self.dbCounter += 1
                self.lstLeaves.append(self.tmpSubTreelstLeaves)
                self.lstDataBlocks.append(self.tmpSubTreelstDataBlock)
         
        # joining subtrees to make main merkle tree
        if len(roots) > 0:
            lastRootIndex = len(roots) - 1
            thisRoot = roots[lastRootIndex]
            i = lastRootIndex - 1
            while i >= 0:
                tNode = TreeNode(data = roots[i].data + thisRoot.data, nodeSide = 'Root')
                thisRoot.parentNode = tNode
                roots[i].parentNode = tNode
                
                tNode.leftChild = roots[i] 
                tNode.rightChild = thisRoot
                
                roots[i].nodeSide = 'L'
                thisRoot.nodeSide = 'R'
                
                thisRoot = tNode
                i -= 1
        if setAsMainTree:
            self.root = thisRoot
        return thisRoot
    
    def getCommonParent(self, leafA, leafB):
        lstA = []
        while leafA != None:
            lstA.append(leafA)
            leafA = leafA.parentNode
        while leafB != None:
            if leafB in lstA:
                return leafB
            leafB = leafB.parentNode
        return None
    
    def combineSimilarSubTrees(self):
        l = len(self.lstLeaves) - 1
        while l > 0:
            if len(self.lstLeaves[l]) == len(self.lstLeaves[l - 1]):
                for i in range(len(self.lstLeaves[l])):
                    self.lstLeaves[l - 1].append(self.lstLeaves[l][i])
                    self.lstDataBlocks[l - 1].append(self.lstDataBlocks[l][i])
                del self.lstLeaves[l]
                del self.lstDataBlocks[l]
                l = len(self.lstLeaves)
            l -= 1
        
    def addOneBlock(self, data):
        if len(self.lstLeaves) == 0:
            raise MerkleError('The tree has not been created and new block cannot be added to the null tree.')
        elif len(self.lstLeaves) == 1:
            tmpRoot = TreeNode(nodeSide = 'Root')
            newLeafNode = TreeNode(data = data, parentNode = tmpRoot, nodeSide = 'R')
            self.lstLeaves.append([newLeafNode])
            self.lstDataBlocks.append([data])
            self.root.parentNode = tmpRoot
            self.root.nodeSide = 'L'
            
            tmpRoot.leftChild = self.root
            tmpRoot.rightChild = newLeafNode
            tmpRoot.setData(self.root.data + newLeafNode.data)
            
            self.root = self.root.parentNode
        else:
            lastLayerIndex = len(self.lstLeaves) - 1
            llFirstLeaf = self.lstLeaves[lastLayerIndex][0]
            bllFirstLeaf = self.lstLeaves[lastLayerIndex - 1][0]
            
            commonParent = self._getCommonParent(llFirstLeaf, bllFirstLeaf)
            
            newLeafNode = TreeNode(data = data, nodeSide = 'R')
            tmpNode = TreeNode(parentNode = commonParent, leftChild = commonParent.rightChild, rightChild = newLeafNode, nodeSide = 'R')

            commonParent.rightChild.nodeSide = 'L'
            commonParent.rightChild = tmpNode

            tmpNode.leftChild.parentNode = tmpNode
            tmpNode.rightChild.parentNode = tmpNode
            
            
            self.lstLeaves.append([newLeafNode])
            self.lstDataBlocks.append([data])
            
            while tmpNode != None:
                tmpNode.setData(tmpNode.leftChild.data + tmpNode.rightChild.data)
                tmpNode = tmpNode.parentNode
        
        self.combineSimilarSubTrees()
                    
        ### Temporary for test
        #self.printAllPaths()
        #leavesCount = [len(x) for x in self.lstLeaves]
        #print(leavesCount)
        
    def addManyDataBlocks(self, dataBlocks):
        if len(self.lstLeaves) == 1 and math.log2(len(self.lstLeaves[0])).is_integer():
            newTreeRoot = self.createTree(dataBlocks, False)
            mainRoot = TreeNode(data = self.root.data + newTreeRoot.data, leftChild = self.root, rightChild = newTreeRoot, nodeSide = 'Root')
            
            self.root.nodeSide = 'L'
            self.root.parentNode = mainRoot
            
            newTreeRoot.nodeSide = 'R'
            newTreeRoot.parentNode = mainRoot
            
            self.root = self.root.parentNode
            self.combineSimilarSubTrees()
        else:
            for data in dataBlocks:                
                self.addOneBlock(data)
                if len(self.lstLeaves) == 1:
                    remainingDataIndex = dataBlocks.index(data)
                    remainingDataBlocks = dataBlocks[remainingDataIndex + 1:]
                    if len(remainingDataBlocks) > 0:
                        newTreeRoot = self.createTree(remainingDataBlocks, False)
                        mainRoot = TreeNode(data = self.root.data + newTreeRoot.data, leftChild = self.root, rightChild = newTreeRoot, nodeSide = 'Root')
            
                        self.root.nodeSide = 'L'
                        self.root.parentNode = mainRoot
            
                        newTreeRoot.nodeSide = 'R'
                        newTreeRoot.parentNode = mainRoot
            
                        self.root = self.root.parentNode
                        self.combineSimilarSubTrees()
                        return self.root
                    else:
                        return self.root
        
        return self.root
            
    def getSiblingNode(self, node):
        if node.nodeSide == 'R':
            return node.parentNode.leftChild
        elif node.nodeSide == 'L':
            return node.parentNode.rightChild
        else:
            return node

    def getLevel(self, node):
        level = 0
        while node != None:
            node = node.parentNode
            level += 1
        return level
    '''
    def proofOfPath(self, layerIndex, leafIndex):
        lstProofPathChain = []

        curNode = self.lstLeaves[layerIndex][leafIndex]
        # sibNode = self._getSiblingNode(curNode)
        # lstProofPathChain.append(sibNode)
        
        while curNode.nodeSide != 'Root':
            
            sibNode = self._getSiblingNode(curNode)
            
            parHashVal = None
            if curNode.nodeSide == 'R':
                parHashVal = utilities.getHash(sibNode.data + curNode.data)
            elif curNode.nodeSide == 'L':
                parHashVal = utilities.getHash(curNode.data + sibNode.data)
            
            if parHashVal != curNode.parentNode.data:
                return lstProofPathChain, False
            
            lstProofPathChain.append(sibNode)
        
            curNode = curNode.parentNode
        
        lstProofPathChain.append(curNode)
        return lstProofPathChain, True    

    def _consistGetInfo(self, k1, k2):
        if k1 + 1 == k2:
            layerIndex, leafIndex = self.getDataIndices(k1)
            return (self.lstLeaves[layerIndex][leafIndex], self._getLevel(self.lstLeaves[layerIndex][leafIndex]))
        else:
            layerIndexA, leafIndex = self.getDataIndices(k1)
            leafA = self.lstLeaves[layerIndexA][leafIndex]

            layerIndexB, leafIndex = self.getDataIndices(k2 - 1)
            leafB = self.lstLeaves[layerIndexB][leafIndex]

            commonParent = self._getCommonParent(leafA, leafB)
            
            return (commonParent, self._getLevel(commonParent))

    def consistProof(self, m, k1, k2, b):
        if m == k2 - k1:
            if b == False:
                return [self._consistGetInfo(k1, k2)]
            return []
        else:
            t = math.log2(k2 - k1)
            if t.is_integer(): t = int(t) - 1
            else: t = int(t)
            k = 2 ** t
            
            if m <= k:
                return [self._consistGetInfo(k1 + k, k2)] + self.consistProof(m, k1, k1 + k, b)
            else:
                return [self._consistGetInfo(k1, k1 + k)] + self.consistProof(m - k, k1 + k, k2, False)            

    def ConsistVerify(self, lstProof, lstOrder):
        proved = False
        
        if proved == True:
            self._lastRootHash = str(self.root)
        return proved
    '''