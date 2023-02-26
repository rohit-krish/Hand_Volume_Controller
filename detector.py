import cv2
import mediapipe as mp


class HandDetector():
    def __init__(self, mode=False, max_hands=2, detection_conf=.5, track_conf=.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_conf = detection_conf
        self.track_conf = track_conf

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode, max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_conf,
            min_tracking_confidence=self.track_conf
        )
        self.lms_draw = mp.solutions.drawing_utils
        self.results = None

    def find_hands(self, img, draw=True):
        # img_h, img_w, _ = img.shape
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            # getting land marks of each hand
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    self.lms_draw.draw_landmarks(
                        img, hand_lms, self.mp_hands.HAND_CONNECTIONS
                    )

        return img

    def get_land_marks(self, img, hand_id=0, draw=False):
        img_h, img_w, _ = img.shape
        land_marks = []

        if self.results.multi_hand_landmarks:
            # only reading one hand
            hand = self.results.multi_hand_landmarks[hand_id]
            for lm in hand.landmark:
                cx, cy = int(lm.x*img_w), int(lm.y*img_h)
                # print(lm.z)
                land_marks.append([cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

        return land_marks
