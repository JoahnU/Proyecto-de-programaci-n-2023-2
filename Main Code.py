# Codigo hecho por Joahn Hernandez, Samuel Luna, Sebastian Rojas y Juan Gomez desde un mismo dispositivo

import cv2
import mediapipe as mp

def detection_h():
  # Se inicia la detección de manos
  hand = mp.solutions.hands.Hands(static_image_mode = False, max_num_hands = 1)
  # Se importa la webcam
  webcam = cv2.VideoCapture(0)
  while True:
    #Se capturan fotogramas
    success, frame = webcam.read()

    #Se detectan las manos en los fotogramas
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hand.process(image)
    #Obteniendo la posicion de la mano
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        # Se dibuja la mano
        mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
    # Se muestra el fotograma con la mano dibujada
    cv2.imshow("Gestos de las manos", frame)
    # Se espera a que se pulse la tecla esc para cerrar el programa
    key = cv2.waitKey(1) & 0xFF
    if key == 27: 
      break
  # Se detiene la webcam
  webcam.release()
  cv2.destroyAllWindows()
if __name__ == "__main__":
  detection_h()
  
  
  
