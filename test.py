from cv2 import cv2 # fixes some pycharm visual bugs
import mediapipe as mp


class HandDetection():
    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
        self.count = 0
        self.no_hand = 0
        self.i_finger = []

    def findHands(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLMS in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, handLMS, self.mpHands.HAND_CONNECTIONS)
        return img

    def swipeDetection(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLMS in self.results.multi_hand_landmarks:
                for pos, lm in enumerate(handLMS.landmark):
                    height, width, center = img.shape
                    centerX, centerY = int(lm.x * width), int(lm.y * height)
                    if pos == 8:
                        cv2.circle(img, (centerX, centerY), 15, (0, 255, 242), cv2.FILLED)
                        if self.count < 2:
                            self.i_finger.append(centerX)
                            self.count += 1
                        else:
                            del self.i_finger[0]
                            self.i_finger.append(centerX)
                            if self.i_finger[0] - self.i_finger[1] >= 100:
                                print("swipe right")
                            if self.i_finger[0] - self.i_finger[1] <= -100:
                                print("swipe left")
        else:
            if self.no_hand <= 15:
                self.no_hand += 1
                if self.no_hand >= 15:
                    self.count = 0
                    self.i_finger.clear()


def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetection()

    while True:

        success, img = cap.read()
        # img = detector.findHands(img)
        detector.swipeDetection(img)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
