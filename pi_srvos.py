#from local_utils.PiStream import stream
import multiprocessing
#from adafruit_servokit import ServoKit
import socket
#pca = ServoKit(channels=8)
servo_angle = [90, 90, 90]
#x = pca.servo[0]
#y1 = pca.servo[1]
#y2 = pca.servo[2]


def servo_ctrl():
    address = ('localhost', 8220)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(address)
    # print(connect(8220, "tcp"))
    server_socket.listen(5)
    print("Listening for client . . .")

    while True:
        conn, addr = server_socket.accept()
        conn.send(b"ack")
        print("Connected to client at ", addr)

        while conn is not None:
            output = conn.recv(2048)
            if output.strip() == b"disconnect":
                print(str(address) + " Disconnected.")
                conn.close()
                conn = None
            elif output:
                a = output.decode("utf-8").split(" ")
                conn.send(b"ack")

            for axis in range(len(a)):
                if a[axis] == '+':
                    servo_angle[axis] += 5
                elif a[axis] == '-':
                    servo_angle[axis] -= 5

            if a[1] != "=":
                servo_angle[2] = 90 - (servo_angle[1] - 90)

            for i in range(3):
                if servo_angle[i] >= 180: servo_angle[i] = 180
                elif servo_angle[i] <= 0: servo_angle[i] = 0

            #x.angle = servo_angle[0]
            #y1.angle = servo_angle[1]
            #y2.angle = servo_angle[2]
            print(servo_angle)


servos = multiprocessing.Process(target=servo_ctrl)
#stream = multiprocessing.Process(target=stream)

if __name__ == "__main__":
    servos.start()
    #stream.start()
    servos.join()
    #stream.join()

