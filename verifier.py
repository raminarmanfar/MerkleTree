'''
Created on Dec 4, 2016

@author: Ramin
'''

from utilities import utilities

class verifier:
	lastProvedRootHash = None
	@staticmethod
	def verifyPath(mt, layerIndex, leafIndex, lstProofPathChain):
		lstVerifiedPathChain = []
		curNode = mt.lstLeaves[layerIndex][leafIndex]
		sibNode = mt.getSiblingNode(curNode)

		lstVerifiedPathChain.append(sibNode)
		for i in range(len(lstProofPathChain)):
			curNode = curNode.parentNode
			sibNode = mt.getSiblingNode(curNode)
			if str(curNode) != lstProofPathChain[i]:
				return [], False
			lstVerifiedPathChain.append(sibNode)
		return lstVerifiedPathChain, True

	@staticmethod
	def verifyConsistency(mt, lstProof, lstOrder):
		proved = False

		if proved == True:
			verifier.lastProvedRootHash = str(mt.root)
		return proved