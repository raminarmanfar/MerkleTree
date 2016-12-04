'''
Created on Dec 4, 2016

@author: Ramin
'''
import math
from utilities import utilities

class prover:
	@staticmethod
	def proofPath(mt, layerIndex, leafIndex):
		lstProofPathChain = []

		curNode = mt.lstLeaves[layerIndex][leafIndex]
		# sibNode = self._getSiblingNode(curNode)
		# lstProofPathChain.append(sibNode)

		while curNode.nodeSide != 'Root':
			sibNode = mt.getSiblingNode(curNode)

			parHashVal = None
			if curNode.nodeSide == 'R':
				parHashVal = utilities.getHash(sibNode.data + curNode.data)
			elif curNode.nodeSide == 'L':
				parHashVal = utilities.getHash(curNode.data + sibNode.data)

			lstProofPathChain.append(str(parHashVal.hex()))
			curNode = curNode.parentNode

		return lstProofPathChain

	@staticmethod
	def _consistGetInfo(mt, k1, k2):
		if k1 + 1 == k2:
			layerIndex, leafIndex = mt.getDataIndices(k1)
			return (mt.lstLeaves[layerIndex][leafIndex], mt.getLevel(mt.lstLeaves[layerIndex][leafIndex]))
		else:
			layerIndexA, leafIndex = mt.getDataIndices(k1)
			leafA = mt.lstLeaves[layerIndexA][leafIndex]

			layerIndexB, leafIndex = mt.getDataIndices(k2 - 1)
			leafB = mt.lstLeaves[layerIndexB][leafIndex]

			commonParent = mt.getCommonParent(leafA, leafB)
		return (commonParent, mt.getLevel(commonParent))

	@staticmethod
	def proofConsistency(mt, m, k1, k2, b):
		if m == k2 - k1:
			if b == False:
				return [prover._consistGetInfo(mt, k1, k2)]
			return []
		else:
			t = math.log2(k2 - k1)
			if t.is_integer(): t = int(t) - 1
			else: t = int(t)
			k = 2 ** t

			if m <= k:
				return [prover._consistGetInfo(mt, k1 + k, k2)] + prover.proofConsistency(mt, m, k1, k1 + k, b)
			else:
				return [prover._consistGetInfo(mt, k1, k1 + k)] + prover.proofConsistency(mt, m - k, k1 + k, k2, False)

