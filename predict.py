import cv2
import numpy as np
import face_recognition
from datetime import datetime

# Load a sample image and learn how to recognize it.
known_image = face_recognition.load_image_file("path/to/known_person.jpg")
known_encoding = face_recognition.face_encodings(known_image)[0]

# Create arrays of known face encodings and their corresponding names
known_face_encodings = [known_encoding]
known_face_names = ["John Doe"]  # Replace with the actual names

video = cv2.VideoCapture('mod.mp4')
face_detect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

labels_dict = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Neutral', 5: 'Sad', 6: 'Surprise'}

# Dictionary to store attendance
attendance_dict = {}

while True:
    ret, frame = video.read()

    if not ret:
        print("Failed to capture video. Exiting...")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detect.detectMultiScale(gray, 1.3, 3)

    for x, y, w, h in faces:
        sub_face_img = frame[y:y + h, x:x + w]

        # Use face_recognition library to recognize faces
        face_locations = face_recognition.face_locations(sub_face_img)
        face_encodings = face_recognition.face_encodings(sub_face_img, face_locations)

        # Check if any known face is detected
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            name = "Unknown"
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

                # Record attendance using the name
                if name not in attendance_dict:
                    attendance_dict[name] = 1
                else:
                    attendance_dict[name] += 1

            # Draw rectangle and display name
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
            cv2.rectangle(frame, (x, y - 40), (x + w, y), (50, 50, 255), -1)
            cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow("Frame", frame)

    k = cv2.waitKey(1)
    if k == ord('q'):
        break

# Display attendance
print("Attendance:")
for name, count in attendance_dict.items():
    print(f"{name}: {count}")

video.release()
cv2.destroyAllWindows()