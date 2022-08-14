import torch
import time
import numpy as np
fps = []
model = torch.hub.load('yolov7', 'custom', 'prebuilts/yolov7-tiny.pt', source='local')
totalstart = time.time()
for i in range(1000):
    start = time.time()
    model("yolov7/inference/images/horses.jpg")
    #model(np.random.uniform(0.0, 1.0, (416, 416)))
    print("Frame ", i)
    fps.append(1/(time.time()-start))
print(f'''Finished processing 1000 frames!
Average Framerate: {sum(fps)/len(fps)} FPS
Total Time: {time.time()-totalstart} Seconds''')