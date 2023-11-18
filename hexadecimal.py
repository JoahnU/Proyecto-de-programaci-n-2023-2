import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)  # Checks for camera

mpHands = mp.solutions.hands  # detects hand/finger
hands = mpHands.Hands()  # complete the initialization configuration of hands
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

        x, y = lmList[4][1], lmList[4][2]  # pulgar
        x1, y1 = lmList[8][1], lmList[8][2]  # indice
        x2, y2 = lmList[12][1], lmList[12][2]  # corazon
        x3, y3 = lmList[16][1], lmList[16][2]  # anular
        x4, y4 = lmList[20][1], lmList[20][2]  # meñique
        x5, y5 = lmList[6][1], lmList[6][2]  # indice falange
        x6, y6 = lmList[10][1], lmList[10][2]  # corazon falange
        x7, y7 = lmList[14][1], lmList[14][2]  # anular falange
        x8, y8 = lmList[13][1], lmList[13][2]  # anular palma
        x9, y9 = lmList[17][1], lmList[18][2]  # meñique base

        if y1 > y6 and y2 > y6 and y3 > y6 and y4 > y6:
            numero = "0"
        elif y2 > y1 and y3 > y1 and y4 > y1 and x < y9:
            numero = "1"
        elif y2 > y1 and y3 > y1 and y4 > y1:
            numero = "2"
        else:
            numero = "puto"

    cv2.putText(img, f"numero {numero}", (10, 65), cv2.FONT_ITALIC, 2, (0, 255, 98), 2)
    cv2.imshow('Image', img)  # Show the video
    if cv2.waitKey(1) & 0xff == ord(' '):  # By using spacebar delay will stop
        break

cap.release()  # stop cam
cv2.destroyAllWindows()

