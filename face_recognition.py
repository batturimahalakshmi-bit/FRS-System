import cv2
import os
import csv
import numpy as np
from datetime import datetime


# ==========================================
# FACE DETECTOR
# ==========================================

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)


# ==========================================
# FACE RECOGNIZER
# ==========================================

recognizer = cv2.face.LBPHFaceRecognizer_create()


# ==========================================
# REGISTERED FACE
# ==========================================

image_path = "known_faces/Maha.jpg"

if not os.path.exists(image_path):

    print("Maha.jpg not found!")
    exit()


image = cv2.imread(
    image_path,
    cv2.IMREAD_GRAYSCALE
)


faces = face_cascade.detectMultiScale(
    image,
    scaleFactor=1.1,
    minNeighbors=5
)


if len(faces) == 0:

    print("No face found in Maha.jpg")
    exit()


training_faces = []
labels = []


for (x, y, w, h) in faces:

    training_faces.append(
        image[y:y+h, x:x+w]
    )

    labels.append(1)


recognizer.train(
    training_faces,
    np.array(labels)
)


# ==========================================
# ATTENDANCE FUNCTION
# ==========================================

def mark_attendance(name):

    file = "attendance.csv"

    today = datetime.now().strftime("%d-%m-%Y")

    # Check existing attendance
    if os.path.exists(file):

        with open(file, "r", newline="") as f:

            reader = csv.reader(f)

            next(reader, None)

            for row in reader:

                if len(row) >= 3:

                    existing_name = row[0]
                    existing_date = row[1]

                    if existing_name == name and existing_date == today:

                        return False


    # Add new attendance
    file_exists = os.path.exists(file)

    with open(
        file,
        "a",
        newline=""
    ) as f:

        writer = csv.writer(f)

        if not file_exists:

            writer.writerow(
                ["Name", "Date", "Time"]
            )

        now = datetime.now()

        writer.writerow([
            name,
            now.strftime("%d-%m-%Y"),
            now.strftime("%H:%M:%S")
        ])

    return True


# ==========================================
# CAMERA
# ==========================================

camera = cv2.VideoCapture(0)


while True:

    ret, frame = camera.read()

    if not ret:

        print("Camera not working")
        break


    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )


    detected_faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5
    )


    for (x, y, w, h) in detected_faces:

        face = gray[y:y+h, x:x+w]

        label, confidence = recognizer.predict(face)


        if confidence < 70:

            name = "Maha"

            # Automatic attendance
            marked = mark_attendance(name)

            if marked:

                print("Attendance marked for", name)


        else:

            name = "Unknown"


        # Face rectangle
        cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            (0, 255, 0),
            2
        )


        # Name
        cv2.putText(
            frame,
            name,
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )


    cv2.imshow(
        "Face Recognition + Attendance",
        frame
    )


    # Q = Quit
    if cv2.waitKey(1) & 0xFF == ord("q"):

        break


# ==========================================
# CLOSE CAMERA
# ==========================================

camera.release()

cv2.destroyAllWindows()