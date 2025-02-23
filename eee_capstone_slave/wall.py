import cv2
import numpy as np
from math import atan2,degrees,sqrt
from numpy import zeros, newaxis

from wall_position_slave import wall_position as m_w_p


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)


    ret, frame = cap.read()
    m_w_p(frame)
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
