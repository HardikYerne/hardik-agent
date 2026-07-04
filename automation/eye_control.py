import cv2
import pyautogui
import time
import threading
import numpy as np

pyautogui.FAILSAFE = False

# eye landmark indices
LEFT_EYE_TOP = 386
LEFT_EYE_BOTTOM = 374
RIGHT_EYE_TOP = 159
RIGHT_EYE_BOTTOM = 145
LEFT_IRIS = [474, 475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]
LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]

BLINK_THRESHOLD = 0.25
BLINK_COOLDOWN = 0.5
SCROLL_SPEED = 5

class EyeController:
    def __init__(self):
        self.is_running = False
        self.cap = None
        self.last_blink_time = 0
        self.blink_count = 0
        self.blink_timer = 0
        self.screen_w, self.screen_h = pyautogui.size()
        self.last_action = ''
        self.gaze_history = []
        self.face_mesh = None

    def init_mediapipe(self):
        try:
            import mediapipe as mp
            self.face_mesh = mp.solutions.face_mesh.FaceMesh(
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=0.7,
                min_tracking_confidence=0.7
            )
            return True
        except Exception as e:
            print(f'MediaPipe error: {e}')
            return False

    def get_ear(self, landmarks, top_idx, bottom_idx, h):
        top_y = landmarks[top_idx].y * h
        bottom_y = landmarks[bottom_idx].y * h
        return abs(top_y - bottom_y) / h

    def get_iris_pos(self, landmarks, iris_idx, eye_idx):
        iris_x = sum(landmarks[i].x for i in iris_idx) / len(iris_idx)
        iris_y = sum(landmarks[i].y for i in iris_idx) / len(iris_idx)
        eye_x_min = min(landmarks[i].x for i in eye_idx)
        eye_x_max = max(landmarks[i].x for i in eye_idx)
        eye_y_min = min(landmarks[i].y for i in eye_idx)
        eye_y_max = max(landmarks[i].y for i in eye_idx)
        if eye_x_max - eye_x_min == 0:
            return 0.5, 0.5
        rel_x = (iris_x - eye_x_min) / (eye_x_max - eye_x_min)
        rel_y = (iris_y - eye_y_min) / (eye_y_max - eye_y_min)
        return rel_x, rel_y

    def smooth(self, x, y):
        self.gaze_history.append((x, y))
        if len(self.gaze_history) > 5:
            self.gaze_history.pop(0)
        avg_x = sum(p[0] for p in self.gaze_history) / len(self.gaze_history)
        avg_y = sum(p[1] for p in self.gaze_history) / len(self.gaze_history)
        return avg_x, avg_y

    def process_frame(self, frame):
        import mediapipe as mp
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb)
        h, w = frame.shape[:2]

        if not results.multi_face_landmarks:
            cv2.putText(frame, 'No face detected', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            return frame

        landmarks = results.multi_face_landmarks[0].landmark
        left_ear = self.get_ear(landmarks, LEFT_EYE_TOP, LEFT_EYE_BOTTOM, h)
        right_ear = self.get_ear(landmarks, RIGHT_EYE_TOP, RIGHT_EYE_BOTTOM, h)
        both_blink = left_ear < BLINK_THRESHOLD and right_ear < BLINK_THRESHOLD
        current_time = time.time()

        if both_blink and current_time - self.last_blink_time > BLINK_COOLDOWN:
            self.last_blink_time = current_time
            self.blink_count += 1
            if self.blink_count >= 2:
                pyautogui.doubleClick()
                self.last_action = 'Double blink - Double click'
                self.blink_count = 0
            else:
                pyautogui.click()
                self.last_action = 'Single blink - Click'

        if current_time - self.last_blink_time > 0.5:
            self.blink_count = 0

        try:
            lx, ly = self.get_iris_pos(landmarks, LEFT_IRIS, LEFT_EYE)
            rx, ry = self.get_iris_pos(landmarks, RIGHT_IRIS, RIGHT_EYE)
            avg_x = (lx + rx) / 2
            avg_y = (ly + ry) / 2
            sx, sy = self.smooth(avg_x, avg_y)

            if sx < 0.35:
                pyautogui.scroll(SCROLL_SPEED)
                self.last_action = 'Look left - Scroll up'
            elif sx > 0.65:
                pyautogui.scroll(-SCROLL_SPEED)
                self.last_action = 'Look right - Scroll down'

            cx = int(sx * self.screen_w)
            cy = int(sy * self.screen_h)
            cx = max(0, min(self.screen_w - 1, cx))
            cy = max(0, min(self.screen_h - 1, cy))
            pyautogui.moveTo(cx, cy, duration=0.05)
        except:
            pass

        for idx in LEFT_EYE + RIGHT_EYE:
            x = int(landmarks[idx].x * w)
            y = int(landmarks[idx].y * h)
            cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

        for idx in LEFT_IRIS + RIGHT_IRIS:
            x = int(landmarks[idx].x * w)
            y = int(landmarks[idx].y * h)
            cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)

        cv2.putText(frame, f'Action: {self.last_action}',
            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(frame, f'EAR L:{left_ear:.2f} R:{right_ear:.2f}',
            (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        cv2.putText(frame, 'Press Q to stop',
            (10, h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 255), 1)

        return frame

    def run(self):
        if not self.init_mediapipe():
            print('MediaPipe failed to initialize')
            return

        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.is_running = True
        print('Eye control started. Press Q to stop.')

        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            frame = self.process_frame(frame)
            cv2.imshow('Hexa Eye Control', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.stop()

    def start(self):
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()
        return 'Eye control started. Camera window opened. Blink to click. Look left or right to scroll. Press Q to stop.'

    def stop(self):
        self.is_running = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        return 'Eye control stopped.'

eye_controller = EyeController()

def start_eye_control():
    return eye_controller.start()

def stop_eye_control():
    return eye_controller.stop()