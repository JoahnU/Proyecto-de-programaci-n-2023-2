import cv2
import mediapipe as mp
from math import hypot

cap = cv2.VideoCapture(0)  # Checks for camera

mpHands = mp.solutions.hands  # detects hand/finger
hands = mpHands.Hands(static_image_mode=False, max_num_hands=1)  # complete the initialization configuration of hands
mpDraw = mp.solutions.drawing_utils

numero = ""

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

        x, y = lmList[0][1], lmList[0][2]  # Base palma
        x1, y1 = lmList[1][1], lmList[1][2]  # Pulgar base
        x11, y11 = lmList[2][1], lmList[2][2]  # Pulgar falange 1
        x12, y12 = lmList[3][1], lmList[3][2]  # Pulgar falange 2
        x13, y13 = lmList[4][1], lmList[4][2]  # Pulgar punta
        x2, y2 = lmList[5][1], lmList[5][2]  # Indice base
        x21, y21 = lmList[6][1], lmList[6][2]  # Indice falange 1
        x22, y22 = lmList[7][1], lmList[7][2]  # Indice falange 2
        x23, y23 = lmList[8][1], lmList[8][2]  # Indice punta
        x3, y3 = lmList[9][1], lmList[9][2]  # Corazon base
        x31, y31 = lmList[10][1], lmList[10][2]  # Corazon falange 1
        x32, y32 = lmList[11][1], lmList[11][2]  # Corazon falange 2
        x33, y33 = lmList[12][1], lmList[12][2]  # Corazon punta
        x4, y4 = lmList[13][1], lmList[13][2]  # Anular base
        x41, y41 = lmList[14][1], lmList[14][2]  # Anular falange 1
        x42, y42 = lmList[15][1], lmList[15][2]  # Anular falange 2
        x43, y43 = lmList[16][1], lmList[16][2]  # Anular punta
        x5, y5 = lmList[17][1], lmList[17][2]  # Meñique base
        x51, y51 = lmList[18][1], lmList[18][2]  # Meñique falange 1
        x52, y52 = lmList[19][1], lmList[19][2]  # Meñique falange 2
        x53, y53 = lmList[20][1], lmList[20][2]  # Meñique punta

        length_indice_pulgar = hypot(x13 - x23, y13 - y23)
        length_corazon_pulgar = hypot(x13 - x33, y13 - y33)
        length_anular_pulgar = hypot(x13 - x43, y13 - y43)
        length_menique_pulgar = hypot(x13 - x53, y13 - y53)
        distancia_umbral = 40

        print("x indice", x22)
        print("x pulgar", x13)
        print(length_menique_pulgar)

        if (y13 > y21 and y23 > y21 and y33 > y31 and y43 > y41 and y53 > y51) and (x23>x13):
            numero = "0"
        elif  y23 < y22 and y33 > y32 and y43 > y42 and y53 > y52: #y13 <= y12 and
            numero = "1"
        elif y13 > y21 and y23 < y22 and y33 < y32 and y43 > y42 and y53 > y52 and x13<x2:
            numero = "2"
        elif y13 < y53 and y23 < y22 and y33 < y32 and y43 > y42 and y53 > y52:
            numero = "3"
        elif y13 > y21 and y23 < y22 and y33 < y32 and y43 < y42 and y53 < y52 and x13<x2 :
            numero = "4"
        elif length_indice_pulgar < distancia_umbral and y53 < y52 and y43 < y42 and y33 < y32:
            numero = "9"
        elif  y23 < y22 and y33 < y32 and y43 < y42 and y53 < y52 and y13 > y23: #y13 <= y5 and
            numero = "5"
        elif length_menique_pulgar < distancia_umbral and y43 < y42 and y33 < y32 and y23 < y22:
            numero = "6"
        elif length_anular_pulgar < distancia_umbral and y53 < y52 and y33 < y32 and y23 < y22:
            numero = "7"
        elif length_corazon_pulgar < distancia_umbral and y53 < y52 and y43 < y42  and y23 < y22:
            numero = "8"
        elif y13 < y21 and y13 < y31 and y13 < y41 and y13 < y51:
            numero = "A"
        elif y13 > y21 and y23 > y21 and y33 > y31 and y43 > y41 and y53 < y51 and y53 < y33:
            numero = "B"
        elif x53 > x5 and x13 > x22 and y13 > y23: # or (x53 < x5 and x13 < x22):
            numero = "C"
        elif y13 > y21 and y23 > y21 and y33 > y31 and y43 < y41 and y53 < y51 and y53 < y33:
            numero = "D"
        elif x23 > x43 and x53 > x33 and y5 > y:
            numero = "E"
        elif x23 > x43 and x33 > x53 and y5 > y:
            numero = "F"

        else:
            numero = "Gesto irreconocible"

    cv2.putText(img, f"numero {numero}", (10, 65), cv2.FONT_ITALIC, 1, (255, 255, 255), 2)
    cv2.imshow('Image', img)  # Show the video
    if cv2.waitKey(1) & 0xff == ord(' '):  # By using spacebar delay will stop
        break

cap.release()  # stop cam
cv2.destroyAllWindows()

