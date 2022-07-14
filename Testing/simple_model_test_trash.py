import cv2
import torch
import time
import Label_xtr
verbose = True
if __name__ == "__main__":
    model = torch.hub.load('WongKinYiu/yolov7', 'custom', 'C:/Users/GG/Desktop/Code/ML/Models/v7t_p5hyps_aqua/yolov7.pt')
    #model = torch.hub.load("ultralytics/yolov5", "custom", path="C:/Users/GG/Desktop/Code/ML/Models/output_models_v5m_v2/weights/best_openvino_model", verbose=verbose) #custom model cpu
    #model = torch.hub.load("ultralytics/yolov5", "custom", path="C:/Users/GG/Desktop/Code/ML/Models/v5s_70/weights/best_openvino_model", verbose=verbose) #v5s cpu
    vid = cv2.VideoCapture("C:/Users/GG/PycharmProjects/testvid.mp4")
    while vid.isOpened():
        ret, img = vid.read()
        results = model(img)
        dets = results.xyxy[0].tolist()
        for i in dets:
            cv2.rectangle(img, (int(i[0]), int(i[1])), (int(i[2]), int(i[3])), (0,255,0), 3, cv2.LINE_AA)
            cv2.putText(img, f"{i[5]}: {i[4]}", (int(i[0]), int(i[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        results.print()
        cv2.imshow("vid", img)
        cv2.waitKey(1)