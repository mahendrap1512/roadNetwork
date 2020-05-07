import asyncio
import csv
import datetime
import random
import time

import cv2
import numpy as np

modelConfiguration = "darknet/cfg/yolov3.cfg"
modelWeights = "darknet/yolov3.weights"
yolo_net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
labels = list()

with open("labels.txt", "r") as file:
    temp_labels = [label.strip() for label in file.readlines()]
    labels.extend(temp_labels)

# print(labels)
layer_names = yolo_net.getLayerNames()
outputlayers = [layer_names[i[0] - 1] for i in yolo_net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(labels), 3))
font = cv2.FONT_HERSHEY_PLAIN


vehicle_counts = [0, 0]


async def object_detection(cap, img):
    frame_id = 0
    starting_time = time.time()
    while True:
        _, frame = cap.read()  #
        frame_id += 1
        height, width, channels = frame.shape
        # detecting objects
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (320, 320), (0, 0, 0), True, crop=False)
        yolo_net.setInput(blob)
        outs = yolo_net.forward(outputlayers)
        # Showing info on screen/ get confidence score of algorithm in detecting an object in blob
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                # if confidence > 0.3 then object found
                if confidence > 0.3:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # rectangle co-ordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])  # put all rectangle areas
                    confidences.append(
                        float(confidence))  # how confidence was that object detected and show that percentage
                    class_ids.append(class_id)  # name of the object that was detected

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.6)

        vehicle_ids = [1, 2, 3, 5, 7, 0]
        for i in range(len(boxes)):
            if i in indexes and class_ids[i] in vehicle_ids:
                x, y, w, h = boxes[i]
                label = str(labels[class_ids[i]])
                confidence = confidences[i]
                color = colors[class_ids[i]]
                if not class_ids[i] == 0:
                    if img == "image1":
                        vehicle_counts[0] += 1
                    elif img == "image2":
                        vehicle_counts[1] += 1
                    elif img == "image3":
                        vehicle_counts[2] += 1
                    elif img == "image4":
                        vehicle_counts[3] += 1
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 30), font, 1, (255, 255, 255), 2)

        elapsed_time = time.time() - starting_time
        # fps = frame_id / elapsed_time
        # cv2.putText(frame, "FPS:" + str(round(fps, 2)), (10, 50), font, 2, (0, 0, 0), 1)

        cv2.imshow(img, frame)
        key = cv2.waitKey(1)  # wait 1ms the loop will start again and we will process the next frame
        await asyncio.sleep(1)
        if key == 27:  # esc key stops the process
            return


async def manager():
    cap1 = cv2.VideoCapture("video1.webm")
    cap1.set(3, 160)
    cap1.set(4, 120)
    cap2 = cv2.VideoCapture("video2.mp4")
    cap2.set(3, 160)
    cap2.set(4, 120)
    # cap3 = cv2.VideoCapture("roadTraffic.mp4")
    # cap3.set(3, 160)
    # cap3.set(4, 120)
    # cap4 = cv2.VideoCapture("roadTraffic.mp4")
    # cap4.set(3, 160)
    # cap4.set(4, 120)
    await asyncio.gather(object_detection(cap1, "image1"),
                         object_detection(cap2, "image2",))

    # while True:
    #     _, frame1 = cap1.read()
    #     cv2.imshow("camera 1", frame1)
    #     _, frame2 = cap2.read()
    #     cv2.imshow("camera 2", frame2)
    #     _, frame3 = cap3.read()
    #     cv2.imshow("camera 3", frame3)
    #     _, frame4 = cap4.read()
    #     cv2.imshow("camera 4", frame4)
    #     key = cv2.waitKey(1)
    #     if key == 27:
    #         cap1.release()
    #         cap2.release()
    #         cap3.release()
    #         cap4.release()
    #         break


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    asyncio.run(manager())
    print(vehicle_counts)
    end_time = datetime.datetime.now()
    safe = random.randint(0, 1)
    fileptr = open("./data/collectedData.csv", "a")
    file = csv.writer(fileptr)
    file.writerow([vehicle_counts[0], start_time, end_time, end_time - start_time, safe])
    fileptr.close()
    cv2.destroyAllWindows()
