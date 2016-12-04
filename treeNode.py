'''
Created on Oct 3, 2016

@author: Ramin
'''
from hashlib import sha256
hash_function = sha256

class TreeNode:
    def __init__(self, parentNode = None, leftChild = None, rightChild = None, siblingNode = None, nodeSide = None, data = '0', preHashed = False):
        self.parentNode = parentNode
        self.leftChild = leftChild
        self.rightChild = rightChild
        self.siblingNode = siblingNode
        self.nodeSide = nodeSide
        if preHashed:
            self.data = data
        else:
            if type(data) is bytes:
                self.data = hash_function(data).digest()
            else:
                self.data = hash_function(data.encode('utf-8')).digest()
                
    def __str__(self):
        return str(self.data.hex())
    
    def setData(self, data, perHashed = False):
        if perHashed:
            self.data = data
        else:
            if type(data) is bytes:
                self.data = hash_function(data).digest()
            else:
                self.data = hash_function(data.encode('utf-8')).digest()
    