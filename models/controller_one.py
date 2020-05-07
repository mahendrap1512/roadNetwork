from datetime import datetime
from multiprocessing import Process, Queue, Pipe
from camera_one import fun


def controller_1(child):
    pass


if __name__ == '__main__':
    parent_conn1, child_conn1 = Pipe()
    p1 = Process(target=fun, args=(child_conn1,))
    p1.start()
    parent_conn2, child_conn2 = Pipe()
    p2 = Process(target=fun, args=(child_conn2,))
    p2.start()
    start_time = datetime.now()
    while True:
        print(parent_conn1.recv())
        vehicles_1 = parent_conn1.recv()
        vehicles_2 = parent_conn2.recv()
        curr_time = datetime.now()
        if (curr_time - start_time).seconds % 300 == 0:
            pass
