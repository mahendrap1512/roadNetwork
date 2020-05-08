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


# controller(duration=20, jam=True)
key = cv2.waitKey(0)
try:
    if key == 27:
        cv2.destroyAllWindows()
except TypeError as e:
    exit(0)
