import cv2
import mediapipe as mp
import numpy as np
from math import hypot, pi
import screen_brightness_control as sbc

cap = cv2.VideoCapture(0)  # Checks for camera

mpHands = mp.solutions.hands  # detects hand/finger
hands = mpHands.Hands()  # complete the initialization configuration of hands
mpDraw = mp.solutions.drawing_utils

while True:
    success, img = cap.read()  # If camera works capture an image
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to rgb

    # Collection of gesture information
    results = hands.process(imgRGB)  # completes the image processing.

    lmList = []  # empty list
    if results.multi_hand_landmarks:  # list of all hands detected.
        # By accessing the list, we can get the information of each hand's corresponding flag bit
        for handlandmark in results.multi_hand_landmarks:
            for id, lm in enumerate(handlandmark.landmark):  # adding counter and returning it
                # Get finger joint points
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])  # adding to the empty list 'lmList'
            mpDraw.draw_landmarks(img, handlandmark, mpHands.HAND_CONNECTIONS)

    if lmList != []:
        # getting the value at a point
        # x      #y
        x1, y1 = lmList[4][1], lmList[4][2]  # thumb
        x2, y2 = lmList[8][1], lmList[8 ][2]  # index finger
        x3, y3 = lmList[0][1], lmList[0][2]

        # creating circle at the tips of thumb and index finger
        cv2.circle(img, (x1, y1), 5, (255, 0, 0), cv2.FILLED)  # image #fingers #radius #rgb
        cv2.circle(img, (x2, y2), 5, (255, 0, 0), cv2.FILLED)  # image #fingers #radius #rgb
        cv2.circle(img, (x3, y3), 5, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
        cv2.line(img, (x2, y2), (x3, y3), (250, 5, 0), 3)
        cv2.line(img, (x1, y1), (x3, y3), (250, 5, 0), 3)  # create a line b/w tips of index finger and thumb

        length = hypot(x2 - x1, y2 - y1)
        length2 = hypot(x3 - x1, y3 - y1)
        length3 = hypot(x3 - x2, y3 - y2)

        try:
            angle = np.arccos((length2 ** 2 + length3 ** 2 - length ** 2) / (2 * length2 * length3))
        except:
            angle = 0
        print(f"Angle {angle}")
        angle = 2 * ((angle * 180) / pi)

        bright = np.interp(angle, [6, 100], [0, 100])

        sbc.set_brightness(int(bright))

        current_brightness = sbc.get_brightness()

        brightness_text = int(current_brightness[0])
        brightness_bar = np.interp(current_brightness, [6, 100], [400, 100])

        cv2.rectangle(img, (50, 100), (85, 400), (0, 0, 255), 2)
        cv2.rectangle(img, (50, int(brightness_bar)), (85, 400), (0, 0, 255), cv2.FILLED)
        # vid ,initial position ,ending position ,rgb ,thickness
        cv2.putText(img, f"{int(brightness_text)}%", (10, 65), cv2.FONT_ITALIC, 2, (0, 255, 98), 2)
    cv2.imshow('Image', img)  # Show the video
    if cv2.waitKey(1) & 0xff == ord(' '):  # By using spacebar delay will stop
        break

cap.release()  # stop cam
cv2.destroyAllWindows()
