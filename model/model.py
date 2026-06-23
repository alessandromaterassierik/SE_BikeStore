import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):
        self.categories = ''
        self.products = ''
        self.G = nx.DiGraph()

    def get_date_range(self):
        return DAO.get_date_range()

    def get_categories(self):
        categories = DAO.load_categories()
        self.categories = [y['category_name'] for y in categories]

    def get_products(self, cat, start, end):    #[(24, 'Electra Townie Original 21D - 2016'), (25, 'Electra Townie Original 7D - 2015/2016'),
        products = DAO.load_products(cat, start, end)
        self.products = [(p['id1'], p['name1'], p['tot1'] ,p['id2'],p['name2'], p['tot2']) for p in products]

    def build_graph(self, cat, start, end):
        self.get_products(cat, start, end)
        for p in self.products:
            if p[2] > p[5]:
                self.G.add_node(p[0], name=p[1])
                self.G.add_node(p[3], name=p[4])
                self.G.add_weighted_edges_from([(p[0], p[3], p[2])])
            elif p[2] == p[5]:
                self.G.add_node(p[0], name=p[1])
                self.G.add_node(p[3], name=p[4])
                self.G.add_weighted_edges_from([(p[0], p[3], p[2])])
                self.G.add_weighted_edges_from([(p[3], p[0], p[5])])
            else:
                self.G.add_node(p[0], name=p[1])
                self.G.add_node(p[3], name=p[4])
                self.G.add_weighted_edges_from([(p[3], p[0], p[5])])

    def ricerca_cammino(self, len, prod_inz,prod_fin):
        self.sol_ott = []
        self.d_ott= 0
        self.ricorsione(n=prod_inz, sol_part=[prod_inz], d_cur=0, l = int(len), n_f= prod_fin)
        return self.sol_ott, self.d_ott

    def ricorsione(self, n, sol_part, d_cur, l, n_f):
        #update
        if d_cur > self.d_ott:
            self.sol_ott = sol_part.copy()
            self.d_ott = d_cur

        #end
        if len(self.sol_ott) == l:
            return

        #ciclo
        for n_i in self.G.neighbors(n):
            if n_i not in sol_part and self.vincoli(n, n_i, sol_part, l, n_f):
                if len(sol_part) == l-1:
                    d= self.G[n_i][n_f]['weight']
                    sol_part.append(n_f)
                    self.ricorsione(n_i, sol_part, d_cur + d, l, n_f)
                    sol_part.pop()
                else:
                    d= self.G[n][n_i]['weight']
                    sol_part.append(n_i)
                    self.ricorsione(n_i, sol_part, d_cur+d, l, n_f)
                    sol_part.pop()

    def vincoli(self,n, n_i, sol_part, l, n_f):
        if len(sol_part) ==1:
            return True
        if len(sol_part) == l-1:
            if self.G.has_edge(sol_part[-1],n_f): return True
            else: return
        if self.G.has_edge(sol_part[-1],n_i) and len(sol_part) <l-1:
            return True
        else: return



