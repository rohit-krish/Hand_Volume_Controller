from detector import HandDetector
import cv2
import numpy as np
from subprocess import call

path = 1
cap = cv2.VideoCapture(path)
detector = HandDetector(max_hands=1)


class VolumeRemember:
    def __init__(self) -> None:
        self.curr_volume = 100

    def is_good_to_change(self, curr):
        if curr == self.curr_volume:
            return False
        else:
            self.curr_volume = curr
            return True

remember = VolumeRemember()


def draw(img, points=None, percent=None, scale=.7):
    # bold the points
    if points:
        for pnt in points:
            cv2.circle(img, (pnt[0], pnt[1]), 8, (255, 0, 0), -1)

        # draw line b/w them
        cv2.line(img, points[0], points[1], (255, 0, 0), 2)

    # show the percent
    percent = 100 if percent == None else percent
    cv2.rectangle(
        img, (0, 0), (int(355*scale), int(50*scale)),
        (100, 46, 21), cv2.FILLED
    )
    cv2.putText(
        img, f'Volume: {percent:<3}%', (int(10*scale), int(40*scale)),
        cv2.FONT_HERSHEY_SIMPLEX, 1.5*scale, (255, 255, 255), int(2*scale)
    )


def get_dist_in_percent(lm_list, close=20, far=170):
    thumb = lm_list[4]
    fore = lm_list[8]
    x_dist = abs(fore[0] - thumb[0])
    y_dist = abs(fore[1] - thumb[1])
    dist = np.sqrt(x_dist**2 + y_dist**2)
    dist = 0 if (dist-close) < 0 else dist-close
    dist_in_percent = (dist*100)/far
    dist_in_percent = 100 if dist_in_percent > 100 else dist_in_percent
    return int(dist_in_percent)


while True:
    read, img = cap.read()
    if not read or cv2.waitKey(1) == ord('q'):
        break

    img = detector.find_hands(img)
    lm_list = detector.get_land_marks(img)
    lm_list = np.array(lm_list, dtype=np.int32)

    if lm_list.shape != (0,):
        percent = get_dist_in_percent(lm_list)
        draw(img, [lm_list[4], lm_list[8]], percent)
    else:
        percent = 100
        draw(img, percent=None)

    # change volume
    if remember.is_good_to_change(percent):
        call(["amixer", "-D", "pulse", "sset", "Master", f"{percent}%"])

    cv2.imshow(str(path), img)
