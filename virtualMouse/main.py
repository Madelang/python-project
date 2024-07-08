import cv2
import mediapipe as mp
import time
import pyautogui
import threading

pyautogui.FAILSAFE = False

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
cap.set(cv2.CAP_PROP_FPS, 30)

mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()

def process_frame(frame):
    thumb_index_close = False
    pTime = time.time()

    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    output = hands.process(rgb_frame)
    hands_landmarks = output.multi_hand_landmarks

    if hands_landmarks:
        hand1 = hands_landmarks[0]
        mpDraw.draw_landmarks(frame, hand1)
        landmarks1 = hand1.landmark

        thumb_x, thumb_y = 0, 0
        index_x, index_y = 0, 0
        ring_x, ring_y = 0, 0

        for id, landmark in enumerate(landmarks1):
            x = int(landmark.x * frame_width)
            y = int(landmark.y * frame_height)

            if id == 8:
                cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255), thickness=-1)
                index_x = screen_width / frame_width * x
                index_y = screen_height / frame_height * y

            if id == 4:
                cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255), thickness=-1)
                thumb_x = screen_width / frame_width * x
                thumb_y = screen_height / frame_height * y

            if id == 16:
                cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 0), thickness=-1)
                ring_x = screen_width / frame_width * x
                ring_y = screen_height / frame_height * y
                pyautogui.moveTo(ring_x, ring_y)

        if abs(index_y - thumb_y) < 20:
            if not thumb_index_close:
                pyautogui.mouseDown()
                thumb_index_close = True
        else:
            if thumb_index_close:
                pyautogui.mouseUp()
                thumb_index_close = False

    cv2.putText(frame, str(int(1 / (time.time() - pTime))), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    return frame

def camera_thread():
    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        frame = process_frame(frame)

        cv2.imshow("Image", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.01)  # Membuat sedikit delay untuk mengontrol FPS

# Mulai thread kamera
thread = threading.Thread(target=camera_thread)
thread.start()

# Tunggu sampai thread selesai
thread.join()

cap.release()
cv2.destroyAllWindows()
