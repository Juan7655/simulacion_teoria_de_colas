from Servidor import Servidor
import pandas as pd
import numpy as np

class Cluster(Servidor):
    def __init__(self,  index, inputs, fun,  n, acceptance,   manager):
        Servidor.__init__(self,  index, inputs, fun, manager)
        self.acceptance = acceptance
        self.fun2 = lambda x: x * (4.0 - 2.0) + 2.0
        self.n = n
    
    def get_output(self):
        data = self.get_input_val()
        data = pd.DataFrame(data if data is not None else np.zeros(self.manager.input_size),  columns=['hora_llegada'])
        data.insert(data.shape[1],  "reproceso", np.zeros(len(data)))
        
        inicio = [[0 for _ in range(len(data))] for i in range(self.n)]
        termina = [[0 for _ in range(len(data))] for i in range(self.n)]
        duracion = [[0 for _ in range(len(data))] for i in range(self.n)]
        termina_cluster = []
        termina_cluster_neto = []
        i = 0
        while i  < len(data):
            best_server = 0 if i == 0 else get_best_server([termina[j][i - 1] for j in range(self.n)])
            for j in range(self.n):
                if j == best_server:
                    inicio[j][i] = init = max(data['hora_llegada'][i],  0 if i == 0 else termina[j][i - 1])
                    duracion[j][i] = dur = (self.fun(np.random.rand()) if data['reproceso'][i] == 0 else self.fun2(np.random.rand()))
                    hora_fin = init + dur
                    termina[j][i] = hora_fin
                    termina_cluster_neto.append(hora_fin) 
                    if np.random.rand() <= self.acceptance:
                        termina_cluster.append(hora_fin) 
                    else:
                        index = data[i:][data[i:]['hora_llegada'] < hora_fin].index[-1]
                        data = pd.DataFrame(np.insert(data.values,  index,  values=[hora_fin, 1],  axis=0),  columns=data.columns)
                        for k in range(self.n):
                            inicio[k].append(0)
                            termina[k].append(0)
                            duracion[k].append(0)
                elif i != 0:
                    inicio[j][i] = inicio[j][i - 1]
                    termina[j][i] = termina[j][i - 1]
                    duracion[j][i] = duracion[j][i - 1]
            i += 1
        data.insert(data.shape[1],  "termina_servicio",  termina_cluster_neto)
        data['termina_servicio'] = data['termina_servicio'].astype('float64')
        cola = [0]
        for i in range(1,  len(data)):
            slice = pd.DataFrame(data['termina_servicio'][:i],  columns=[0])
            cola.append(sum([j > data['hora_llegada'][i] for j in slice[0]]))
        data.insert(data.shape[1],  "fila",  cola)
        self.data = data
        print("output for cluster {0}".format(self.index))
        return np.sort([int(i) for i in termina_cluster])

class Assembly(Cluster):
    def __init__(self,  index, inputs, fun,  n, acceptance,   manager):
        valid = {12,  15}
        if index not in valid:
            raise ValueError("AssemblyConstructor: Cluster must be one of %r." % valid)
        Cluster.__init__(self,  index, inputs, fun,  n, acceptance,   manager)

    def get_input_val(self):
        input_val = []
        if self.index == 15:
            input_val = np.sort(list(self.manager.get_server(self.inputs[0]).get_output().tolist()))
            return input_val[9::10]
        else:
            val = [[], [], [], []]
            for i in self.inputs:
                input_val.append(list(self.manager.get_server(i).get_output().tolist()))
            val[0] = input_val[0]
            val[3] = input_val[2]
            val[1] = input_val[1][::2]
            val[2] = input_val[1][1::2]
            return np.max(val,  axis=0)
        
            
def get_best_server(server_last):
    index = 0
    val = server_last[0]
    for i in range(1,  len(server_last)):
        if server_last[i] < val:
            val = server_last[i]
            index = i
    return index

