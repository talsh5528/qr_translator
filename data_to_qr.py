import os
import cv2
import pyqrcode
from pyzbar.pyzbar import decode
import tkinter as tk
from tkinter import filedialog


def open_file_dialog():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Ask the user to select a file
    file_path = filedialog.askopenfilename()

    # Check if a file was selected
    if file_path:
        print(f"Selected file path: {file_path}")
    return file_path


def wait_for_qr(line):
    # Step 2: Open the camera and wait for confirmation QR code
    cap = cv2.VideoCapture(0)
    while True:
        # Capture a frame from the camera
        ret, frame = cap.read()

        # Decode QR codes in the frame
        decoded_objects = decode(frame)

        for obj in decoded_objects:
            qr_data = obj.data.decode('utf-8')
            # Check if the QR code contains a confirmation message
            if int(qr_data) == line:
                return True


def main():

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    try:
        with open(input_file, 'r') as file:
            lines = file.readlines()
        line_count = len(lines)

        # Step 2: Create a QR code with the line count
        line_count_qr = pyqrcode.create(str(line_count))
        line_count_output_file = os.path.join(output_folder, 'line_count_qr.png')
        line_count_qr.png(line_count_output_file, scale=6)  # You can adjust the scale as needed
        line_count_qr.show()
        for line_number in range(line_count):
            while wait_for_qr(line_number):
                line_data = lines[line_number].strip()
                print(f"Creating line data {line_data}")
                qr = pyqrcode.create(line_data)
                output_file = os.path.join(output_folder, f'qr_code_{line_number}.png')
                qr.png(output_file, scale=6)
                print(f"QR code for line {line_number} saved as {output_file}")
                qr.show()
                break

        print("Finish to transfer the all file")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    # Specify the input file and output folder
    input_file = open_file_dialog()
    output_folder = 'qr_codes'
    main()
