class NFANode(object):
    def __init__(self, name=None, isFinal=0):
        self.name = name
        self.isFinal = isFinal
        self.edge = dict()
 
    def addEdge(self, alpha, target):
        if alpha not in self.edge:
            nextNodes = list()
            nextNodes.append(target)
            self.edge[alpha] = nextNodes
        else:
            if target not in self.edge[alpha]:
                self.edge[alpha].append(target)
 
 
class NFA(object):
 
    def __init__(self, terminators=None):
        self.terminators = terminators
        self.status = dict()
