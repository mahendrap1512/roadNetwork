from multiprocessing import Process, Queue, Pipe
from controller_one import controller_1


if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p1 = Process(target=controller_1, args=(child_conn,))
    p.start()
    p2 = Process(target=controller_2, args=(child_conn_2,))