import pandas
import matplotlib.pyplot as plt
import Server
import numpy as np

tiempo_llegadas = "Tiempo entre llegadas"
duracion_servicio = "Duracion servicio"
momento_llegada = "Momento de llegada"
inicia_servicio = "Inicia servicio"
termina_servicio = "Termina servicio"
tiempo_sistema = "Tiempo en el sistema"
tiempo_espera = "Tiempo en espera"
clientes_cola = "Clientes en cola"


clients = 500
servers = 5


def run():
	client_generator = Server.Server(lambda x: -2 * np.log(1 - x))
	service_time = [Server.Server(lambda x: x * (1.5 - 0.5) + 0.5),
	                Server.Server(lambda x: x * (2.5 - 2) + 2),
	                Server.Server(lambda x: x * (2.5 - 2) + 2),
	                Server.Server(lambda x: x * (2.5 - 2) + 2),
	                Server.Server(lambda x: x * (1.5 - 0.5) + 0.5),
	                Server.Server(lambda x: x*5)]
	mat = pandas.DataFrame({tiempo_llegadas: client_generator.get_list(clients),
	                        duracion_servicio + " 1": service_time[0].get_list(clients)})
	for i in range(servers):
		mat.insert(i + 2, duracion_servicio + " 2." + str(i + 1), service_time[i + 1].get_list(clients))

	mat = matriz_inicial(mat)
	x_val = [i for i in range(len(mat))]
	for i in range(servers):
		plt.step(x_val, mat[clientes_cola + " 2." + str(i + 1)], where='post', label=" Servidor 2." + str(i + 1))
	plt.legend()
	plt.show()


def matriz_inicial(mat):
	momento_llegada_list = []
	inicia_servicio_list = []
	termina_servicio_list = []
	clientes_cola_list = []

	inicia_servicio_list_2 = []
	termina_servicio_list_2 = []
	clientes_cola_list_2 = []
	first = True

	for _ in range(servers):
		inicia_servicio_list_2.append([])
		termina_servicio_list_2.append([])
		clientes_cola_list_2.append([])

	for i in range(len(mat[tiempo_llegadas])):
		momento_llegada_list.append(mat[tiempo_llegadas][i] + (0 if first else momento_llegada_list[i - 1]))
		inicia_servicio_list.append(max(momento_llegada_list[i], 0 if first else termina_servicio_list[i - 1]))
		termina_servicio_list.append(inicia_servicio_list[i] + mat[duracion_servicio + " 1"][i])

		for j in range(servers):
			if j == 0:
				inicia_servicio_list_2[j].append(0 if first else max(termina_servicio_list[i], termina_servicio_list_2[j][i - 1]))
				termina_servicio_list_2[j].append(inicia_servicio_list_2[j][i] + mat[duracion_servicio + " 2." + str(j + 1)][i])
			else:
				inicia_servicio_list_2[j].append(0 if first else max(termina_servicio_list_2[j - 1][i], termina_servicio_list_2[j][i - 1]))
				termina_servicio_list_2[j].append(inicia_servicio_list_2[j][i] + mat[duracion_servicio + " 2." + str(j + 1)][i])
		first = False
	for j in range(servers):
		mat.insert(1, inicia_servicio + " 2." + str(j + 1), inicia_servicio_list_2[j])
		mat.insert(1, termina_servicio + " 2." + str(j + 1), termina_servicio_list_2[j])

	mat.insert(1, momento_llegada, momento_llegada_list)
	mat.insert(1, inicia_servicio + " 1", inicia_servicio_list)
	mat.insert(1, termina_servicio + " 1", termina_servicio_list)
	mat.insert(1, tiempo_sistema, mat[termina_servicio + " 1"] - mat[momento_llegada])
	mat.insert(1, tiempo_espera, mat[inicia_servicio + " 1"] - mat[momento_llegada])

	# Generación de las listas de clientes en cada cola
	for i in range(len(mat)):
		temp = mat[termina_servicio + " 1"]
		temp = temp[:i]
		clientes_cola_list.append(len(temp[temp > mat[momento_llegada][i]]))

		for j in range(servers):
			temp = mat[termina_servicio + " 2." + str(j + 1)]
			temp = temp[:i]
			clientes_cola_list_2[j].append(len(temp[temp > mat[termina_servicio + " 1"][i]]))

	# inserción de los clientes en cada cola
	mat.insert(1, clientes_cola + " 1", clientes_cola_list)
	for i in range(servers):
		mat.insert(1, clientes_cola + " 2." + str(i + 1), clientes_cola_list_2[i])

	return mat[['Tiempo entre llegadas', 'Momento de llegada', 'Inicia servicio 1',
	            'Duracion servicio 1', 'Termina servicio 1', 'Tiempo en el sistema',
	            'Tiempo en espera', 'Clientes en cola 1', 'Inicia servicio 2.1',
	            'Duracion servicio 2.1', 'Termina servicio 2.1', 'Clientes en cola 2.1',
	            'Inicia servicio 2.2',
	            'Duracion servicio 2.2', 'Termina servicio 2.2', 'Clientes en cola 2.2',
	            'Inicia servicio 2.3',
	            'Duracion servicio 2.3', 'Termina servicio 2.3', 'Clientes en cola 2.3',
	            'Inicia servicio 2.4',
	            'Duracion servicio 2.4', 'Termina servicio 2.4', 'Clientes en cola 2.4',
	            'Inicia servicio 2.5',
	            'Duracion servicio 2.5', 'Termina servicio 2.5', 'Clientes en cola 2.5'
	            ]]


if __name__ == '__main__':
	run()
