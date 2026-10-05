import cv2
import os

name = input("Enter person's name: ")

folder = "known_faces"

if not os.path.exists(folder):
    os.makedirs(folder)

camera = cv2.VideoCapture(0)

count = 0

while True:
    ret, frame = camera.read()

    if not ret:
        print("Camera not working")
        break

    cv2.imshow("Register Face - Press Q to Stop", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("s"):
        filename = f"{folder}/{name}.jpg"
        cv2.imwrite(filename, frame)
        print("Face image saved:", filename)
        break

    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()