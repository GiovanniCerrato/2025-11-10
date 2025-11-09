import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceDDStore = None

    def fillDDStore(self):
        stores = self._model.getStores()
        for store in stores:
            self._view._ddStore.options.append(ft.dropdown.Option(
                data=store, text=store.store_name, on_click=self._pickDDStore))
        self._view.update_page()

    def handleCreaGrafo(self, e):
        k = self._view._txtIntK.value
        kint = int(k)
        self._model.buildGraph(self._choiceDDStore, kint)

        allNodes = self._model.getAllNodes()
        self.fillDD(allNodes)
        self._view._ddNode.disabled = False
        self._view._btnCerca.disabled = False
        self._view._btnRicorsione.disabled = False

        Nnodes, Nedges = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi:{Nnodes}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi:{Nedges}"))

        top_five_edges = self._model.getSortedEdges()
        self._view.txt_result.controls.append(ft.Text("5 Archi di peso maggiore:"))

        for source,target, peso in top_five_edges:
            self._view.txt_result.controls.append(ft.Text((f"Arco: {source} -> {target} - Peso: {peso["weight"]}")))
        self._view.update_page()

    def handleCerca(self, e):
        if self._view._ddNode.value is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Selezionare nodo di partenza."))
            self._view.update_page()
            return
        nodes = self._model.getCammino(self._view._ddNode.value)

        self._view.txt_result.controls.append(ft.Text(f"Nodo di partenza : {self._view._ddNode.value}"))
        for n in nodes:
            self._view.txt_result.controls.append(ft.Text(n))
        self._view.update_page()

    def handleRicorsione(self, e):
        bestpath, bestscore = self._model.getBestPath(self._view._ddNode.value)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Trovato un cammino che parte da {self._view._ddNode.value} "
                    f"con somma dei pesi uguale a {bestscore}."))

        print(bestpath)
        for v in bestpath:
            self._view.txt_result.controls.append(ft.Text(f"{v}"))
        self._view.update_page()

    def fillDD(self, allNodes):
        self._view._ddNode.options.clear()
        for n in allNodes:
            self._view._ddNode.options.append(
                ft.dropdown.Option(n))

    def _pickDDStore(self, e):
        if e.control.data is None:
            self._choiceDDStore = None
        else:
            self._choiceDDStore = e.control.data