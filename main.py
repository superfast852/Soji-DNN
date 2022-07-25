import torch  # For Model
import cv2  # For Cam
import time  # Inference measuring
import local_utils.Label_xtr as Label_xtr  # Custom Label Extractor TODO: Develop Extractor functions
import random
import socket

# Parameter Wall TODO: Add argparse
send_info = False
debug = True  # Enable Function Outputs
one = False
model_type = "v7t"   # Select from: v5s, v5m, v5n, v7, v7t, v5_custom, v7_custom
v5_custom_path = "C:/Users/GG/Desktop/Code/ML/Models/v5s_70/weights/best.pt"  # Path to a YOLOv5 model trained on a custom dataset
v7_custom_path = "prebuilts/custom/v7t_aqua/V2-512-90%/yolov7.pt"  # Path to a YOLOv7 model trained on a custom dataset
custom_yaml = "prebuilts/custom/v7t_aqua/data.yaml"  # Path to the custom dataset's data.yaml file
src = 0  # "Testing/testvid.mp4" or HTTP address
min_conf = 0.01
pixel_threshold = 25
avg_fps = []  # List for Calculating Average FPS at ending
#clr = lambda: (random.randint(0,255), random.randint(0,255), random.randint(0,255))
clr = lambda: (0, 255, 0)
record = False
host = "192.168.43.56"
port = 65432


def infer(frame, model, debug=False):
    results = model(frame)  # infer
    # extract and convert results to list
    dets = results.xyxy[0].tolist()
    #if debug: print(dets)
    return dets


def draw(dets, frame, classes, debug=True, color=(0,255,0)):
    xy1 = (int(dets[0]), int(dets[1]))  # top left point
    xy2 = (int(dets[2]), int(dets[3]))  # bottom right point
    conf, lbl = dets[4:]  # confidence and output label

    cv2.rectangle(frame, xy1, xy2, color, 3, cv2.LINE_AA)  # draw rectangle
    cv2.putText(frame, f"{classes[int(lbl)]}: {conf:.2f}", xy1, cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)  # write label and conf atop rectangle
    if debug:
        print(f"Detection: \n   BBox: {xy1, xy2} \n   Label: {classes[int(lbl)]} \n   Confidence: {conf:.2f}")  # output info
        cx = (dets[2] + dets[0]) / 2  # Center of X
        cy = (dets[3] + dets[1]) / 2  # Center of Y
        cv2.circle(frame, (int(cx), int(cy)), 5, color=color, thickness=-1)


def draw_1(dets, frame, classes, debug=True, color=(0,255,0)):
    xy1 = (int(dets[0]), int(dets[1]))  # top left point
    xy2 = (int(dets[2]), int(dets[3]))  # bottom right point
    conf, lbl = dets[4:]  # confidence and output label

    cv2.rectangle(frame, xy1, xy2, color, 3, cv2.LINE_AA)  # draw rectangle
    cv2.putText(frame, f"{classes[int(lbl)]}: {conf:.2f}", xy1, cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)  # write label and conf atop rectangle
    if debug:
        print(f"Detection: \n   BBox: {xy1, xy2} \n   Label: {classes[int(lbl)]} \n   Confidence: {conf:.2f}")  # output info
        cx = (dets[2] + dets[0]) / 2  # Center of X
        cy = (dets[3] + dets[1]) / 2  # Center of Y
        cv2.circle(frame, (int(cx), int(cy)), 5, color=color, thickness=-1)


def pos_servo(dets, frame, socket_plug, px=25):
    detX = (dets[2] + dets[0]) / 2  # Center of X
    detY = (dets[3] + dets[1]) / 2  # Center of Y
    ccy, ccx = [x/2 for x in frame.shape[:2]]

    if ccx<detX-px: xServ = '-'
    elif ccx>detX+px: xServ = '+'
    else: xServ = "="

    if ccy<detY-px: yServ = '-'
    elif ccy>detY+px: yServ = '+'
    else: yServ = "="

    socket_plug.sendall(xServ + " " + yServ)


