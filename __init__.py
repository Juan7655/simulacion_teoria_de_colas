import Servidor
import math
import pprint


def run():
    wiiiiiiiiiiuuuuuuuuuuwwwiiiiiiiiiiiu()
    cincomasseis()

def wiiiiiiiiiiuuuuuuuuuuwwwiiiiiiiiiiiu():
    NServ = 14
    ListSrv = []
    for NServ in range(NServ):
        tempServ = Servidor.Servidor(NServ, 1)
        ListSrv.append(tempServ)
        print(NServ)
    ListSrv[13].set_inputs(ListSrv[12])
    ListSrv[12].set_inputs(ListSrv[11])
    ListSrv[11].set_inputs(ListSrv[10])
    ListSrv[10].set_inputs(ListSrv[9])
    ListSrv[9].set_inputs(ListSrv[6:9])
    ListSrv[6].set_inputs(ListSrv[3])
    ListSrv[3].set_inputs(ListSrv[0])
    ListSrv[7].set_inputs(ListSrv[4])
    ListSrv[4].set_inputs(ListSrv[1])
    ListSrv[8].set_inputs(ListSrv[5])
    ListSrv[5].set_inputs(ListSrv[2])

    print(NServ)
    

if __name__ == '__main__':
    run()
