'''
Created on Oct 3, 2016

@author: Ramin
'''

import sys
from merkleTree import MerkleTree
from utilities import utilities
from verifier import verifier
from prover import prover

def printLeavesCount(lstLeaves):
    leavesCount = [len(x) for x in lstLeaves]
    print(leavesCount)

def aboutUs():
    print(utilities.BOLD + utilities.OKGREEN + '*****************************************************')
    print(utilities.BOLD + utilities.WARNING + '>>> Merkle Tree (Ver 1.2)\n>>> By Ramin Armanfar\n>>> Date: Oct 3, 2016\n>>> Last Update: Nov 20, 2016\nEmail: ramin.armanfar@gmail.com' + utilities.ENDC)
    print(utilities.BOLD + utilities.OKGREEN + '*****************************************************' + utilities.ENDC)

def getDataFromInput():
    dataBlockCount = 0
    while True:
        txtDataBlockCount = input(utilities.OKBLUE + 'Enter number of initial data blocks to create tree: ' + utilities.ENDC)
        try:
            dataBlockCount = int(txtDataBlockCount)
            break
        except:
            print(utilities.WARNING + '>>> Error: You must enter numeric value which represents the number of initial data blocks !!!' + utilities.ENDC)
            pass
            
    dataBlocks = []
    for i in range(dataBlockCount):
        db = input(utilities.OKBLUE + 'Enter number data block ' + str(i) + ' value: ' + utilities.ENDC)
        dataBlocks.append(db)
    return dataBlocks
    
def createTreeWithUserInput(mt):
    dataBlocks = getDataFromInput()

    #print(dir(mt))
    mt.createTree(dataBlocks, True)

def importDataFromFile():
    fn = input(utilities.OKBLUE + 'Enter number file name: ' + utilities.ENDC)
    fpt = open(fn, 'r')
    splitter = input(utilities.OKBLUE + 'Enter splitter character: ' + utilities.ENDC)
    dataBlocks = fpt.read()
    dataBlocks = dataBlocks.rstrip()
    dataBlocks = dataBlocks.split(splitter)
    return dataBlocks
    
def createTreeFromFile(mt):
    dataBlocks = importDataFromFile()
    print(utilities.OKGREEN + 'Imported data are: ' + utilities.ENDC)
    print(dataBlocks)
    #print(dir(mt))
    mt.createTree(dataBlocks, True)

def addOneDataBlock(mt):
        value = input(utilities.OKBLUE + 'Enter data block value to add to the tree: ' + utilities.ENDC)
        try:
            mt.addOneBlock(value)
            print(utilities.OKBLUE + '>>> Given value (', value, ') has been added to the tree successfully...' + utilities.ENDC) 
        except:
            print(utilities.FAIL + '>>> Error: Tree object is not exist !!!')
            print('>>> You may need to create tree first...' + utilities.ENDC)

def addManyDataBlocksToTree(mt):
    if mt.root == None:
        yn = ''
        while True:
            yn = input(utilities.WARNING + '>>> Three has not been generated yet! do you want to create tree using given data blocks? (y/n)' + utilities.ENDC)
            if yn == 'y' or yn == 'n' or yn == 'Y' or yn == 'N':
                break
        if yn =='y' or yn == 'Y':
            dataBlocks = importDataFromFile()
            print(utilities.OKBLUE + 'Imported data are: ' + utilities.ENDC)
            print(dataBlocks)
            mt.createTree(dataBlocks, True)
    else:
        dataBlocks = getDataFromInput()
        mt.addManyDataBlocks(dataBlocks)
    
def addManyDataBlocksToTreeFromFile(mt):
    if mt.root == None:
        yn = ''
        while True:
            yn = input(utilities.WARNING + '>>> Three has not been generated yet! do you want to create tree using given data blocks? (y/n)' + utilities.ENDC)
            if yn == 'y' or yn == 'n' or yn == 'Y' or yn == 'N':
                break
        if yn =='y' or yn == 'Y':
            dataBlocks = importDataFromFile()
            print(utilities.OKBLUE + 'Imported data are: ' + utilities.ENDC)
            print(dataBlocks)
            mt.createTree(dataBlocks, True)
    else:
        dataBlocks = importDataFromFile()
        print('Imported data are: ')
        print(dataBlocks)
        mt.addManyDataBlocks(dataBlocks)
        
    
