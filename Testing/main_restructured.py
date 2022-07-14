import torch #For Model
import cv2 #For Cam
import time #Inference measuring
import Label_xtr #Custom Label Extractor TODO: Develop Extractor functions


verbose = True #Enable Function Outputs


def infer(frame, model, verbose=True):

    results = model(frame) #infer
    # extract and convert results to list
    dets = results.xyxy[0].tolist()
    return dets

def draw(dets, frame, classes, point=True, verbose=True):
    xy1 = (int(dets[0]), int(dets[1])) #top left point
    xy2 = (int(dets[2]), int(dets[3])) #bottom right point
    conf, lbl = dets[4:] #confidence and output label

    cv2.rectangle(frame, xy1, xy2, (0,255,0), 3, cv2.LINE_AA) #draw rectangle
    cv2.putText(frame, f"{classes[int(lbl)]}: {conf:.2f}", xy1, cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2) #write label and conf atop rectangle

    if point:
        cx = (dets[2] + dets[0])/2 #Center of X
        cy = (dets[3] + dets[1])/2 #Center of Y
        cv2.circle(frame, (int(cx), int(cy)), 5, color = (0,0,255), thickness=-1)
    if verbose:
        print(f"Detection: \n   BBox: {xy1, xy2} \n   Label: {classes[int(lbl)]} \n   Confidence: {conf:.2f} \n" ) #output info

def pos_servo(dets, frame):
    #from adafruit_servokit import ServoKit
    #pca = ServoKit(channels=8)
    detX = (dets[2] + dets[0]) / 2  # Center of X
    detY = (dets[3] + dets[1]) / 2  # Center of Y
    ccy, ccx = [x/2 for x in frame.shape[:2]]
    xServ = 90
    yServ = 90

    if ccx<detX-50: xServ += 5
    if ccx>detX+50: xServ -= 5
    if ccy<detY-50: yServ += 5
    if ccy>detY+50: yServ -+5

    return [xServ, yServ]

if __name__ == "__main__":
    # Load Model (ONLY UNCOMMENT 1)

    #CPU
    #model = torch.hub.load("ultralytics/yolov5", "custom", path="C:/Users/GG/Desktop/Code/ML/Models/output_models_v5m_v2/weights/best_openvino_model", verbose=verbose) #custom model cpu
    #model = torch.hub.load("ultralytics/yolov5", "custom", path="C:/Users/GG/Desktop/Code/ML/Models/v5s_70/weights/best_openvino_model", verbose=verbose) #v5s cpu
    #CUDA
    #model = torch.hub.load("ultralytics/yolov5", "custom", path="C:/Users/GG/Desktop/Code/ML/Models/output_models_v5m_v2/weights/best.pt", device=0, verbose=verbose) #custom model cuda
    #model = torch.hub.load("ultralytics/yolov5", "custom", path="C:/Users/GG/Desktop/Code/ML/Models/v5s_70/weights/best.pt", device=0, verbose=verbose) #v5s cuda

    #Standard Model
    model = torch.hub.load('ultralytics/yolov5', 'yolov5n', verbose=verbose) #Standard v5s model (COCO)

    #Extract classes from file
    classes = Label_xtr.getLabelsFromTxt(path="coco-lbl.txt", verbose=verbose) #replaceable with class list
    #classes = ['-', 'cardboard', 'glass', 'metal', 'plastic']

    #Open Webcam
    vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    vid.open(0)

    while vid.isOpened():
        start_time = time.time()
        ret, frame = vid.read() #read webcam image info

        detections = infer(frame, model, verbose=verbose) #goto infer function atop


        for dets in detections:
            #Show Webcam Image with Detection Info
            draw(dets, frame, classes, point=False, verbose=verbose)


        cv2.imshow("Model Modified Output", frame)
        print("FPS: ", 1/(time.time()-start_time))
        if cv2.waitKey(1) & 0xFF == ord('q'): #stop process if q is pressed
            break


vid.release()
cv2.destroyAllWindows()