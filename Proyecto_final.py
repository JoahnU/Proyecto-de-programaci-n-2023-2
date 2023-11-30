import os
import cv2
import time
import ctypes
import pyautogui
import numpy as np
import mediapipe as mp
import screen_brightness_control as sbc
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from math import hypot, pi


# funciones
def menu():
    cap = cv2.VideoCapture(0)

    mpHands = mp.solutions.hands
    hands = mpHands.Hands(static_image_mode=False,
                          max_num_hands=1)
    mpDraw = mp.solutions.drawing_utils

    numero = ""

    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = hands.process(imgRGB)

        lmList = []
        if results.multi_hand_landmarks:

            for handlandmark in results.multi_hand_landmarks:
                for id, lm in enumerate(handlandmark.landmark):
                    h, w, _ = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
                mpDraw.draw_landmarks(img, handlandmark, mpHands.HAND_CONNECTIONS)

        if lmList != []:

            x13, y13 = lmList[4][1], lmList[4][2]  # Pulgar punta
            x2, y2 = lmList[5][1], lmList[5][2]  # Indice base
            x21, y21 = lmList[6][1], lmList[6][2]  # Indice falange 1
            x22, y22 = lmList[7][1], lmList[7][2]  # Indice falange 2
            x23, y23 = lmList[8][1], lmList[8][2]  # Indice punta
            x32, y32 = lmList[11][1], lmList[11][2]  # Corazon falange 2
            x33, y33 = lmList[12][1], lmList[12][2]  # Corazon punta
            x42, y42 = lmList[15][1], lmList[15][2]  # Anular falange 2
            x43, y43 = lmList[16][1], lmList[16][2]  # Anular punta
            x52, y52 = lmList[19][1], lmList[19][2]  # Meñique falange 2
            x53, y53 = lmList[20][1], lmList[20][2]  # Meñique punta

            length_menique_pulgar = hypot(x13 - x53, y13 - y53)
            distancia_umbral = 40

            if y23 < y22 and y33 > y32 and y43 > y42 and y53 > y52:  # 
                numero = "1"
                num = 1
            elif y13 > y21 and y23 < y22 and y33 < y32 and y43 > y42 and y53 > y52 and x13 < x2:
                numero = "2"
                num = 2
            elif y13 < y53 and y23 < y22 and y33 < y32 and y43 > y42 and y53 > y52:
                numero = "3"
                num = 3
            elif y13 > y21 and y23 < y22 and y33 < y32 and y43 < y42 and y53 < y52 and x13 < x2:
                numero = "4"
                num = 4
            elif y23 < y22 and y33 < y32 and y43 < y42 and y53 < y52 and y13 > y23:  # y13 <= y5 and
                numero = "5"
                num = 5
            elif length_menique_pulgar < distancia_umbral and y43 < y42 and y33 < y32 and y23 < y22:
                numero = "6"
                num = 6
            else:
                numero = "Gesto irreconocible"
                num = 0

        cv2.putText(img, f"numero {numero}", (10, 65), cv2.FONT_ITALIC, 1, (255, 255, 255), 2)
        cv2.putText(img, "Menu", (10, 470), cv2.FONT_ITALIC, 1.5, (255, 255, 255), 2)
        cv2.imshow('Image', img)
        if cv2.waitKey(1) & 0xff == ord(' '):
            break

    cap.release()
    cv2.destroyAllWindows()
    return num


