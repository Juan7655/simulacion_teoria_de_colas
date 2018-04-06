import pandas as pd
import numpy as np
import Servidor
import Cluster


class Manager:
    input_size = 100
    def run(self):
        id = 1
        m_x = pd.read_csv("files/input.csv")
        self.servers = []
        for index,  server in m_x.iterrows():
            inputs = server['inputs']
            inputs = float('nan') if type(inputs) == float else inputs.split(',')
            fun = eval("lambda x: "+server['funcion'])
            num_procesos = server['procesos']
            acceptance = 1.0 - server['rechazo']
            inputs = None if type(inputs) == float else map(int,  inputs)
            if index in {12,  15}:
                self.servers.append(Cluster.Assembly(index,  inputs,  fun,  num_procesos, acceptance, self))
            else:
                self.servers.append(Cluster.Cluster(index,  inputs,  fun,  num_procesos, acceptance, self))
        print(len(self.servers))
        
#        for i in range(10, len(self.servers)):
#            print(self.servers[i].get_result())
        wq,  ws = [], []
        for i in range(40):
            wq_val,  ws_val = self.servers[11].get_result(i)
            wq.append(wq_val)
            ws.append(ws_val)
        lista = np.array([wq,  ws]).T[0]
        esperas = pd.DataFrame(lista,  columns=['wq','ws'])
        esperas.to_csv('files/esperas_finales.csv')
    
    def get_server(self,  id):
        return self.servers[id]

if __name__ == '__main__':
    man = Manager()
    man.run()
