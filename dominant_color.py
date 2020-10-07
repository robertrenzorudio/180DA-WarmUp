"""
NAME: Robert Renzo Rudio
ID: 005366334

References: 
- getting region of interest in opencv2:
https://techtutorialsx.com/2019/11/24/python-opencv-getting-region-of-interest/
"""

import argparse
import cv2
import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
import sys

def dominant_color(cap: cv2.VideoCapture, pt1: tuple, pt2: tuple):
    x1, y1 = pt1
    x2, y2 = pt2

    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    size = (int(cap.get(3)), int(cap.get(4)))
    out = cv2.VideoWriter('output.mp4', fourcc, 20.0, size)

    while(True):
        ret, frame = cap.read()
       
        if not ret:
            break

        # Get region of interest from frame. 
        roi = frame[y1:y2, x1:x2]
        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)

        # Convert roi to 2d array.
        x, y, z = roi.shape
        roi_2d = roi.reshape(x*y, z)
       
        # Perfrom K-means clustering to find dominant color.
        kmeans = KMeans(n_clusters=3)
        kmeans.fit(roi_2d)
        most_label = np.bincount(kmeans.labels_).argmax()
        dc = [int(i) for i in kmeans.cluster_centers_[most_label]]
        
        # Draw rectangle and print dominant color.
        rect_color = (dc[2], dc[1], dc[0])
        rect = cv2.rectangle(frame, (x1, y1), (x2, y2), rect_color, 2)
        cv2.putText(rect, "Dominant RGB: {}".format(dc), (x1, y1), 0, 0.5, rect_color)
        print(dc)

        out.write(frame)
        cv2.imshow("frame", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    out.release()
    return 

def main():
    usg_msg = "python3 {} -p [Starting-Point: x,y] -w [Width] -l [Height]\n".format(sys.argv[0])
    descr = "Print Dominant Color Inside a Rectangle."
    parser = argparse.ArgumentParser(usage=usg_msg, description=descr)
    parser.add_argument("-p", type=str, required=False, help="Starting point of Rectangle (Centered by Default)")
    parser.add_argument("-w", type=str, required=False, help="Width of Rectangle (Default = 250)")
    parser.add_argument("-l", type=str, required=False, help="Height of Rectangle (Default = 250)")
    args = parser.parse_args()
    

    # Parse Arguments.
    w = int(args.w) if args.w else 250
    h = int(args.l) if args.l else 250 
    cap = cv2.VideoCapture(0)

    if args.p:
        pt1 = args.p.split(",")
        pt1 = (int(pt1[0]), int(pt1[1]))
    else:
        pt1 = (int(cap.get(3))//2 - w//2, int(cap.get(4))//2 - h//2)

    pt2 = (pt1[0] + w, pt1[1] + h)
    
    dominant_color(cap, pt1, pt2)
   
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
