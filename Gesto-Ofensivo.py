import cv2
import mediapipe as mp
import ctypes

def turn_off_screen():
    ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, 2)

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
        y1 = lmList[10][2]  # Dedo corazon
        y2 = lmList[8][2]  # Dedo indice
        y3 = lmList[16][2] # Dedo anular
        y4 = lmList[20][2]  # Dedo meñique

        if y1 < y2 and y1 < y3 and y1 < y3:
            turn_off_screen()
            break

    cv2.imshow('Image', img)  # Show the video
    if cv2.waitKey(1) & 0xff == ord(' '):  # By using spacebar delay will stop
        break

cap.release()  # stop cam

cv2.destroyAllWindows()  # close window
