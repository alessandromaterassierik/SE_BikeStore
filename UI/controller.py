from UI.alert import AlertManager
from UI.view import View
from model.model import Model
import flet as ft
import datetime

class Controller:
    def __init__(self, view: View, model: Model, alert: AlertManager):
        self._view = view
        self._model = model
        self._alert = alert

    def set_dates(self):
        first, last = self._model.get_date_range()

        self._view.dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view.dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp2.current_date = datetime.date(last.year, last.month, last.day)

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """

        if self._view.dp1.value and self._view.dp2.value:
            cat = self._view.dd_category.value
            start= self._view.dp1.value
            end = self._view.dp2.value
            self._model.build_graph(cat, start, end)
            self._view.txt_risultato.controls.clear()
            self._view.txt_risultato.controls.append(ft.Text(f'Date selezionate:'))
            self._view.txt_risultato.controls.append(ft.Text(f'Start date: {start}'))
            self._view.txt_risultato.controls.append(ft.Text(f'End date: {end}'))
            self._view.txt_risultato.controls.append(ft.Text(f'Grafo correttamente creato:'))
            self._view.txt_risultato.controls.append(ft.Text(f'Numero di nodi:{len(self._model.G.nodes)}'))
            self._view.txt_risultato.controls.append(ft.Text(f'Numero di archi:{len(self._model.G.edges)}'))
            self._view.update()
            self.populate_dd_iniziale()
            self.populate_dd_finale()
        else:
            self._alert.show_alert(message="Non hai messo le date!!!")

    def handle_best_prodotti(self, e):
        """ Handler per gestire la ricerca dei prodotti migliori """
        self.populate_dd_iniziale()
        self.populate_dd_finale()
        n_weight = []
        for n in self._model.G.nodes:
            count_ext =0
            count_int=0
            for m in self._model.G.neighbors(n):
                if self._model.G.has_edge(n,m):
                    count_ext += self._model.G[n][m]['weight']
                elif self._model.G.has_edge(m,n):
                    count_int += self._model.G[m][n]['weight']
            n_weight.append((n, self._model.G.nodes[n]['name'],count_ext-count_int))

        n_weight.sort(key=lambda x: x[2], reverse=True)

        self._view.txt_risultato.controls.append(ft.Text(f'\n'))
        self._view.txt_risultato.controls.append(ft.Text(f'I cinque prodotti più venduti sono:'))
        for i in n_weight[0:5]:
            self._view.txt_risultato.controls.append(ft.Text(f'{i[1]} with score {i[2]}'))

        self._view.update()

    def handle_cerca_cammino(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        if not(self._view.txt_lunghezza_cammino.value and self._view.dd_prodotto_iniziale.value and self._view.dd_prodotto_finale.value):
            return
        else:
            prod_iniz_inp = int(self._view.dd_prodotto_finale.value)
            prod_fin_inp = int(self._view.dd_prodotto_finale.value)
            len =self._view.txt_lunghezza_cammino.value
            sol_ott , d_ott = self._model.ricerca_cammino(len, prod_iniz_inp,prod_fin_inp)

            self._view.txt_risultato.controls.clear()
            self._view.txt_risultato.controls.append(ft.Text(f'Cammino migliore:'))
            for i in sol_ott:
                self._view.txt_risultato.controls.append(
                        ft.Text(f'{self._model.G.nodes[i]["name"]}'))

            self._view.txt_risultato.controls.append(ft.Text(f'Score: {d_ott}'))
            self._view.update()


    def populate_dd_category(self):
        self._view.dd_category.options.clear()
        self._model.get_categories()
        for c in self._model.categories:
            self._view.dd_category.options.append(ft.dropdown.Option(key=c, text=c))
        self._view.update()

    def populate_dd_iniziale(self):
        self._view.dd_prodotto_iniziale.options.clear()
        for c in self._model.G.nodes:
            #attributo nodo
            txt = self._model.G.nodes[c]['name']
            self._view.dd_prodotto_iniziale.options.append(ft.dropdown.Option(key=c, text=txt))
        self._view.update()

    def populate_dd_finale(self):
        self._view.dd_prodotto_finale.options.clear()
        for c in self._model.G.nodes:
            txt = self._model.G.nodes[c]['name']
            self._view.dd_prodotto_finale.options.append(ft.dropdown.Option(key=c, text=txt))
        self._view.update()
