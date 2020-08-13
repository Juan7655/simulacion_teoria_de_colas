import numpy as np
import pandas as pd

from src import cluster


class Manager:
    system_set = False

    def run(self, server, n, periods=1, show_graph=False):
        if not self.system_set:
            self.setup()
        self.input_size = n  # set number of raw input material
        wq, ws = [], []
        for i in range(periods):  # number of runs for the specified server
            wq_val, ws_val = self.servers[server].get_result(i, show_graph)
            wq.append(wq_val)
            ws.append(ws_val)
        delays = pd.DataFrame(np.array([wq, ws]).T, columns=['wq', 'ws'])
        delays.to_csv('files/esperas_finales.csv')

    def setup(self):
        m_x = pd.read_csv("files/input.csv")  # read input configurations
        self.servers = []
        for index, server in m_x.iterrows():  # iterate over servers in configuration matrix
            inputs = server['inputs']
            inputs = float('nan') if type(inputs) == float else inputs.split(',')
            fun = eval("lambda x: " + server['funcion'])  # create lambda expression from configuration value
            process_count = server['procesos']
            acceptance = 1.0 - server['rechazo']
            rejection_fun = eval("lambda x: " + server['funcion_rechazo'])
            inputs = None if type(inputs) == float else list(map(int, inputs))  # convert inputs to int list
            if index in {12, 15}:  # assembly clusters
                self.servers.append(cluster.Assembly(index, inputs, fun, process_count, acceptance, rejection_fun, self))
            else:  # other normal clusters
                self.servers.append(cluster.Cluster(index, inputs, fun, process_count, acceptance, rejection_fun, self))
        self.system_set = True

    def get_server(self, id):
        if not self.system_set:
            self.setup()
        return self.servers[id]

    def get_server_index_list(self):
        if not self.system_set:
            self.setup()
        return [i.index for i in self.servers]
