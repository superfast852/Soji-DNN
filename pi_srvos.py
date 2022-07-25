from local_utils.PiStream import stream
import multiprocessing
from adafruit_servokit import ServoKit
pca = ServoKit(channels=8)
servo_angle = [90, 90, 90]
x = pca.servo[0]
y1 = pca.servo[1]
y2 = pca.servo[2]


def servos():
    import socket

    HOST = "192.168.43.56"
    PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")

            while True:
                data = conn.recv(1024)
                if not data: break
                conn.sendall(data)
                a = data.split(" ")

                for axis in range(len(a)):
                    if a[axis] == '+':
                        servo_angle[axis] += 5
                    elif a[axis] == '-':
                        servo_angle[axis] -= 5

                if a[1] != "=":
                    b = servo_angle[1] - 90
                    servo_angle[2] = 90 - b

                for i in servo_angle:
                    if i > 180: i = 180
                    elif i < 0: i = 0

                x.angle = servo_angle[0]
                y1.angle = servo_angle[1]
                y2.angle = servo_angle[2]


servos = multiprocessing.Process(target=servos)
stream = multiprocessing.Process(target=stream)

if __name__ == "__main__":
    servos.start()
    stream.start()
    servos.join()
    stream.join()

