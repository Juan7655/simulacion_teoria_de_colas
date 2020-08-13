import time
import matplotlib.pyplot as plt

from src import manager


def waiting_times(server, n, ciclos=1):
    start_time = time.time()
    man.run(server, n, ciclos)
    end_time = time.time() - start_time
    return end_time


def complexity(serv):
    time_diff = []
    max_input = 1000
    for i in range(100, max_input, 50):
        end_time = waiting_times(serv, i)
        time_diff.append(end_time)
        print(end_time)
    plt.plot([i for i in range(100, max_input, 50)], time_diff)
    plt.xlabel("Input size for server " + str(serv))
    plt.ylabel("Time (s)")
    plt.show()


def show_graphs(list_servers=None):
    input_size = 1000
    if list_servers is None:
        list_servers = man.get_server_index_list()
    if type(list_servers) == int:
        man.run(list_servers, input_size, show_graph=True)
    else:
        for i in list_servers:
            man.run(i, input_size, show_graph=True)


if __name__ == '__main__':
    man = manager.Manager()
    # man.run(13, 100, show_graph=True)
    ## para mostrar las graficas del comportamiento de la cola
    # show_graphs([3, 6, 9])  # muestra las graficas de los servidores que se pongan en la lista
    # show_graphs(9)  # si no se le ponen argumentos, muestra las graficas de todos los servidores
    show_graphs()  # si se quiere visualizar la grafica de un solo servidor, no se tiene que poner en lista, el numero solo funciona
    ## para medir los tiempos de ejecucion (complejidad computacional)
    # complexity(12)
    ## para medir el tiempo tardado en ejecutar una o varias corridas de un servidor
    # time = waiting_times(12, 100, ciclos=10)
    # print(time)
