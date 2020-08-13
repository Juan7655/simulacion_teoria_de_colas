import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb


class Server:
    def __init__(self, index, inputs, fun, manager):
        self.index = index
        self.inputs = inputs
        self.fun = fun
        self.manager = manager

    def get_output(self):
        data = self.get_input_val()
        data = pd.DataFrame(data if data is not None else np.zeros(self.manager.input_size), columns=['hora_llegada'])
        span = self.fun(np.random.rand(len(data['hora_llegada'])))
        data.insert(data.shape[1], "duracion_servicio", span)
        service_start = []
        service_end = []
        for i in range(len(data)):
            service_start.append(
                data["hora_llegada"][0] if i == 0 else max(data["hora_llegada"][i], service_end[i - 1]))
            service_end.append(service_start[i] + data["duracion_servicio"][i])
        data.insert(data.shape[1], "inicia_servicio", service_start)
        data.insert(data.shape[1], "termina_servicio", service_end)
        data.insert(data.shape[1], "tiempo_espera", data["termina_servicio"] - data["inicia_servicio"])
        queue_len = [0]
        for i in range(1, len(data)):
            slice = pd.DataFrame(data['termina_servicio'][:i], columns=[0])
            queue_len.append(sum([j > data['hora_llegada'][i] for j in slice[0]]))
        data.insert(data.shape[1], "fila", queue_len)
        self.data = data
        print("output for server {0}".format(self.index))
        return data['termina_servicio'].astype('float64')

    def get_result(self, n=0, show_graph=False):
        self.get_output()
        for i in self.data.columns:
            self.data[i] = self.data[i].astype('float64')
        self.data.to_csv('files/final_output{0}.csv'.format(n))
        if show_graph:
            sb.pairplot(self.data)
            plt.show()
            self.data = self.data.sort_values(by=['hora_llegada'])
            plt.step(self.data['hora_llegada'], self.data['fila'])
            plt.xlabel("Servidor " + str(self.index))
            plt.ylabel("Clientes en cola")
            plt.show()
        return float(self.times[0]), float(self.times[1])

    # returns a list with input elements of the server, orderder by arrival time
    def get_input_val(self):
        if self.inputs is None:
            return None  # there are no inputs
        input_val = []
        for i in self.inputs:  # append the output of each connected server
            input_val += list(self.manager.get_server(i).get_output().tolist())
        return np.sort(input_val)
