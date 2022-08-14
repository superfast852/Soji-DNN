#from local_utils.PiStream import stream  # Camera Streamer Code
import multiprocessing
#from adafruit_servokit import ServoKit  # Servo Controller lib
import socket
#pca = ServoKit(channels=8)  # Initialize the Servo Controller with 8 ports open (6 servos will be used)
servo_angle = [90, 90, 90]  # Initialization Angles
#x = pca.servo[0]  # Assign servo port to variable
#y1 = pca.servo[1]
#y2 = pca.servo[2]


def servo_ctrl():
    address = ('localhost', 8220)  # Comm socket address

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Init socket
    server_socket.bind(address)  # Open Socket in that address
    # print(connect(8220, "tcp"))  # Open ngrok tunnel
    server_socket.listen(5)  # Listen for new clients
    print("Listening for client . . .")

    while True:
        conn, addr = server_socket.accept()  # Start communication if a client is found
        print("Connected to client at ", addr)

        while conn is not None:
            output = conn.recv(2048)  # Wait and receive a new packet
            if output.strip() == b"disconnect":  # If the packet is a disconnect.
                print(str(address) + " Disconnected.")
                conn.close()  # Close connection with client
                conn = None  # Disable loop in next pass
            elif output:
                a = output.decode("utf-8").split(" ")  # decode and split into a list the received adjustments

            for axis in range(len(a)):  # Pretty self-explanatory imo
                if a[axis] == '+':
                    servo_angle[axis] += 5
                elif a[axis] == '-':
                    servo_angle[axis] -= 5

            if a[1] != "=":
                servo_angle[2] = 90 - (servo_angle[1] - 90)  # Broken, gotta fix

            for i in range(3):  # Range Delimiters
                if servo_angle[i] >= 180: servo_angle[i] = 180
                elif servo_angle[i] <= 0: servo_angle[i] = 0

            # Write angles to servos
            #x.angle = servo_angle[0]
            #y1.angle = servo_angle[1]
            #y2.angle = servo_angle[2]
            print(servo_angle)


servos = multiprocessing.Process(target=servo_ctrl)  # Assign servos function to Thread #1
#stream = multiprocessing.Process(target=stream)     # Assign video stream handling to Thread #2

if __name__ == "__main__":
    # Start Threads
    servos.start()
    #stream.start()
    servos.join()
    #stream.join()

