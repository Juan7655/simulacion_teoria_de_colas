import pandas as pd
import numpy as np

import Servidor
import Cluster


class Manager:
    system_set = False
    def run(self, server,  n,  ciclos=1,  show_graph=False):
        if not self.system_set:
            self.setup()
        self.input_size = n # set number of raw input material
        wq,  ws = [], []
        for i in range(ciclos): # number of runs for the specified server
            wq_val,  ws_val = self.servers[server].get_result(i,  show_graph)
            wq.append(wq_val)
            ws.append(ws_val)
        lista = np.array([wq,  ws]).T
        esperas = pd.DataFrame(lista,  columns=['wq','ws'])
        esperas.to_csv('files/esperas_finales.csv')
    
    def setup(self):
        m_x = pd.read_csv("files/input.csv")  # read input configurations
        self.servers = []
        for index,  server in m_x.iterrows(): # iterate over servers in configuration matrix
            inputs = server['inputs']
            inputs = float('nan') if type(inputs) == float else inputs.split(',')
            fun = eval("lambda x: " + server['funcion']) # create lambda expression from configuration value
            num_procesos = server['procesos']
            acceptance = 1.0 - server['rechazo']
            fun_rechazo = eval("lambda x: " + server['funcion_rechazo'])
            inputs = None if type(inputs) == float else map(int,  inputs) # convert inputs to int list
            if index in {12,  15}: # assembly clusters
                self.servers.append(Cluster.Assembly(index,  inputs,  fun,  num_procesos, acceptance,  fun_rechazo, self))
            else: # other normal clusters
                self.servers.append(Cluster.Cluster(index,  inputs,  fun,  num_procesos, acceptance,  fun_rechazo, self))
        self.system_set = True
    
    def get_server(self,  id):
        if not self.system_set:
            self.setup()
        return self.servers[id]
    
    def get_server_index_list(self):
        if not self.system_set:
            self.setup()
        lista = [i.index for i in self.servers]
        return list(lista)
