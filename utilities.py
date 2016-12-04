'''
Created on Dec 4, 2016

@author: Ramin
'''

import os
from hashlib import sha256
hash_function = sha256

class utilities:
    '''
    HEADER = ''
    OKBLUE = ''
    OKGREEN = ''
    WARNING = ''
    FAIL = ''
    ENDC = ''
    BOLD = ''
    UNDERLINE = '\033[4m'
    '''

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ''''''

    @staticmethod
    def getHash(data):
        return hash_function(data).digest()

    @staticmethod
    def clearScreen():
        os.system('cls' if os.name == 'nt' else 'clear')
        
    @staticmethod
    def getScreenSize():
        ts = os.get_terminal_size()
        return ts
    
    @staticmethod
    def locatePrint(x, y, text, color = ENDC):
        sys.stdout.write(color + "\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text) + utilities.ENDC)
        sys.stdout.flush()

    @staticmethod
    def getDistinctColumn(matrix, i):
        lstResult = []
        for row in matrix:
            if len(row) > i and row[i] not in lstResult:
                lstResult.append(row[i])
        return lstResult
    
    @staticmethod
    def getListColumn(matrix, i):
        lstResult = []
        for row in matrix:
            lstResult.append(row[i])
        return lstResult

    @staticmethod
    def _getTreeAsList(mt):
        l = mt.lstLeaves[0][0]

        lstPaths = []
        for layer in mt.lstLeaves:
            for leaf in layer:
                lstLeafPath = mt._getPathFromRoot(leaf)
                lstPaths.append(lstLeafPath)

        listedTree = []
        for i in range(len(lstPaths[0]) - 1, -1, -1):
            listedTree.append(utilities.getDistinctColumn(lstPaths, i))
        
        del lstPaths

        h = 0
        while l != None:
            h += 1
            l = l.parentNode
        return h, listedTree

    @staticmethod
    def graphTree(mt, graphTitle, lstSpec = [], isUpperCase = False):
        height, listedTree = utilities._getTreeAsList(mt)
        lstOutData = []
        lstOutType = []
        lashesCount = 3
        levelCounter = 1
                
        #lstDatablocks = mt.getDataBlocks()
        dbIndex = 1
        
        for level in listedTree:
            '''
            ### data block info ###
            msg = ' ' * (lashesCount - 3 + 2)
            edges = ' ' * (lashesCount - 3 + 2)
            for node in level:
                if node.leftChild == None:
                    tmp = 'd' + str(dbIndex)
                    dbIndex += 1
                    msg += tmp
                    edges += '|'
                    if level.index(node) + 1 < len(level):
                        msg += ' ' * (len(tmp) + 6)
                        edges += ' ' * 9
        
                    if isUpperCase == True:
                        lstOutData.insert(0, msg.upper())
                    else: 
                        lstOutData.insert(0, msg)
                    lstOutType.insert(0, 'Node')

                    lstOutData.insert(0, edges)
                    lstOutType.insert(0, 'Edge')
            '''
            #### Nodes ###
            msg = ' ' * (lashesCount - 3)
            for node in level:
                if node in lstSpec:
                    msg += str(node)[0:5] + '<<<'
                    if level.index(node) + 1 < len(level):
                        msg += ' ' * (2 * lashesCount - 1 - 3)
                else:
                    msg += str(node)[0:5]
                    if level.index(node) + 1 < len(level):
                        msg += ' ' * (2 * lashesCount - 1)

            if isUpperCase == True:
                lstOutData.insert(0, msg.upper())
            else:
                lstOutData.insert(0, msg)
            lstOutType.insert(0, 'Node')
            #### edges ###
            if level[0] == mt.root: break
            discount = 0
            for i in range(lashesCount):
                msg = ' ' * (lashesCount + i - 1)
                for nodeIndex in range(len(level)):
                    if nodeIndex % 2 == 0: 
                        msg += '/'
                        if nodeIndex + 1 < len(level):
                            msg += ' ' * (2 * (lashesCount + 1) + 1 - discount)
                    else: 
                        msg += '\\'
                        if nodeIndex + 1 < len(level):
                            msg += ' ' * (2 * (lashesCount + 1) + 1 + discount)
                discount += 2
                    
                lstOutData.insert(0, msg)
                lstOutType.insert(0, 'Edge')

            levelCounter += 1
            lashesCount = 2 * (lashesCount + 1)
        
        ### show in console ### 
        i = 0
        for row in lstOutData:
            if lstOutType[i] == 'Node':
                print(utilities.WARNING + row + utilities.ENDC)
            else:
                print(utilities.OKGREEN + row + utilities.ENDC)
            i += 1
        print(utilities.ENDC)
        print(utilities.OKGREEN + 'Tree graphed successfully...' + utilities.ENDC)
        
        ### generate .html output file (export tree in an .html file) ###
        yn = ''
        while True:
            yn = input(utilities.WARNING + 'Do you want to save the graph of in file (y/n)?' + utilities.ENDC)
            if yn == 'y' or yn == 'n' or yn == 'Y' or yn == 'N': break
        
        if yn == 'y' or yn == 'Y':
            fn = input(utilities.WARNING + 'Enter output file name: ' + utilities.ENDC)
            fptr = open(fn, 'w')
            for row in lstOutData:
                fptr.write(row + '\n')
            fptr.close()
            fptr = open(fn + '.html', 'w')

            fptr.write('<!DOCTYPE html>\n<html>\n')
            fptr.write('<head>\n\t<title>' + graphTitle + '</title>\n</head>\n')
            fptr.write('<body>\n')
            fptr.write('<p>&nbsp;</p>\n')
            fptr.write('<p><b>Merkle Hash Tree Graph...</b></p>\n')
            fptr.write('<p><b>Graph Title: '+ graphTitle +'.</b></p>\n')
            fptr.write('<p>By Ramin Armanfar.</p>\n')
            fptr.write('<ul>\n')
            fptr.write('\t<li>Graph Source File Name: ' + fn + '</li>\n')
            fptr.write('\t<li> # of Leaf Nodes (data blocks): ' + str(len(mt.getDataBlocks())) + '</li>\n')
            fptr.write('\t<li> Tree Height: ' + str(height) + '</li>\n')
            fptr.write('</ul>\n')
            
            if len(lstSpec) > 0:
                fptr.write('<p><b>Resulted Items...</b></p>\n')
                fptr.write('<ul>\n')
                for item in lstSpec:
                    if isUpperCase == True:
                        fptr.write('\t<li>' + str(item).upper() + '</li>\n')
                    else:
                        fptr.write('\t<li>' + str(item) + '</li>\n')
                fptr.write('</ul>\n')
                
            fptr.write('<div id="list">\n')
            fptr.write('\t<p><iframe src="' + fn + '" frameborder="0" height="40000"\n')
            fptr.write('\twidth="10000%"></iframe></p>\n')                
            fptr.write('</div>\n')
            fptr.write('<p>&nbsp;</p>\n')
            fptr.write('</body>\n')
            fptr.write('</html>\n')
            fptr.close()

            print(utilities.OKGREEN + 'graph has been generated in files (' + utilities.WARNING + fn + ', ' + fn + '.html' + utilities.OKGREEN + ')' + utilities.ENDC + '\n')
        return lstOutData