def frame_debug(frame, px=25):
    cy, cx = frame.shape[:2]
    ccx = int(cx/2)
    ccy = int(cy/2)
    cv2.rectangle(frame, (ccx-px, ccy-px), (ccx+px, ccy+px), (255, 0, 0), 2, cv2.LINE_AA)

    cv2.line(frame, (0, ccy), (ccx-px, ccy), (0, 0, 255), 2, cv2.LINE_AA)  # left line
    cv2.line(frame, (ccx, 0), (ccx, ccy-px), (0, 0, 255), 2, cv2.LINE_AA)  # upper line
    cv2.line(frame, (ccx+px, ccy), (cx, ccy), (0, 0, 255), 2, cv2.LINE_AA)  # right line
    cv2.line(frame, (ccx, ccy+px), (ccx, cy), (0, 0, 255), 2, cv2.LINE_AA)  # lower line


if __name__ == "__main__":
    try:
        if model_type == 'v5m':
            model = torch.hub.load("ultralytics/yolov5", 'custom', "prebuilts/yolov5m.pt", verbose=debug)

        elif model_type == 'v5s':
            model = torch.hub.load("ultralytics/yolov5", 'custom', "prebuilts/yolov5s.pt", verbose=debug)

        elif model_type == 'v5n':
            model = torch.hub.load("ultralytics/yolov5", 'custom', "prebuilts/yolov5n.pt", verbose=debug)

        elif model_type == "v5_custom":
            model = torch.hub.load('ultralytics/yolov5', 'custom', v5_custom_path, verbose=debug)  # YoloV7 Tiny Model

        elif model_type == 'v7':
            model = torch.hub.load('yolov7', 'custom', "prebuilts/yolov7.pt", source='local', verbose=debug)  # YoloV7 Tiny Model

        elif model_type == 'v7t':
            model = torch.hub.load('yolov7', 'custom', "prebuilts/yolov7t.pt", source='local', verbose=debug)  # YoloV7 Tiny Model

        elif model_type == "v7_custom":
            model = torch.hub.load('yolov7', 'custom', v7_custom_path, source='local', verbose=debug)  # YoloV7 Tiny Model

        # Extract classes from file
        if not model_type.endswith("custom"):
            classes = Label_xtr.getLabelsFromTxt(path="coco-lbl.txt", verbose=debug)  # Coco Labels Extract
        else:
            classes = Label_xtr.getLabelsFromYaml(custom_yaml, verbose=debug)  # AquaTrash Labels
            #classes = Label_xtr.getLabelsFromYaml(custom_yaml, verbose=debug)  # Trash-Filter Labels
            #classes = ['-', 'cardboard', 'glass', 'metal', 'plastic'] #Manual Labels



        # Open Webcam
        vid = cv2.VideoCapture(src)
        if record:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter('Soji-DNN-Out.avi', fourcc, 80.0, (int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)), int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))))
        if send_info:
            print(f"Connecting to {host}:{port}...")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            print("Connection Success!")
        while vid.isOpened():
            start_time = time.time()
            ret, frame = vid.read()  # read webcam image info
            detections = infer(frame, model, debug=debug)  # goto infer function atop

            confs = []
            for i in range(len(detections)):
                # Show Webcam Image with Detection Info
                if not one:
                    if detections[i][4] >= min_conf:
                        draw(detections[i], frame, classes, debug=debug, color=clr())
                confs.append(detections[i][4])

            if confs:
                most_conf_det = confs.index(max(confs))
                if send_info: pos_servo(detections[most_conf_det])
                if one: draw_1(detections[most_conf_det], frame, classes, debug=debug, color=clr())

                if debug:
                    frame_debug(frame, pixel_threshold)
                    if detections[0]: print(f"{detections[most_conf_det][4]:.3f}: {classes[int(detections[most_conf_det][5])]}")

            cv2.imshow("Model Modified Output", frame)
            if record: out.write(frame)
            # FrameRate calculations
            if debug:
                fps = 1 / (time.time() - start_time)
                avg_fps.append(fps)
                print(f"FPS: {fps:.3f}\n")
            if cv2.waitKey(1) & 0xFF == ord('q'): 1/0  # stop process if q is pressed
    except:
        print(f"\nAverage FrameRate: {sum(avg_fps)/len(avg_fps):.3f}")
        vid.release()
        if record: out.release()
        cv2.destroyAllWindows()
