import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Servidor:
    def __init__(self,  index, inputs, fun,  manager):
        self.index = index
        self.inputs = inputs
        self.fun = fun
        self.manager = manager
        
    def get_output(self):
        data = self.get_input_val()
        data = pd.DataFrame(data if data is not None else np.zeros(self.manager.input_size),  columns=['hora_llegada'])
        aleatorios = np.random.rand(len(data['hora_llegada']) )
        vals = list(map(self.fun,  aleatorios))
        data.insert(data.shape[1],  "duracion_servicio",  vals)
        inicio_servicio = []
        termina_servicio = []
        for i in range(len(data)):
            inicio_servicio.append(data["hora_llegada"][0] if i == 0 else max(data["hora_llegada"][i],  termina_servicio[i - 1]))
            termina_servicio.append(inicio_servicio[i] + data["duracion_servicio"][i])
        data.insert(data.shape[1],  "inicia_servicio",  inicio_servicio)
        data.insert(data.shape[1],  "termina_servicio",  termina_servicio)
        data.insert(data.shape[1],  "tiempo_espera",  data["termina_servicio"] - data["inicia_servicio"])
        largo_fila = [0]
        for i in range(1,  len(data)):
            slice = pd.DataFrame(data['termina_servicio'][:i],  columns=[0])
            largo_fila.append(sum([j > data['hora_llegada'][i] for j in slice[0]]))
        data.insert(data.shape[1],  "fila",  largo_fila)
        self.data = data
        print("output for server {0}".format(self.index))
        return data['termina_servicio'].astype('float64')
        
    def get_result(self):
        self.get_output()
        for i in self.data.columns:
            self.data[i] = self.data[i].astype('float64')
        self.data.to_csv('files/final_output.csv')
        plt.step(self.data['hora_llegada'],  self.data['fila'])
        plt.xlabel("Servidor " + str(self.index))
        plt.ylabel("Clientes en cola")
        plt.show()
        return "Done."
    
    def get_input_val(self):
        if self.inputs is None:
            return None
        input_val = []
        for i in self.inputs:
            input_val += list(self.manager.get_server(i).get_output().tolist())
        return np.sort(input_val)
