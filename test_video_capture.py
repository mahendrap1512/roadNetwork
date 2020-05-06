import cv2

cap0 = cv2.VideoCapture("roadTraffic.mp4")
# cap0.set(3, 160)
# cap0.set(4, 120)
cap1 = cv2.VideoCapture(0)
# cap1.set(3, 160)
# cap1.set(4, 120)

while True:
    ret0, frame0 = cap0.read()
    ret1, frame1 = cap1.read()
    cv2.imshow("frame 0", frame0)
    cv2.imshow("frame 1", frame1)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap1.release()
cap0.release()
cv2.destroyWindow()