def volume():
    cap = cv2.VideoCapture(0)

    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    volMin, volMax = volume.GetVolumeRange()[:2]

    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        cv2.putText(img, "Volumen", (10, 470), cv2.FONT_ITALIC, 1.5, (255, 255, 255), 2)
        lmList = []
        if results.multi_hand_landmarks:
            for handlandmark in results.multi_hand_landmarks:
                for id, lm in enumerate(handlandmark.landmark):
                    h, w, _ = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
                mpDraw.draw_landmarks(img, handlandmark, mpHands.HAND_CONNECTIONS)

        if lmList != []:
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            x3, y3 = lmList[0][1], lmList[0][2]

            cv2.circle(img, (x1, y1), 5, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 5, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x3, y3), 5, (255, 0, 0), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
            cv2.line(img, (x2, y2), (x3, y3), (250, 5, 0), 3)
            cv2.line(img, (x1, y1), (x3, y3), (250, 5, 0), 3)

            length = hypot(x2 - x1, y2 - y1)
            length2 = hypot(x3 - x1, y3 - y1)
            length3 = hypot(x3 - x2, y3 - y2)

            try:
                angle = np.arccos((length2 ** 2 + length3 ** 2 - length ** 2) / (2 * length2 * length3))
            except:
                angle = 0

            angle = 2 * ((angle * 180) / pi)

            vol = np.interp(angle, [6, 90], [volMin, volMax])
            volbar = np.interp(angle, [6, 90], [400, 150])
            volper = np.interp(angle, [6, 90], [0, 100])

            volume.SetMasterVolumeLevel(vol, None)

            cv2.rectangle(img, (50, 150), (85, 400), (0, 0, 255),
                          4)  # vid ,initial position ,ending position ,rgb ,thickness
            cv2.rectangle(img, (50, int(volbar)), (85, 400), (0, 0, 255), cv2.FILLED)
            cv2.putText(img, f"{int(volper)}%", (10, 40), cv2.FONT_ITALIC, 1, (255, 255, 255), 3)
        cv2.imshow('Image', img)
        if cv2.waitKey(1) & 0xff == ord(' '):
            break

    cap.release()
    cv2.destroyAllWindows()


def bright():
    cap = cv2.VideoCapture(0)

    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils

    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = hands.process(imgRGB)

        lmList = []
        if results.multi_hand_landmarks:
            for handlandmark in results.multi_hand_landmarks:
                for id, lm in enumerate(handlandmark.landmark):  
                    h, w, _ = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])  
                mpDraw.draw_landmarks(img, handlandmark, mpHands.HAND_CONNECTIONS)

        if lmList != []:
            x1, y1 = lmList[4][1], lmList[4][2]  
            x2, y2 = lmList[8][1], lmList[8][2]  
            x3, y3 = lmList[0][1], lmList[0][2]
            
            cv2.circle(img, (x1, y1), 5, (255, 0, 0), cv2.FILLED)  
            cv2.circle(img, (x2, y2), 5, (255, 0, 0), cv2.FILLED)  
            cv2.circle(img, (x3, y3), 5, (255, 0, 0), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (250, 5, 0), 3)
            cv2.line(img, (x2, y2), (x3, y3), (250, 5, 0), 3)
            cv2.line(img, (x1, y1), (x3, y3), (250, 5, 0), 3)  

            length = hypot(x2 - x1, y2 - y1)
            length2 = hypot(x3 - x1, y3 - y1)
            length3 = hypot(x3 - x2, y3 - y2)

            try:
                angle = np.arccos((length2 ** 2 + length3 ** 2 - length ** 2) / (2 * length2 * length3))
            except:
                angle = 0

            angle = 2 * ((angle * 180) / pi)

            bright = np.interp(angle, [6, 100], [0, 100])

            sbc.set_brightness(int(bright))

            current_brightness = sbc.get_brightness()

            brightness_text = int(current_brightness[0])
            brightness_bar = np.interp(current_brightness, [6, 100], [400, 100])

            cv2.rectangle(img, (50, 100), (85, 400), (0, 0, 255), 2)
            cv2.rectangle(img, (50, int(brightness_bar)), (85, 400), (0, 0, 255), cv2.FILLED)
            # vid ,initial position ,ending position ,rgb ,thickness
            cv2.putText(img, f"{int(brightness_text)}%", (10, 65), cv2.FONT_ITALIC, 2, (255, 255, 255), 2)
            cv2.putText(img, "Brillo", (10, 470), cv2.FONT_ITALIC, 1.5, (255, 255, 255), 2)
        cv2.imshow('Image', img)  
        if cv2.waitKey(1) & 0xff == ord(' '):  
            break

    cap.release()  
    cv2.destroyAllWindows()


