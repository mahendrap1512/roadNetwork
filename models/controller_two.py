from datetime import datetime
from multiprocessing import Process, Queue, Pipe
from models.deep_network import predict_clearance_time
from models.camera_two import camera2
from models.trafficJamDetection import detect_jam


# if __name__ == '__main__':
#     parent_conn, child_conn = Pipe()
#     p = Process(target=camera2, args=(child_conn,))
#     p.start()
#     start_time = datetime.now()
#     while True:
#         vehicle_density = parent_conn.recv()
#         estimated_clearance_time = predict_clearance_time(vehicle_density)
#         # print(estimated_clearance_time)
#         curr_time = datetime.now()
#         diff = (curr_time - start_time).seconds
#         if diff != 0 and diff % 60 == 0:
#             jam = False
#             if detect_jam(vehicle_density, estimated_clearance_time) == 0:
#                 jam = True
#                 print(f'oh no wait for {estimated_clearance_time}')
#                 pass
#             else:
#                 print("You can go")
#             light_controller(estimated_clearance_time, jam)


def controller2(child_process):
    parent_conn, child_conn = Pipe()
    p = Process(target=camera2, args=(child_conn,))
    p.start()
    start_time = datetime.now()
    while True:
        vehicle_density = parent_conn.recv()
        estimated_clearance_time = predict_clearance_time(vehicle_density)
        # print(estimated_clearance_time)
        curr_time = datetime.now()
        diff = (curr_time - start_time).seconds
        print("diff : ", diff)
        if diff != 0 and diff % 30 == 0:
            jam_status = detect_jam(vehicle_density, estimated_clearance_time)  # 0 means jam detected
            jam_status = 1 - jam_status
            info = {"vehicles": vehicle_density, "clearance_time": estimated_clearance_time, "jam": jam_status}
            # child_process.send(info)
            print(info)
            # jam = False
            # if detect_jam(vehicle_density, estimated_clearance_time) == 0:
            #     jam = True
            #     print(f'oh no wait for {estimated_clearance_time}')
            #     pass
            # else:
            #     print("You can go")
            # light_controller(estimated_clearance_time, jam)


if __name__ == '__main__':
    controller2('')
