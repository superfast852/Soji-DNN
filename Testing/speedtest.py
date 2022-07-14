from time import time
import numpy as np
detections = [np.random.uniform(0.000, 640.000, 6), np.random.uniform(0.000, 640.000, 6)]
progStart = time()
for j in range(10):
    for dets in detections:
        start = time()
        cx = (int(dets[2]) + int(dets[0]))/2
        cy = (int(dets[3]) + int(dets[1]))/2
        conf, lbl = dets[4:]
        print(f"Center of dets: {(cx, cy)}\nConfidence: {conf}\nLabel: {lbl}\nTime of Calc of det: {time()-start}\n")

print("Done! Total Time of 10 reps: ", time()-progStart)
