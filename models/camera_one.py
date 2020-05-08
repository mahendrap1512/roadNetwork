

from multiprocessing import Process, Pipe

vehicles_count = 0


def camera1(child_conn):
    global vehicles_count
    # msg = "Hello"
    # child_conn.send(msg)

    import cv2
    import numpy as np
    import time
    import datetime

    # _net_cfg_path = "/home/mahendra/PycharmProjects/roadNetwork/darknet/cfg/yolo.cfg"

    modelConfiguration = "../darknet/cfg/yolov3.cfg"
    modelWeights = "../darknet/yolov3.weights"
    yolo_net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
    labels = list()

    with open("../labels.txt", "r") as file:
        temp_labels = [label.strip() for label in file.readlines()]
        labels.extend(temp_labels)

    # print(labels)
    layer_names = yolo_net.getLayerNames()
    outputlayers = [layer_names[i[0] - 1] for i in yolo_net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(labels), 3))

    # loading image
    cap = cv2.VideoCapture("../video2.mp4")  # for web-cam use 0, else file name
    font = cv2.FONT_HERSHEY_PLAIN
    starting_time = datetime.datetime.now()
    frame_id = 0
    cv2.waitKey(0)

    while True:
        _, frame = cap.read()  #
        frame_id += 1
        height, width, channels = frame.shape
        # detecting objects
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (320, 320), (0, 0, 0), True, crop=False)  # reduce 416 to 320

        yolo_net.setInput(blob)
        outs = yolo_net.forward(outputlayers)
        # print(outs[1])
        vehicle_ids = [1, 2, 3, 5, 7, 0]
        # Showing info on screen/ get confidence score of algorithm in detecting an object in blob
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.3:
                    # object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # cv2.circle(img,(center_x,center_y),10,(0,255,0),2)
                    # rectangle co-ordinate
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    # cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
                    # print("y_center is : ", center_y)
                    if class_id in vehicle_ids and 400 < center_y < 404:
                        print("catch the vehicles")
                        vehicles_count += 1
                        pass

                    boxes.append([x, y, w, h])  # put all rectangle areas
                    confidences.append(
                        float(confidence))  # how confidence was that object detected and show that percentage
                    class_ids.append(class_id)  # name of the object tha was detected
                    # print(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.6)

        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(labels[class_ids[i]])
                confidence = confidences[i]
                color = colors[class_ids[i]]
                # if not class_ids[i] == 0:
                #     vehicles_count += 1
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 30), font, 1, (255, 255, 255), 2)

        # cv2.line(frame, (10, 320), (800, 320), color=(211, 102, 198))
        # elapsed_time = time.time() - starting_time
        # fps = frame_id / elapsed_time
        # cv2.putText(frame, "FPS:" + str(round(fps, 2)), (10, 50), font, 2, (0, 0, 0), 1)

        cv2.imshow("Image", frame)
        key = cv2.waitKey(2)  # wait 1ms the loop will start again and we will process the next frame

        if key == 27:  # esc key stops the process
            # print(vehicles_count)
            child_conn.close()
            break

        current_time = datetime.datetime.now()
        time_elapsed = (current_time - starting_time).seconds
        if time_elapsed % 60 == 0:
            child_conn.send(vehicles_count)
            pass

    cap.release()
    cv2.destroyAllWindows()


