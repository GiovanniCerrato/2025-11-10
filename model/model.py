import copy

import networkx as nx

from database.DAO import DAO
import networkx as nx
class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMap = {}


    def getBestPath(self, startStr):
        self._bestPath = []
        self._bestScore = 0

        start = self._idMap[int(startStr)]

        parziale = [start]

        vicini = self._graph.neighbors(start)
        for v in vicini:
            parziale.append(v)
            self._ricorsione(parziale)
            parziale.pop()

        return self._bestPath, self._bestScore
    def _ricorsione(self, parziale):
        if self.getScore(parziale) > self._bestScore:
            self._bestScore = self.getScore(parziale)
            self._bestPath = copy.deepcopy(parziale)

        for v in self._graph.neighbors(parziale[-1]):
            if (v not in parziale and #check if not in parziale
                    self._graph[parziale[-2]][parziale[-1]]["weight"] >
                    self._graph[parziale[-1]][v]["weight"]): #check if peso nuovo arco è minore del precedente
                parziale.append(v)
                self._ricorsione(parziale)
                parziale.pop()

    def buildGraph(self, store, k):
        self._graph.clear()
        self._orders = DAO.getAllOrdersbyStore(store)
        for o in self._orders:
            self._idMap[o.order_id] = o

        self._graph.add_nodes_from(self._orders)

        allEdges = DAO.getEdges(store, k, self._idMap)
        for e in allEdges:
                self._graph.add_edge(e[0], e[1], weight=e[2])

    def getSortedEdges(self):
        sorted_edges = sorted(self._graph.edges(data=True), key=lambda x: x[2]["weight"], reverse=True)

        top_five_edges = sorted_edges[:5]
        return top_five_edges

    def getCammino(self, sourceStr):
        source = self._idMap[int(sourceStr)]
        lp = []

        #for source in self._graph.nodes:
        tree = nx.dfs_tree(self._graph, source)
        nodi = list(tree.nodes())

        for node in nodi:
            tmp = [node]

            while tmp[0] != source:
                pred = nx.predecessor(tree, source, tmp[0])
                tmp.insert(0, pred[0])

            if len(tmp) > len(lp):
                lp = copy.deepcopy(tmp)

        return lp

    def getScore(self, listOfNodes):
        tot = 0
        for i in range(len(listOfNodes) - 1):
            tot += self._graph[listOfNodes[i]][listOfNodes[i + 1]]["weight"]

        return tot
    def getStores(self):
        return DAO.getAllStores()
    def getAllNodes(self):
        nodes = list(self._graph.nodes)
        return nodes
    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()
