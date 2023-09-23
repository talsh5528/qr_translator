import cv2
from pyzbar.pyzbar import decode
import pyqrcode
import os

output_folder = "qr_codes"
output_file_path = 'qr_code_data.txt'


# Function to get the expected file size from the first QR code
def get_expected_file_size():
    cap = cv2.VideoCapture(0)  # Open the camera
    while True:
        ret, frame = cap.read()
        decoded_objects = decode(frame)
        if decoded_objects:
            qr_data = decoded_objects[0].data.decode('utf-8')
            expected_file_size = int(qr_data)
            cap.release()  # Release the camera
            return expected_file_size


def main():
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    cap = cv2.VideoCapture(0)  # Open the camera
    expected_file_size = get_expected_file_size()
    file = open(output_file_path, 'w')
    qr_last_data = str(expected_file_size)
    for line in range(0, expected_file_size):
        qr = pyqrcode.create(str(line))
        output_file = os.path.join(output_folder, f'qr_code_{line}.png')
        qr.png(output_file, scale=6)  # Create and save QR code image
        qr.show()  # Show the QR code on the screen
        while True:
            ret, frame = cap.read()
            decoded_objects = decode(frame)

            if decoded_objects:
                qr_data = decoded_objects[0].data.decode('utf-8')
                if qr_data != qr_last_data:
                    file.write(qr_data + '\n')  # Write QR data to a file
                    qr_last_data = qr_data
                    cv2.imshow('QR Code Scanner', frame)  # Display the frame
                    break
    cap.release()  # Release the camera
    cv2.destroyAllWindows()  # Close the OpenCV window
    file.close()  # Close the file


if __name__ == "__main__":
    main()