def window():
    cap = cv2.VideoCapture(0)  

    mpHands = mp.solutions.hands  
    hands = mpHands.Hands()  
    mpDraw = mp.solutions.drawing_utils

    previous_command = None

    while True:
        success, img = cap.read()  
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  
        results = hands.process(imgRGB)  

        lmList = []  
        if results.multi_hand_landmarks:  
            for handlandmark in results.multi_hand_landmarks:
                for id, lm in enumerate(handlandmark.landmark):  
                    h, w, _ = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])  
                mpDraw.draw_landmarks(img, handlandmark, mpHands.HAND_CONNECTIONS)

        if lmList != []:
            x1, y1 = lmList[4][1], lmList[4][2]  
            x2, y2 = lmList[12][1], lmList[12][2] 
            cv2.circle(img, (x1, y1), 8, (0, 0, 255), cv2.FILLED)  
            cv2.circle(img, (x2, y2), 8, (0, 0, 255), cv2.FILLED) 
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 0), 3)  

            length = hypot(x2 - x1, y2 - y1)  
            # Distancia umbral
            threshold_distance = 100

            current_command = None

            # Maximizar ventana
            if length > threshold_distance:
                current_command = 'win+shift+m'

            elif length < threshold_distance:
                current_command = 'win+m'

            # Ejecutar el comando solo si no se ejecutó en el ciclo anterior
            if current_command != previous_command:
                pyautogui.hotkey(*current_command.split('+'))
                previous_command = current_command

        cv2.putText(img, "Video", (10, 470), cv2.FONT_ITALIC, 1.5, (255, 255, 255), 2)
        cv2.imshow('Image', img)  
        if cv2.waitKey(1) & 0xff == ord(' '):  
            break

    cap.release()  
    cv2.destroyAllWindows()  


def calculadora():
    def numeros():
        cap = cv2.VideoCapture(0)

        mpHands = mp.solutions.hands
        hands = mpHands.Hands(static_image_mode=False,
                              max_num_hands=1)
        mpDraw = mp.solutions.drawing_utils

        numero = ""

        while True:
            success, img = cap.read()
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)

            lmList = []
            if results.multi_hand_landmarks:
                for handlandmark in results.multi_hand_landmarks:
                    for id, lm in enumerate(handlandmark.landmark):
                        h, w, _ = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        lmList.append([id, cx, cy])
                    mpDraw.draw_landmarks(img, handlandmark, mpHands.HAND_CONNECTIONS)

            if lmList != []:

                x, y = lmList[0][1], lmList[0][2]  # Base palma
                x13, y13 = lmList[4][1], lmList[4][2]  # Pulgar punta
                x2, y2 = lmList[5][1], lmList[5][2]  # Indice base
                x21, y21 = lmList[6][1], lmList[6][2]  # Indice falange 1
                x22, y22 = lmList[7][1], lmList[7][2]  # Indice falange 2
                x23, y23 = lmList[8][1], lmList[8][2]  # Indice punta
                x31, y31 = lmList[10][1], lmList[10][2]  # Corazon falange 1
                x32, y32 = lmList[11][1], lmList[11][2]  # Corazon falange 2
                x33, y33 = lmList[12][1], lmList[12][2]  # Corazon punta
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

                if (y13 > y21 and y23 > y21 and y33 > y31 and y43 > y41 and y53 > y51) and (x23 > x13):
                    numero = "0"
                    num = 0
                elif y23 < y22 and y33 > y32 and y43 > y42 and y53 > y52:  # y13 <= y12 and
                    numero = "1"
                    num = 1
                elif y13 > y21 and y23 < y22 and y33 < y32 and y43 > y42 and y53 > y52 and x13 < x2:
                    numero = "2"
                    num = 2
                elif y13 < y53 and y23 < y22 and y33 < y32 and y43 > y42 and y53 > y52:
                    numero = "3"
                    num = 3
                elif y13 > y21 and y23 < y22 and y33 < y32 and y43 < y42 and y53 < y52 and x13 < x2:
                    numero = "4"
                    num = 4
                elif length_indice_pulgar < distancia_umbral and y53 < y52 and y43 < y42 and y33 < y32:
                    numero = "9"
                    num = 9
                elif y23 < y22 and y33 < y32 and y43 < y42 and y53 < y52 and y13 > y23:  # y13 <= y5 and
                    numero = "5"
                    num = 5
                elif length_menique_pulgar < distancia_umbral and y43 < y42 and y33 < y32 and y23 < y22:
                    numero = "6"
                    num = 6
                elif length_anular_pulgar < distancia_umbral and y53 < y52 and y33 < y32 and y23 < y22:
                    numero = "7"
                    num = 7
                elif length_corazon_pulgar < distancia_umbral and y53 < y52 and y43 < y42 and y23 < y22:
                    numero = "8"
                    num = 8
                elif y13 < y21 and y13 < y31 and y13 < y41 and y13 < y51:
                    numero = "A"
                    num = 10
                elif y13 > y21 and y23 > y21 and y33 > y31 and y43 > y41 and y53 < y51 and y53 < y33:
                    numero = "B"
                    num = 11
                elif x53 > x5 and x13 > x22 and y13 > y23:  # or (x53 < x5 and x13 < x22):
                    numero = "C"
                    num = 12
                elif y13 > y21 and y23 > y21 and y33 > y31 and y43 < y41 and y53 < y51 and y53 < y33:
                    numero = "D"
                    num = 13
                elif x23 > x43 and x53 > x33 and y5 > y:
                    numero = "E"
                    num = 14
                elif x23 > x43 and x33 > x53 and y5 > y:
                    numero = "F"
                    num = 15

                else:
                    numero = "Gesto irreconocible"
                    num = None

            cv2.putText(img, f"numero {numero}", (10, 65), cv2.FONT_ITALIC, 1, (255, 255, 255), 2)
            cv2.putText(img, "Calculadora", (10, 470), cv2.FONT_ITALIC, 1.5, (255, 255, 255), 2)
            cv2.imshow('Image', img)
            if cv2.waitKey(1) & 0xff == ord(' '):
                break

        cap.release()  
        cv2.destroyAllWindows()
        return num

    print("Elige una opcion: \n1. suma \n2. resta \n3. multiplicacion \n4. division \n5. salir\n")
    opcion = numeros()

    if opcion == 1:
        x = numeros()
        time.sleep(0.5)
        y = numeros()
        time.sleep(0.5)
        operacion = x + y
        print(f'El resultado es: {operacion}')
    elif opcion == 2:
        x = numeros()
        time.sleep(0.5)
        y = numeros()
        time.sleep(0.5)
        operacion = x - y
        print(f'El resultado es: {operacion}')
    elif opcion == 3:
        x = numeros()
        time.sleep(0.5)
        y = numeros()
        time.sleep(0.5)
        operacion = x * y
        print(f'El resultado es: {operacion}')
    elif opcion == 4:
        x = numeros()
        time.sleep(0.5)
        y = numeros()
        time.sleep(0.5)
        if y != 0:
            operacion = x / y
            print(f'El resultado es: {operacion}')
        else:
            print("no es posible dividir entre 0")
    elif opcion == 5:
        exit()


