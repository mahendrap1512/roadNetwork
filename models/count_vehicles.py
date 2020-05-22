# import the necessary packages
import cv2
from imutils.video import FPS

tracker = cv2.TrackerCSRT_create()
vs = cv2.VideoCapture("../Traffic.mp4")
initBB = None

detec = []


def pega_centro(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx,cy


roi = 480
counter = 0
offset = 6

# loop over frames from the video stream
while vs.isOpened():

    ret,frame = vs.read()

    cv2.line(frame, (769 , roi), (1298 , roi), (255,0,0), 3)
    # check to see if we are currently tracking an object
    if initBB is not None:
        # grab the new bounding box coordinates of the object
        (success, box) = tracker.update(frame)

        # check to see if the tracking was a success
        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h),
                (0, 255, 0), 2)

            cX = int((x + x+w) / 2.0)
            cY = int((y + y+h) / 2.0)

            cv2.circle(frame, (cX, cY), 3, (0, 0, 255), -1)

            c=pega_centro(x, y, w, h)
            detec.append(c)

        for (x,y) in detec:
            if y<(roi+offset) and y>(roi-offset):
                counter+=1
                print(counter)
                cv2.line(frame, (769 , roi), (1298 , roi), (0,0,255), 3)
                detec.remove((x,y))

    # show the output frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("s"):
        # select the bounding box of the object we want to track (make
        # sure you press ENTER or SPACE after selecting the ROI)
        initBB = cv2.selectROI("Frame", frame, fromCenter=False,
            showCrosshair=True)

        # start OpenCV object tracker using the supplied bounding box
        # coordinates, then start the FPS throughput estimator as well
        tracker.init(frame, initBB)
        fps = FPS().start()

    # if the `q` key was pressed, break from the loop
    elif key == ord("q"):
        break

else:
    vs.release()

cv2.destroyAllWindows()