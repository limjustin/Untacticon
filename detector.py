from imutils.video import VideoStream
from imutils import face_utils
import imutils
import dlib
import cv2
import time
from queue import Queue
from scipy.spatial import distance as dist
import numpy as np


class MyDetector:

    state = 1

    # left 관련
    LEFT_COUNTER = 0
    LEFT_CONSEC_FRAMES = 100

    #### sleep 관련
    COUNTER = 0
    TOTAL = 0

    EYE_AR_THRESH = 0.3
    SLEEP_CONSEC_FRAMES = 30

    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    #### yes/no/doubt 관련
    # define movement threshodls
    max_head_movement = 20
    movement_threshold = 50
    x_gesture_threshold = 80
    y_gesture_threshold = 80  # Yes Gesture Threshold

    gesture = False
    x_movement = 1
    y_movement = 1
    gesture_show = 20  # number of frames a gesture is shown

    stop_cnt = 0
    font = cv2.FONT_HERSHEY_SIMPLEX

    # 전역 변수로 설정해서 for문에서 빼오기
    x_center = 0
    y_center = 0
    p0 = 0
    p1 = 0

    x_up = 0
    y_up = 0
    x_down = 0
    y_down = 0

    a_cot = 0
    b_cot = 0

    gradient_a = 1
    gradient_b = 1

    keep_cnt = 0

    def get_coords(self, p1):
        try:
            return int(p1[0][0][0]), int(p1[0][0][1])
        except:
            return int(p1[0][0]), int(p1[0][1])

    def maximum(self, n1, n2):
        if (n1 > n2):
            return n1
        else:
            return n2

    def get_ear(self, eye):
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        C = dist.euclidean(eye[0], eye[3])
        ear = (A + B) / (2.0 * C)
        return ear

    def detect_sleep(self, shape, frame, state, state_changed):
        leftEye = shape[self.lStart: self.lEnd]
        rightEye = shape[self.rStart:self.rEnd]
        leftEAR = self.get_ear(leftEye)
        rightEAR = self.get_ear(rightEye)

        ear = (leftEAR + rightEAR) / 2.0

        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)

        # 졸음 감지
        if ear < self.EYE_AR_THRESH:  # 눈을 감았을 때
            self.COUNTER += 1

            # 눈을 계속 감고 있는 경우 -> 졸음이라고 판단
            if self.COUNTER >= self.SLEEP_CONSEC_FRAMES:
                self.state = 3

        else:  # 눈을 떴을 때
            self.COUNTER = 0
            self.state = 1

    def video(self, detect, detect_changed, state, state_changed):
        ###
        lk_params = dict(winSize=(15, 15),
                         maxLevel=2,
                         criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        ###

        # 모델 불러오기
        print('load model...')
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor("public/shape_predictor_68_face_landmarks.dat")

        # video stream 시작
        print('start video stream')
        cap = cv2.VideoCapture(0)

        time.sleep(2.0)

        print('start detecting')
        while True:

            # 인식 여부 (detect) 관련
            if self.keep_cnt <= 0 :
                detect = "0"



            ret, old_frame = cap.read()
            old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)  # from color to black and white

            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            rects = detector(gray, 0)

            for rect in rects:
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)

                # 일반 상태로
                if self.keep_cnt <= 0 :
                    self.state = 1

                # 졸음 감지
                if self.keep_cnt <= 0 :
                    self.detect_sleep(shape, frame, state, state_changed)

                # 인식 됐을 때 관련 변수 변경
                detect = "1"
                self.LEFT_COUNTER = 0

                self.x_center, self.y_center = shape[30]  # 34는 너무 콧구멍
                self.x_up, self.y_up = shape[28]
                self.x_down, self.y_down = shape[8]

                ## 찾은 좌표 사용하여 광학 흐름 측정하기
                face_up = self.x_up, self.y_up
                p0_up = np.array([[face_up]], np.float32)
                face_center = self.x_center, self.y_center  # 특정 부위 좌표 저장
                p0_center = np.array([[face_center]], np.float32)  # Numpy array로 형변환
                face_down = self.x_down, self.y_down
                p0_down = np.array([[face_down]], np.float32)

                p1_up, st, err = cv2.calcOpticalFlowPyrLK(old_gray, gray, p0_up, None, **lk_params)
                p1_center, st, err = cv2.calcOpticalFlowPyrLK(old_gray, gray, p0_center, None, **lk_params)
                p1_down, st, err = cv2.calcOpticalFlowPyrLK(old_gray, gray, p0_down, None, **lk_params)

                # cv2.circle(frame, self.get_coords(p0_up), 3, (0, 255, 0))
                # cv2.circle(frame, self.get_coords(p1_up), 3, (255, 0, 0), -1)
                # cv2.circle(frame, self.get_coords(p0_center), 3, (0, 0, 255))
                # cv2.circle(frame, self.get_coords(p1_center), 3, (255, 0, 0), -1)
                # cv2.circle(frame, self.get_coords(p0_down), 3, (0, 255, 0))
                # cv2.circle(frame, self.get_coords(p1_down), 3, (255, 0, 0), -1)

                ## 정수로 좌표화
                a_up, b_up = self.get_coords(p0_up), self.get_coords(p1_up)
                a_down, b_down = self.get_coords(p0_down), self.get_coords(p1_down)
                a, b = self.get_coords(p0_center), self.get_coords(p1_center)

                ## 움직임 최소화하기
                if abs(a[0] - b[0]) > 5 or abs(a[1] - b[1]) > 5 and self.x_movement > 0 and self.y_movement > 0:  # 이것에 대한 임계값은 해보면서 계속 찾아보기
                    self.x_movement += abs(a[0] - b[0])
                    self.y_movement += abs(a[1] - b[1])
                    self.gradient_a += (self.x_movement / self.y_movement) + 1
                    self.gradient_b += (self.y_movement / self.x_movement) + 1
                    self.stop_cnt = 0  # 움직임 감지 되었다면 count 초기화
                else :
                    self.stop_cnt += 1  # 움직임 감지 안될 때 count 진행

                ## movement 글씨로 표시
                # text = 'x_movement: ' + str(self.x_movement)
                # if not self.gesture: cv2.putText(frame, text, (50, 50), self.font, 0.8, (0, 0, 255), 2)  # x_movement 글씨 표시
                # text = 'y_movement: ' + str(self.y_movement)
                # if not self.gesture: cv2.putText(frame, text, (50, 100), self.font, 0.8, (0, 0, 255), 2)  # y_movement 글씨 표시

                if self.x_movement > self.x_gesture_threshold or self.y_movement > self.y_gesture_threshold:
                    if self.x_movement > self.x_gesture_threshold and self.keep_cnt <= 0:
                        self.gesture = 'No'
                        self.keep_cnt = 20
                        self.state = 6  # No

                    if self.y_movement > self.y_gesture_threshold and self.keep_cnt <= 0:
                        self.gesture = 'Yes'
                        self.keep_cnt = 20
                        self.state = 5  # Yes

                else:
                    if abs(a_up[0] - a_down[0]) >= 1 and abs(b_up[0] - b_down[0]) >= 1:
                        self.a_cot = abs(a_up[0] - a_down[0]) / abs(a_up[1] - a_down[1]) * 100
                        self.b_cot = abs(b_up[0] - b_down[0]) / abs(b_up[1] - b_down[1]) * 100

                        if abs(self.a_cot - self.b_cot) > 6 and abs(self.a_cot - self.b_cot) < 20 and self.maximum(self.gradient_a / self.gradient_b, self.gradient_b / self.gradient_a) < 8 and self.keep_cnt <= 0:
                            self.gesture = 'Doubt'
                            self.keep_cnt = 20
                            self.state = 2  # Doubt

                # text = 'gradient_a: ' + str(self.gradient_a)
                # if not self.gesture: cv2.putText(frame, text, (50, 150), self.font, 0.8, (255, 0, 0), 2)
                # text = 'gradient_b: ' + str(self.gradient_b)
                # if not self.gesture: cv2.putText(frame, text, (50, 200), self.font, 0.8, (255, 0, 0), 2)
                # text = 'Doubt: ' + str(abs(self.a_cot - self.b_cot))
                # if not self.gesture: cv2.putText(frame, text, (50, 250), self.font, 0.8, (255, 0, 0), 2)

                if self.gesture and self.gesture_show > 0:
                    # cv2.putText(frame, 'Gesture Detected: ' + self.gesture, (50, 50), self.font, 1.2, (0, 0, 255), 3)
                    self.gesture_show -= 1

                if self.gesture_show == 0:
                    self.gesture = False
                    self.x_movement = 1
                    self.y_movement = 1
                    self.gradient_a = 1
                    self.gradient_b = 1
                    self.gesture_show = 20  # number of frames a gesture is shown

                if self.stop_cnt > 30:
                    self.x_movement = 1
                    self.y_movement = 1
                    self.gradient_a = 1
                    self.gradient_b = 1
                    self.stop_cnt = 0

            self.keep_cnt -= 1

            # 자리 비움 관련
            self.LEFT_COUNTER += 1

            if self.LEFT_COUNTER > self.LEFT_CONSEC_FRAMES:
                self.state = 4

            state_changed.emit('{}'.format(self.state))
            detect_changed.emit('{}'.format(detect))

            cv2.imshow("webcam", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

if __name__=='__main__':
    q = Queue()
    md = MyDetector()
    md.video(q)