def main(argv):
    mt = MerkleTree()
    aboutUs()
    menuItem = '-'
    #utilities.clearScreen()

    while True:
        print('\n' + utilities.BOLD + utilities.OKGREEN + '*************** Merkle-Tree Main Menu ***************' + utilities.ENDC)
        print(utilities.OKBLUE + '1) Create Merkle-Tree')
        print('2) Add new data block(s)')
        print('3) Show a path')
        print('4) Graph Tree')
        print('5) Proof of path')
        print('6) Proof of consistency')
        print('7) About Us')
        print('0) Exit' + utilities.ENDC)
        menuItem = input(utilities.OKGREEN + 'Choose an item (0 - 7): ' + utilities.ENDC)
        if menuItem == '0': ### Exit the program
            while True:
                yn = input(utilities.WARNING + 'Exit Program, Are you sure? (y/n): ' + utilities.ENDC)
                if yn == 'y' or yn == 'n' or yn == 'Y' or yn == 'N': break
            if yn == 'y' or yn == 'Y':
                aboutUs()
                print(utilities.OKBLUE + utilities.BOLD + 'Thank you for using the application...' + utilities.ENDC)
                break

        elif menuItem == '1': ### Create tree by giving number of specific values from the user
            while True:
                print(utilities.BOLD + utilities.OKGREEN + '*************** Create Tree Sub-Menu ***************' + utilities.ENDC)
                print(utilities.OKBLUE + '1) Create tree with user input')
                print('2) Create tree with imported data from a file')
                print('0) Return to main menu' + utilities.ENDC)
                subMenuItem = input(utilities.OKGREEN + 'Choose one of items (0, 1, or 2): ' + utilities.ENDC)
                if subMenuItem == '0':
                    break
                elif subMenuItem == '1':
                    if mt.root != None:
                        yn = ''
                        while True:
                            yn = input(utilities.WARNING + 'Warning: Tree has already been created. Do you want to recreate it? (y/n): ' + utilities.ENDC)
                            if yn == 'y' or yn == 'n' or yn == 'Y' or yn == 'N':
                                break
                        if yn =='y' or yn == 'Y':
                            createTreeWithUserInput(mt)
                            print(utilities.OKBLUE + '>>> The tree has been recreated successfully...' + utilities.ENDC)
                    else:
                        createTreeWithUserInput(mt)
                        print(utilities.OKBLUE + '>>> The tree has been created successfully...' + utilities.ENDC)

                elif subMenuItem == '2':
                    if mt.root != None:
                        yn = ''
                        while True:
                            yn = input(utilities.WARNING + 'Warning: Tree has already been created. Do you want to recreate it? (y/n): ' + utilities.ENDC)
                            if yn == 'y' or yn == 'n' or yn == 'Y' or yn == 'N':
                                break
                        if yn =='y' or yn == 'Y':
                            createTreeFromFile(mt)
                            print(utilities.OKBLUE + '>>> The tree has been recreated successfully...' + utilities.ENDC)
                    else:
                        createTreeFromFile(mt)
                        print(utilities.OKBLUE + '>>> The tree has been created successfully...' + utilities.ENDC)

                else:
                    print(utilities.FAIL + '>>> Error: You are allowed to enter numbers (1 - 3) to choose sub menu items !!!' + utilities.ENDC)

        elif menuItem == '2': ### Adding new data block(s) to the tree
            while True:
                print(utilities.BOLD + utilities.OKGREEN + '*************** Add Data Block(s) to the Tree Sub-Menu ***************' + utilities.ENDC)
                print(utilities.OKBLUE + '1) Add a data block')
                print('2) Add batch data blocks with user input')
                print('3) Add batch data blocks with importing data from a file')
                print('0) Return to main menu' + utilities.ENDC)
                subMenuItem = input(utilities.OKGREEN + 'Choose one of items (0, 1, 2, or 3): ' + utilities.ENDC)
                if subMenuItem == '0':
                    break
                elif subMenuItem == '1':
                    addOneDataBlock(mt)
                elif subMenuItem == '2':
                    addManyDataBlocksToTree(mt)
                elif subMenuItem == '3':
                    addManyDataBlocksToTreeFromFile(mt)
                else:
                    print(utilities.FAIL + '>>> Error: You are allowed to enter numbers (1 - 4) to choose sub menu items !!!' + utilities.ENDC)
        
        ###################### Show information of an specific path in the tree ######################
        elif menuItem == '3': 
            if mt.root == None:
                print(utilities.FAIL + '>>> Error: The tree has not beet created yet !!!')
                print('>>> Please create tree first.' + utilities.ENDC)
            else:
                numberOfDataBlocks = len(mt.getDataBlocks())
                strPathIndex = '-'
                while strPathIndex != '-1':
                    strPathIndex = input(utilities.OKGREEN + 'Enter path index (0 - ' + str(numberOfDataBlocks - 1) + ') to show or enter (-1) to return main menu: ' + utilities.ENDC)
                    pathIndex = int(strPathIndex)
                    layerIndex, leafIndex = mt.getDataIndices(pathIndex)
                    if layerIndex == -1 or leafIndex == -1:
                        print(utilities.FAIL + '>>> Error: Given path index (' + strPathIndex + ') is out of range !!!')
                        print('>>> There is/are (' + str(numberOfDataBlocks) + ') data block(s) in the tree. You can enter number between (0 - ' + str(numberOfDataBlocks - 1) + ').' + utilities.ENDC)
                    else:
                        print(utilities.OKBLUE + '>>> Show path chain...' + utilities.ENDC)
                        mt.printPath(layerIndex, leafIndex)
                        break
        
        ###################### Graph Tree ######################
        elif menuItem == '4': 
            utilities.graphTree(mt, 'Display MHT Graph')
        
        ###################### Proof of a path ######################
        elif menuItem == '5':
            if mt.root == None:
                print(utilities.FAIL + '>>> Error: The tree has not beet created yet !!!')
                print('>>> Please create tree first.' + utilities.ENDC)
            elif len(mt.getDataBlocks()) <= 1:
                print(utilities.FAIL + '>>> Error: The tree has only one node !!!')
                print('>>> Proof of path needs at least two nodes.' + utilities.ENDC)
            else:
                numberOfDataBlocks = len(mt.getDataBlocks())
                strPathIndex = '-'
                while strPathIndex != '0':
                    strPathIndex = input(utilities.OKGREEN + 'Enter path index (1 - ' + str(numberOfDataBlocks) + ') to show or enter (0) to return main menu: ' + utilities.ENDC)
                    if strPathIndex == '0': break
                    pathIndex = int(strPathIndex) - 1
                    layerIndex, leafIndex = mt.getDataIndices(pathIndex)
                    if layerIndex == -1 or leafIndex == -1:
                        print(utilities.FAIL + '>>> Error: Given path index (' + strPathIndex + ') is out of range !!!')
                        print('>>> There is/are (' + str(numberOfDataBlocks) + ') data block(s) in the tree. You can enter number between (1 - ' + str(numberOfDataBlocks) + ').' + utilities.ENDC)
                    else:
                        break
                
                print(utilities.OKBLUE + '>>> Proving leaf node (' + mt.lstDataBlocks[layerIndex][leafIndex] + ')...' + utilities.ENDC)
                lstProofPathChain = prover.proofPath(mt, layerIndex, leafIndex)
                lstVerifiedPathChain, proved = verifier.verifyPath(mt, layerIndex, leafIndex, lstProofPathChain)

                #lstProofOfPath, proved = mt.proofOfPath(layerIndex, leafIndex)
                i = 0
                for item in lstVerifiedPathChain:
                    i += 1
                    print(i, ')', str(item))
                
                if proved:
                    print(utilities.BOLD + utilities.WARNING + '>>> Path chain has been proved...' + utilities.ENDC)
                else:
                    print(utilities.BOLD + utilities.WARNING + '>>> Path chain has NOT been proved !!!' + utilities.ENDC)

                utilities.graphTree(mt, 'Proof Of Path Index ' + strPathIndex, lstVerifiedPathChain)
        ###################### Proof of consistency ######################
        elif menuItem == '6': 
            if mt.root == None:
                print(utilities.FAIL + '>>> Error: The tree has not beet created yet !!!')
                print('>>> Please create tree first.' + utilities.ENDC)
            else:
                numberOfDataBlocks = len(mt.getDataBlocks())
                strPathIndex = '-'
                while strPathIndex != '0':
                    strPathIndex = input(utilities.OKGREEN + 'Enter path index (1 - ' + str(numberOfDataBlocks) + ') to show or enter (0) to return main menu: ' + utilities.ENDC)
                    if strPathIndex == '0': break
                    pathIndex = int(strPathIndex) - 1
                    layerIndex, leafIndex = mt.getDataIndices(pathIndex)
                    if layerIndex == -1 or leafIndex == -1:
                        print(utilities.FAIL + '>>> Error: Given path index (' + strPathIndex + ') is out of range !!!')
                        print('>>> There is/are (' + str(numberOfDataBlocks) + ') data block(s) in the tree. You can enter number between ( - ' + str(numberOfDataBlocks) + ').' + utilities.ENDC)
                    else:
                        print(utilities.OKBLUE + '>>> Consistency Proof List...' + utilities.ENDC)
                        lstConsistencyProof = prover.proofConsistency(mt, pathIndex + 1, 0, numberOfDataBlocks, True)
                        verified = verifier.verifyConsistency(mt, lstConsistencyProof, lstConsistencyProof)

                        lstNodes = utilities.getListColumn(lstConsistencyProof, 0)
                        lstLevels = utilities.getListColumn(lstConsistencyProof, 1)
                        for r in lstConsistencyProof:
                            print(lstConsistencyProof.index(r) + 1, ')', str(r[0]), ', Level:', r[1])
                        utilities.graphTree(mt, 'Consistency Proof (Leaf Index = '+ strPathIndex + ')', lstNodes)
                        print(utilities.OKBLUE + '>>> Verifying consistency Proof List...' + utilities.ENDC)
                        break
        ###################### About the project ######################
        elif menuItem == '7':
            aboutUs()
    
    return 0
            
    #print('Guaranteed:\n{}\n'.format(', '.join(sorted(hashlib.algorithms_guaranteed))))
    #print('Available:\n{}'.format(', '.join(sorted(hashlib.algorithms_available))))

if __name__ == '__main__':
    main(sys.argv)
    exit(0)
