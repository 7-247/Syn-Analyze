class LRDFANode(object):
    def __init__(self, id):
        self.id = id
        self.itemSet = list()
 
    def addItemSetBySet(self, itemSet):
        for i in itemSet:
            if i not in self.itemSet:
                self.itemSet.append(i)
 