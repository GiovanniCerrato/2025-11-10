import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._store = None
        self._node = None


    def handleCreaGrafo(self, e):
        k = 0
        k = self._view._txtIntK.value
        try:
            k = int(k)
        except ValueError:
            self._view.txt_result.clean()
            self._view.txt_result.controls.append(ft.Text("Digitare un valore intero!"))
            self._view.update_page()
            return
        if self._store is None or k<=0:
            self._view.txt_result.clean()
            self._view.txt_result.controls.append(ft.Text("Selezionare uno store valido e un numero di giorni maggiore di zero!"))
            self._view.update_page()
            return
        self._model.buildGraph(self._store.store_id,k)
        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:", color="red"))
        nNodi, nArchi = self._model.getNumNodiArchi()
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {nNodi}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {nArchi}"))
        self._view._btnCerca.disabled = False
        topFive = self._model.topFive()
        self._view.txt_result.controls.append(ft.Text("5 archi di peso maggiore:", color="red"))
        for a in topFive:
            self._view.txt_result.controls.append(ft.Text(f"Arco:{a[0]} -> {a[1]} - peso: {a[2]["weight"]}"))
        self.fillDDNode()
        self._view.update_page()
        return

    def handleCerca(self, e):
        if self._node is None:
            self._view.txt_result.clean()
            self._view.txt_result.controls.append(ft.Text("Selezionare un nodo"))
            self._view.update_page()
            return

        self._view.txt_result.clean()
        lp = self._model.getPercorsoMax(self._node.order_id)
        self._view.txt_result.controls.append(ft.Text(f"Nodo di partenza: {self._node}"))
        for n in lp:
            self._view.txt_result.controls.append(ft.Text(f"{n}"))

        self._view.update_page()
        return



    def handleRicorsione(self, e):
        pass

    def fillDDNode(self):
        self._view._ddNode.options.clear()
        allNodes = self._model.getAllNodes()
        self._view._ddNode.disabled = False
        for n in allNodes:
            self._view._ddNode.options.append(ft.dropdown.Option(key=n.order_id, data=n, on_click=self._handleNode))
        self._view.update_page()
        return

    def _handleNode(self, e):
        self._node = e.control.data
        print(self._node, type(self._node))
        return


    def fillDDStore(self):
        allStores = self._model.getAllStores()
        for s in allStores:
            self._view._ddStore.options.append(ft.dropdown.Option(key=s.store_name, data=s,on_click=self._handleStore))
        self._view.update_page()
        return

    def _handleStore(self,e):
        self._store = e.control.data
        print(self._store)
        return
