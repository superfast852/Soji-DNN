import torch
import time
verbose = True
if __name__ == "__main__":
    #model = torch.hub.load('WongKinYiu/yolov7', 'custom', 'C:/Users/GG/Downloads/yolov7.pt')
    #model = torch.hub.load("ultralytics/yolov5", "custom", path="C:/Users/GG/Desktop/Code/ML/Models/output_models_v5m_v2/weights/best_openvino_model", verbose=verbose) #custom model cpu
    #model = torch.hub.load("ultralytics/yolov5", "custom", path="C:/Users/GG/Desktop/Code/ML/Models/v5s_70/weights/best_openvino_model", verbose=verbose) #v5s cpu
    img = ["C:/Users/GG/Downloads/testimg.jpg"]
    for i in range(60):
        start = time.time()
        results = model(img)
        print("FPS: ", 1/(time.time()-start))