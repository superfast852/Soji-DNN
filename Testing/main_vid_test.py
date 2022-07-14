import torch
from os import listdir
import cv2
import yaml

txt = False
with open(r"C:/Users/GG/Desktop/Code/ML/Datasets/AquaTrash-yolov5/data.yaml") as file:
    classes = yaml.full_load(file)['names']

model = torch.hub.load('WongKinYiu/yolov7', 'custom', 'C:/Users/GG/Downloads/yolov7.pt')

for i in listdir("C:/Users/GG/Desktop/Code/ML/Datasets/AquaTrash-yolov5/test/images"):
    img = cv2.imread("C:/Users/GG/Desktop/Code/ML/Datasets/AquaTrash-yolov5/test/images/" + i)
    results = model(img)
    dets = results.xyxy[0].tolist()

    for i in dets:
        cv2.rectangle(img, (int(i[0]), int(i[1])), (int(i[2]), int(i[3])), (0,255,0), 3, cv2.LINE_AA)
        if txt: cv2.putText(img, f"{classes[int(i[5])]}: {i[4]:.3f}", (int(i[0]), int(i[1])), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0), 1, cv2.LINE_AA)

    cv2.imshow("Inferenced Images", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()


