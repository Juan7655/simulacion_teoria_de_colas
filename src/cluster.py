from src.server import Server
import pandas as pd
import numpy as np


class Cluster(Server):
    def __init__(self, index, inputs, fun, n, acceptance, fun_rechazo, manager):
        Server.__init__(self, index, inputs, fun, manager)
        self.acceptance = acceptance
        self.fun2 = fun_rechazo
        self.n = n

    def get_output(self):
        data = self.get_input_val()
        data = pd.DataFrame(data if data is not None else np.zeros(self.manager.input_size), columns=['hora_llegada'])
        data.insert(data.shape[1], "reproceso", np.zeros(len(data)))

        start = [[0 for _ in range(len(data))] for i in range(self.n)]
        end = [[0 for _ in range(len(data))] for i in range(self.n)]
        span = [[0 for _ in range(len(data))] for i in range(self.n)]
        cluster_finish = []
        net_cluster_finish = []
        wq, ws = 0, 0
        i = 0
        while i < len(data):
            best_server = 0 if i == 0 else get_best_server([end[j][i - 1] for j in range(self.n)])
            for j in range(self.n):
                if j == best_server:
                    start[j][i] = init = max(data['hora_llegada'][i], 0 if i == 0 else end[j][i - 1])
                    span[j][i] = dur = self.fun(np.random.rand()) if data['reproceso'][i] == 0 else self.fun2(
                        np.random.rand())
                    time_end = init + dur
                    ws += time_end - data['hora_llegada'][i]
                    wq += init - data['hora_llegada'][i]
                    end[j][i] = time_end
                    net_cluster_finish.append(time_end)
                    if np.random.rand() <= self.acceptance:
                        cluster_finish.append(time_end)
                    else:
                        index = data[i:][data[i:]['hora_llegada'] < time_end].index[-1]
                        data = pd.DataFrame(
                            data=np.insert(data.values, index, values=[time_end, 1], axis=0),
                            columns=data.columns
                        )
                        for k in range(self.n):
                            start[k].append(0)
                            end[k].append(0)
                            span[k].append(0)
                elif i != 0:
                    start[j][i] = start[j][i - 1]
                    end[j][i] = end[j][i - 1]
                    span[j][i] = span[j][i - 1]
            i += 1
        data.insert(data.shape[1], "termina_servicio", net_cluster_finish)
        data['termina_servicio'] = data['termina_servicio'].astype('float64')
        queue = [0]
        for i in range(1, len(data)):
            slice = pd.DataFrame(data['termina_servicio'][:i])
            queue.append(sum([j > data['hora_llegada'][i] for j in slice['termina_servicio']]))
        data.insert(data.shape[1], "fila", queue)

        self.data = data
        self.times = [wq, ws]
        return np.sort([int(i) for i in cluster_finish])


class Assembly(Cluster):
    def __init__(self, index, inputs, fun, n, acceptance, rejected_fun, manager):
        if index not in {12, 15}:
            raise ValueError("AssemblyConstructor: Cluster must be 12 or 15.")
        Cluster.__init__(self, index, inputs, fun, n, acceptance, rejected_fun, manager)

    def get_input_val(self):
        input_val = []
        if self.index == 15:
            input_val = np.sort(list(self.manager.get_server(self.inputs[0]).get_output().tolist()))
            return input_val[9::10]
        else:
            val = [[], [], [], []]
            inps = list(self.inputs).copy()
            for i in self.inputs:
                input_val.append(list(self.manager.get_server(i).get_output().tolist()))
            val[0] = input_val[0]  # pieza A
            val[3] = input_val[2]  # pieza C
            val[1] = input_val[1][::2]  # primera pieza B
            val[2] = input_val[1][1::2]  # segunda pieza B
            return np.max(val, axis=0)  # returns list with maximum time values for each ensemble


# receives a list of values and returns the id of the server with minimum value
def get_best_server(server_last):
    return min(enumerate(server_last), key=lambda x: x[1])[0]
