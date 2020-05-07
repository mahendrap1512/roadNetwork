from datetime import datetime
from multiprocessing import Process, Queue, Pipe
from camera_two import fun
from trafficJamDetection import detect_jam
from deep_network import predict_clearance_time

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=fun, args=(child_conn,))
    p.start()
    start_time = datetime.now()
    while True:
        vehicle_density = parent_conn.recv()
        estimated_clearance_time = predict_clearance_time(vehicle_density)
        # print(estimated_clearance_time)
        curr_time = datetime.now()
        diff = (curr_time - start_time).seconds
        if diff != 0 and diff % 60 == 0:
            if detect_jam(vehicle_density, estimated_clearance_time) == 0:
                print(f'oh no wait for {estimated_clearance_time}')
                pass
            else:
                print("You can go")
            pass
