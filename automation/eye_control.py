import cv2
import mediapipe as mp
import pyautogui
import time
import threading
import numpy as np

pyautogui.FAILSAFE = False

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# eye landmark indices
LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
LEFT_IRIS = [474, 475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]

# blink detection
LEFT_EYE_TOP = 386
LEFT_EYE_BOTTOM = 374
RIGHT_EYE_TOP = 159
RIGHT_EYE_BOTTOM = 145

BLINK_THRESHOLD = 0.25
BLINK_COOLDOWN = 0.5
DOUBLE_BLINK_TIME = 0.4
SCROLL_THRESHOLD = 0.35
SCROLL_SPEED = 5

class EyeController:
    def __init__(self):
        self.is_running = False
        self.cap = None
        self.last_blink_time = 0
        self.blink_count = 0
        self.blink_timer = 0
        self.screen_w, self.screen_h = pyautogui.size()
        self.status = 'stopped'
        self.last_action = ''
        self.smoothing = 5
        self.gaze_history = []

    def get_ear(self, landmarks, eye_top, eye_bottom, img_h, img_w):
        top = landmarks[eye_top]
        bottom = landmarks[eye_bottom]
        top_y = top.y * img_h
        bottom_y = bottom.y * img_h
        ear = abs(top_y - bottom_y) / img_h
        return ear

    def get_iris_position(self, landmarks, iris_indices, eye_indices, img_w, img_h):
        iris_x = sum(landmarks[i].x for i in iris_indices) / len(iris_indices)
        iris_y = sum(landmarks[i].y for i in iris_indices) / len(iris_indices)
        eye_x_min = min(landmarks[i].x for i in eye_indices)
        eye_x_max = max(landmarks[i].x for i in eye_indices)
        eye_y_min = min(landmarks[i].y for i in eye_indices)
        eye_y_max = max(landmarks[i].y for i in eye_indices)
        if eye_x_max - eye_x_min == 0:
            return 0.5, 0.5
        rel_x = (iris_x - eye_x_min) / (eye_x_max - eye_x_min)
        rel_y = (iris_y - eye_y_min) / (eye_y_max - eye_y_min)
        return rel_x, rel_y

    def smooth_position(self, x, y):
        self.gaze_history.append((x, y))
        if len(self.gaze_history) > self.smoothing:
            self.gaze_history.pop(0)
        avg_x = sum(p[0] for p in self.gaze_history) / len(self.gaze_history)
        avg_y = sum(p[1] for p in self.gaze_history) / len(self.gaze_history)
        return avg_x, avg_y

    def process_frame(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)
        h, w = frame.shape[:2]

        if not results.multi_face_landmarks:
            return frame

        landmarks = results.multi_face_landmarks[0].landmark

        left_ear = self.get_ear(landmarks, LEFT_EYE_TOP, LEFT_EYE_BOTTOM, h, w)
        right_ear = self.get_ear(landmarks, RIGHT_EYE_TOP, RIGHT_EYE_BOTTOM, h, w)

        left_blink = left_ear < BLINK_THRESHOLD
        right_blink = right_ear < BLINK_THRESHOLD
        both_blink = left_blink and right_blink

        current_time = time.time()

        if both_blink:
            if current_time - self.last_blink_time > BLINK_COOLDOWN:
                self.blink_count += 1
                self.last_blink_time = current_time
                self.blink_timer = current_time

                if self.blink_count == 1:
                    pyautogui.click()
                    self.last_action = 'Single blink - Click'
                    print('Action: Single click')

                elif self.blink_count == 2:
                    if current_time - self.blink_timer < DOUBLE_BLINK_TIME:
                        pyautogui.doubleClick()
                        self.last_action = 'Double blink - Double click'
                        print('Action: Double click')
                    self.blink_count = 0

        if current_time - self.blink_timer > DOUBLE_BLINK_TIME:
            self.blink_count = 0

        # get iris position for gaze direction
        try:
            left_rel_x, left_rel_y = self.get_iris_position(
                landmarks, LEFT_IRIS, LEFT_EYE, w, h)
            right_rel_x, right_rel_y = self.get_iris_position(
                landmarks, RIGHT_IRIS, RIGHT_EYE, w, h)

            avg_x = (left_rel_x + right_rel_x) / 2
            avg_y = (left_rel_y + right_rel_y) / 2

            smooth_x, smooth_y = self.smooth_position(avg_x, avg_y)

            # gaze direction detection
            if smooth_x < 0.35:
                pyautogui.scroll(SCROLL_SPEED)
                self.last_action = 'Look left - Scroll up'
            elif smooth_x > 0.65:
                pyautogui.scroll(-SCROLL_SPEED)
                self.last_action = 'Look right - Scroll down'

            # move cursor with eyes
            cursor_x = int(smooth_x * self.screen_w)
            cursor_y = int(smooth_y * self.screen_h)
            cursor_x = max(0, min(self.screen_w - 1, cursor_x))
            cursor_y = max(0, min(self.screen_h - 1, cursor_y))
            pyautogui.moveTo(cursor_x, cursor_y, duration=0.1)

        except Exception as e:
            pass

        # draw eye landmarks on frame
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
        cv2.putText(frame, f'L-EAR: {left_ear:.2f} R-EAR: {right_ear:.2f}',
            (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)

        return frame

    def run(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.is_running = True
        self.status = 'running'
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
        return 'Eye control started. Look at screen to control cursor. Blink to click.'

    def stop(self):
        self.is_running = False
        self.status = 'stopped'
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        return 'Eye control stopped.'

eye_controller = EyeController()

def start_eye_control():
    return eye_controller.start()

def stop_eye_control():
    return eye_controller.stop()