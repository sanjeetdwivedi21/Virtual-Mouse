import cv2
import mediapipe as mp
import math


class HandDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon,
        )
        self.mpDraw = mp.solutions.drawing_utils
        self.results = None
        self.lmList = []

    def findHands(self, img, draw=True):
        """Detect hands and draw landmarks"""
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        """Return list of landmark positions"""
        self.lmList = []
        if self.results.multi_hand_landmarks:
            if handNo < len(self.results.multi_hand_landmarks):
                myHand = self.results.multi_hand_landmarks[handNo]
                h, w, c = img.shape
                for id, lm in enumerate(myHand.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    self.lmList.append([id, cx, cy])
                    if draw:
                        cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lmList, None

    def fingersUp(self):
        """Check which fingers are up"""
        fingers = []
        if len(self.lmList) != 0:
            # Thumb
            if self.lmList[4][1] < self.lmList[3][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            # Fingers (index to pinky)
            tips = [8, 12, 16, 20]
            for tip in tips:
                if self.lmList[tip][2] < self.lmList[tip - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        return fingers

    def findDistance(self, p1, p2, img, draw=True):
        """Find distance between two points"""
        x1, y1 = self.lmList[p1][1], self.lmList[p1][2]
        x2, y2 = self.lmList[p2][1], self.lmList[p2][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        length = math.hypot(x2 - x1, y2 - y1)

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
            cv2.circle(img, (x1, y1), 7, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 7, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), 7, (0, 255, 0), cv2.FILLED)

        return length, img, [x1, y1, x2, y2, cx, cy]