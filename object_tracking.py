"""
NAME: Robert Renzo Rudio
ID: 005366334

References:
 - Changing color-space:
 https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/
 py_imgproc/py_colorspaces/py_colorspaces.html#converting-colorspaces

 - Finding contours and bounding rectangle:
 https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/
 py_imgproc/py_contours/py_contour_features/py_contour_features.html#contour-features
"""

import argparse
import cv2
import numpy as np
import sys

def track(c_space: str, lower: np.uint8, upper: np.int8):
    cap = cv2.VideoCapture(0)

    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    size = (int(cap.get(3)), int(cap.get(4)))
    out = cv2.VideoWriter('output.mp4', fourcc, 20.0, size)

    while (True):
        ret, frame = cap.read()

        if not ret:
            break

        if c_space == "RGB":
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mask = cv2.inRange(rgb, lower, upper)
        
        else:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower, upper)

        res = cv2.bitwise_and(frame, frame, mask=mask) 
        countours, _ = cv2.findContours(mask, 1, 2)

        for cnt in countours:
            area = cv2.contourArea(cnt)
            if area > 1000:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

        out.write(res)
        cv2.imshow("frame", frame)
        cv2.imshow("res", res)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()

def main():
    usg_msg = "python3 {} -c [RGB|HSV] -l [Lower-Range], -u [Upper-Range]".format(sys.argv[0])
    descr = "Track Object Using RGB or HSV Values."
    parser = argparse.ArgumentParser(usage=usg_msg, description=descr)
    parser.add_argument("-c", type=str, required=True, help="Color Space to be Used (RGB or HSV)")
    parser.add_argument("-l", type=str, required=True, help="Lower Range of the Color in CSV Format")
    parser.add_argument("-u", type=str, required=True, help="Upper Range of the Color in CSV Format")
    args = parser.parse_args()

    # Parse arguments.
    c_space = str.upper(args.c)
    if c_space == "RGB" or c_space == "HSV":
        lower = args.l.split(',')
        lower = np.array([int(i) for i in lower], np.uint8)
        upper = args.u.split(',')
        upper = np.array([int(i) for i in upper], np.uint8)
        track(c_space, lower, upper)
    else:
        print("unrecognized -c option")
        sys.exit(1)
    
if __name__ == "__main__":
    main()
