import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self, mode=False, max_hands=1, detection_con=0.5, track_con=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.track_con = track_con

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_con,
            min_tracking_confidence=self.track_con
        )
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        return img

    def find_position(self, img, hand_no=0, draw=True):
        lm_list = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(my_hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
        return lm_list

    def fingersUp(self):
        fingers = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[0]
            # Tip identifiers for 4 fingers (Index, Middle, Ring, Pinky)
            tipIds = [8, 12, 16, 20]
            
            # Thumb (Check if tip is to the right/left of knuckle depending on hand)
            # Assuming right hand for simplicity usually works, or check x relative to wrist
            if my_hand.landmark[4].x < my_hand.landmark[3].x: # Left side of thumb
                fingers.append(1)
            else:
                fingers.append(0)

            # 4 Fingers
            for id in range(0, 4):
                 # Check if tip is higher (smaller y) than the pip joint (2 joints down)
                if my_hand.landmark[tipIds[id]].y < my_hand.landmark[tipIds[id] - 2].y:
                    fingers.append(1)
                else:
                    fingers.append(0)
        return fingers

def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetector()
    while True:
        success, img = cap.read()
        if not success:
            break
        img = detector.find_hands(img)
        lm_list = detector.find_position(img)
        if len(lm_list) != 0:
            print(lm_list[8]) # Tip of index finger

        cv2.imshow("Hand Tracker", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
