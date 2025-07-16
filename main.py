import face_recognition
import cv2
import os

# Load known faces from the known_faces folder
known_faces_dir = "known_faces"
known_encodings = []
known_names = []

print("Loading known faces...")
for filename in os.listdir(known_faces_dir):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        path = os.path.join(known_faces_dir, filename)
        image = face_recognition.load_image_file(path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_encodings.append(encodings[0])
            name = os.path.splitext(filename)[0]  # filename without extension
            known_names.append(name)
print(f"Loaded {len(known_names)} known faces.")

# Load the test image
print("Loading test image...")
test_image = face_recognition.load_image_file("test_images.jpg")

# Detect faces in the test image
print("Detecting faces in test image...")
face_locations = face_recognition.face_locations(test_image)
face_encodings = face_recognition.face_encodings(test_image, face_locations)

print("Number of faces detected:", len(face_encodings))

# Convert image to BGR for display with OpenCV
test_image_bgr = cv2.cvtColor(test_image, cv2.COLOR_RGB2BGR)

# Compare each face with known faces
for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
    matches = face_recognition.compare_faces(known_encodings, face_encoding)
    name = "Unknown"

    if True in matches:
        match_index = matches.index(True)
        name = known_names[match_index]

    # Draw rectangle and put name label
    cv2.rectangle(test_image_bgr, (left, top), (right, bottom),(0,255,0), 2)
    cv2.putText(test_image_bgr, name, (left - 70, top -50), cv2.FONT_HERSHEY_SIMPLEX , 0.6, (0, 0,0),2)

# Show the result
cv2.imshow("Recognition Result", test_image_bgr)
cv2.waitKey(0)
cv2.destroyAllWindows()
