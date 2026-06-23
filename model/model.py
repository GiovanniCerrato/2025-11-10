from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMapOrder = {}

    def buildGraph(self,store_id,k):
        self._graph.clear()
        print(self._graph)
        self._addNodes(store_id)
        print(self._graph)
        self._addEdges(store_id,k,self._idMapOrder)
        print(self._graph)

    def _addNodes(self,store_id):
        allNodes = DAO.getAllNodes(store_id)
        for n in allNodes:
            self._idMapOrder[n.order_id] = n
        self._graph.add_nodes_from(allNodes)
        return

    def _addEdges(self,store_id,k,idMapOrder):
        allEdges = DAO.getAllEdges(store_id,k,idMapOrder)
        for e in allEdges:
            self._graph.add_edge(e.o1,e.o2,weight=e.weight)
        return

    def getNumNodiArchi(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def topFive(self):
        listaArchi = list(self._graph.edges(data = True))
        listaArchi.sort(key=lambda x:x[2]["weight"],reverse=True)
        return listaArchi[:5]

    def getPercorsoMax(self,order_id):
        pathMax = list(nx.dfs_edges(self._graph,self._idMapOrder[order_id]))
        print(len(pathMax))
        print(*(f"{v}" for u,v in pathMax))

    def getAllStores(self):
        return DAO.getAllStores()

    def getAllNodes(self):
        return list(self._graph.nodes())

