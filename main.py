import cv2
import numpy as np

class UV:
    def __init__(self):
        self.center = None
        self.radius = None
        self.pose = {'roll': 0, 'pitch': 0, 'yaw': 0}

    def detect_circle(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=100, param1=50, param2=30,
                                   minRadius=10, maxRadius=100)

        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                self.center = (x, y)
                self.radius = r
                cv2.circle(frame, (x, y), r, (0, 255, 0), 4)

        return frame

    def approach_circle(self):
            if self.center is not None:
                target_roll = 0
                target_pitch = 0
                target_yaw = 0

                while not self.is_aligned(target_roll, target_pitch, target_yaw):

                    roll_difference = target_roll - self.pose['roll']

                    if self.center[0] > self.radius:
                        print("Turn Right")
                    elif self.center[0] < self.radius:
                        print("Turn Left")
                    else:
                        print("Move Forward")

                    self.pose['roll'] += roll_difference
                    self.pose['yaw'] += 1
                    self.pose['pitch'] += 1

                    print("Current Pose:", self.pose)

                print("Aligned with target pose.")


    def is_aligned(self, target_roll, target_pitch, target_yaw, tolerance=1):

        return abs(self.pose['roll'] - target_roll) <= tolerance and \
               abs(self.pose['pitch'] - target_pitch) <= tolerance and \
               abs(self.pose['yaw'] - target_yaw) <= tolerance



uv = UV()

video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()

    frame_with_circle = uv.detect_circle(frame)

    cv2.imshow('Frame', frame_with_circle)


    if cv2.waitKey(1) & 0xFF == ord('e'):
        break


video_capture.release()
cv2.destroyAllWindows()