def off():

    cap = cv2.VideoCapture(0)  

    mpHands = mp.solutions.hands  
    hands = mpHands.Hands()  
    mpDraw = mp.solutions.drawing_utils

    while True:
        success, img = cap.read()  
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  
        results = hands.process(imgRGB)  

        lmList = []  
        if results.multi_hand_landmarks:  
            for handlandmark in results.multi_hand_landmarks:
                for id, lm in enumerate(handlandmark.landmark):  
                    h, w, _ = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])  
                mpDraw.draw_landmarks(img, handlandmark, mpHands.HAND_CONNECTIONS)

        if lmList != []:
            y1 = lmList[10][2]  # Dedo corazon
            y2 = lmList[8][2]  # Dedo indice
            y3 = lmList[16][2]  # Dedo anular
            y4 = lmList[20][2]  # Dedo meñique

            if y1 < y2 and y1 < y3 and y1 < y4:
                os.system("shutdown /s /t 1")
                break

        cv2.imshow('Image', img)  
        cv2.putText(img, "Apagado", (10, 470), cv2.FONT_ITALIC, 1.5, (255, 255, 255), 2)
        if cv2.waitKey(1) & 0xff == ord(' '):  
            break

    cap.release()  

    cv2.destroyAllWindows()  


# Menu principal
print("Elige una opcion: \n1. Controlar Volumen \n2. Controlar Brillo \n3. Controlar Ventanas \n4. Calculadora "
      "Hexadecimal \n5. Apagar el Computador\n6. Salir del programa\n")

z = 0

while z != 6:
    print("Elige una opcion: \n1. Controlar Volumen \n2. Controlar Brillo \n3. Controlar Ventanas \n4. Calculadora "
          "Hexadecimal \n5. Apagar el Computador\n6. Salir del programa\n")
    z = menu()
    if z == 1:
        volume()
    elif z == 2:
        bright()
    elif z == 3:
        window()
    elif z == 4:
        calculadora()
    elif z == 5:
        off()
    elif z == 6:
        exit()
    else:
        print("Gesto irreconocible")
