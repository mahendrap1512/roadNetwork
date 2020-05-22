from datetime import datetime
from multiprocessing import Process, Pipe
from models.deep_network import predict_clearance_time
from models.camera_two import camera2
from models.trafficJamDetection import detect_jam
from datetime import timedelta
import csv


def one_second_wait():
    temporary_start = datetime.now()
    while True:
        temporary_end = datetime.now()
        if (temporary_end - temporary_start).seconds >= 1:
            break


def wait_to_five():
    minutes = datetime.now().minute
    print(minutes)
    while minutes % 5 != 0:
        one_second_wait()
        minutes = datetime.now().minute
    print("wait done : ")


def write_to_file(info):
    with open("../data/collectedData.csv", "a") as fileptr:
        file_writer = csv.writer(fileptr)
        safe = 1 - info.get("jam")
        vehicle_density = info.get('vehicles')
        clearance_time = info.get("clearance_time")
        time = str(datetime.now() - timedelta(minutes=5))[11:16]
        print("time is :", time)
        row = [vehicle_density, time, clearance_time, safe]
        file_writer.writerow(row)


def controller2(child_conn2):
    parent_conn, child_conn = Pipe()
    p = Process(target=camera2, args=(child_conn,))
    p.start()
    start_time = datetime.now()
    while True:
        vehicle_density = parent_conn.recv()
        estimated_clearance_time = int(predict_clearance_time(vehicle_density))
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
            if diff % 300 == 0:
                write_to_file(info)

            one_second_wait()
            # jam = False
            # if detect_jam(vehicle_density, estimated_clearance_time) == 0:
            #     jam = True
            #     print(f'oh no wait for {estimated_clearance_time}')
            #     pass
            # else:
            #     print("You can go")
            # light_controller(estimated_clearance_time, jam)


if __name__ == '__main__':
    # wait_to_five()
    controller2('')
