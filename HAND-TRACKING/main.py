import cv2
import mediapipe as mp
import pyautogui

# Inisialisasi MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Fungsi untuk menghitung jumlah jari yang terbuka
def count_fingers(landmarks):
    finger_tips = [4, 8, 12, 16, 20]  # Ujung jari: ibu jari, telunjuk, tengah, manis, kelingking
    fingers_open = 0

    # Ibu jari
    if landmarks[finger_tips[0]].x < landmarks[finger_tips[0] - 1].x:
        fingers_open += 1

    # Jari lainnya
    for tip in finger_tips[1:]:
        if landmarks[tip].y < landmarks[tip - 2].y:
            fingers_open += 1

    return fingers_open

# Inisialisasi webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Atur resolusi
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

last_fingers_count = -1  # Variabel untuk melacak jumlah jari sebelumnya

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = hand_landmarks.landmark
            fingers_count = count_fingers(landmarks)

            cv2.putText(frame, f"Fingers: {fingers_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Kirim input keyboard hanya jika jumlah jari berubah
            if fingers_count != last_fingers_count:
                if fingers_count == 5:
                    pyautogui.press('up')  # Panah atas
                    cv2.putText(frame, f"Lompat", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                elif fingers_count == 2:
                    pyautogui.press('left')  # Panah kiri
                elif fingers_count == 1:
                    pyautogui.press('right')  # Panah kanan
                elif fingers_count == 3:
                    pyautogui.press('down')  # Panah bawah

                last_fingers_count = fingers_count  # Update jumlah jari terakhir

    cv2.imshow("Hand Gesture Control", frame)

    if cv2.waitKey(30) & 0xFF == ord('q'):  # Tambahkan delay 30ms
        break

cap.release()
cv2.destroyAllWindows()