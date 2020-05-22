from models.deep_network import predict_clearance_time
from models.camera_two import camera2
from models.trafficJamDetection import detect_jam

from datetime import datetime
from multiprocessing import Process, Pipe
from models.camera_one import camera1
import random
import cv2
import numpy as np


canvas = np.zeros((500, 500), dtype="uint8")
canvas = cv2.cvtColor(canvas, cv2.COLOR_BAYER_GB2BGR)
image = cv2.rectangle(canvas, (120, 120), (270, 350), (255, 255, 255), 2)

image = cv2.circle(image, (195, 180), 30, (0, 255, 0), -1)

cv2.rectangle(image, (150, 250), (250, 320), (255, 255, 255), 2)
# cv2.imshow("canvas", image)


def make_green():
    global image
    image = cv2.circle(image, (195, 180), 30, (0, 255, 0), -1)
    cv2.imshow("canvas", image)


def make_red():
    global image
    image = cv2.circle(image, (195, 180), 30, (0, 0, 255), -1)
    cv2.imshow("canvas", image)


def make_yellow():
    global image
    image = cv2.circle(image, (195, 180), 30, (0, 255, 255), -1)
    cv2.imshow("canvas", image)


def light_controller(duration, jam):
    global image
    a = duration
    if jam:
        cv2.putText(image, "STOP", (160, 290), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
        make_red()
        while a > 0:
            cv2.waitKey(1000)
            a -= 1
            text = str(a)
            if a > 5:
                image = cv2.rectangle(image, (150, 250), (250, 320), (0, 0, 0), -1)
                image = cv2.rectangle(image, (150, 250), (250, 320), (255, 255, 255), 2)
                cv2.putText(image, text, (180, 290), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1)
                make_red()
            elif a <= 5:
                image = cv2.rectangle(image, (150, 250), (250, 320), (0, 0, 0), -1)
                image = cv2.rectangle(image, (150, 250), (250, 320), (255, 255, 255), 2)
                cv2.putText(image, text, (180, 290), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1)
                make_yellow()
        image = cv2.rectangle(image, (150, 250), (250, 320), (0, 0, 0), -1)
        image = cv2.rectangle(image, (150, 250), (250, 320), (255, 255, 255), 2)
        cv2.putText(image, "GO", (180, 290), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
        make_green()
    else:
        cv2.putText(image, "GO", (160, 290), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
        make_green()


if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=camera2, args=(child_conn,))
    p.start()
    parent_conn1, child_conn1 = Pipe()
    p1 = Process(target=camera1, args=(child_conn1,))
    p1.start()
    start_time = datetime.now()
    last_five_minute_traffic = [0, 0, 0, 0, 0]
    vehicle_count = 0
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
            if jam_status == 1:
                estimated_clearance_time = info.get("clearance_time")
                # display traffic light here for clearance time
                light_controller(estimated_clearance_time, True)

        curr_time = datetime.now()
        time_duration = (curr_time - start_time).seconds
        if time_duration != 0 and time_duration % 60 == 0:
            # change permissible traffic here
            permissible_traffic = random.randint(40, 120)
            # last_minute_traffic_camera_1 = parent_conn1.recv()
            last_minute_traffic_camera_1 = random.randint(10, 30)
            vehicle_count -= last_five_minute_traffic[4]
            for i in range(4, 0, -1):
                last_five_minute_traffic[i] = last_five_minute_traffic[i - 1]
            last_five_minute_traffic[0] = last_minute_traffic_camera_1
            vehicle_count += last_minute_traffic_camera_1
            if vehicle_count > permissible_traffic:
                # cool-down for 1 min
                # display traffic light here
                light_controller(60, True)
                vehicle_count -= last_five_minute_traffic[4]
                for i in range(4, 0, -1):
                    last_five_minute_traffic[i] = last_five_minute_traffic[i - 1]
                last_five_minute_traffic[0] = 0

        if time_duration % 300 == 0:
            start_time = datetime.now()
            last_five_minute_traffic = [0, 0, 0, 0, 0]
            vehicle_count = 0
            pass

        # if time_duration != 0 and time_duration % 30 == 0:
        #     camera2_info = parent_conn2.recv()
        #     print(camera2_info)
        #     if camera2_info.get("jam") == 1:
        #         estimated_clearance_time = camera2_info.get("clearance_time")
        #         # display traffic light here for clearance time
        #         light_controller(estimated_clearance_time, True)
