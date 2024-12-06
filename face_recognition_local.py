import cv2
import numpy as np
import os
import json

# Directory to store registered faces
os.makedirs("registered_faces", exist_ok=True)

# JSON file to store roles and mappings
roles_file = "roles.json"
roles_access_file = "roles_access.json"
areas_file = "areas.json"

# Load roles from the JSON file if it exists
if os.path.exists(roles_file):
    with open(roles_file, "r") as f:
        roles = json.load(f)
else:
    roles = {}

# Load roles access permissions
if os.path.exists(roles_access_file):
    with open(roles_access_file, "r") as f:
        roles_access = json.load(f)
else:
    roles_access = {}

# Load areas from the JSON file
if os.path.exists(areas_file):
    with open(areas_file, "r") as f:
        areas = json.load(f).get("areas", [])
else:
    areas = []

# Initialize the face recognizer and face detector
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


# Save roles to JSON file
def save_roles_to_json():
    with open(roles_file, "w") as f:
        json.dump(roles, f, indent=4)


# Function to register a face
def register_face():
    global roles
    print("Choose an option to register a face:")
    print("1. Capture face using webcam")
    print("2. Upload photo file")

    choice = input("Enter your choice (1/2): ").strip()

    if choice == "1":
        cam = cv2.VideoCapture(0)
        print("Press 'c' to capture a face or 'q' to quit.")

        while True:
            ret, frame = cam.read()
            if not ret:
                print("Failed to access the webcam.")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            cv2.imshow("Register Face", frame)

            key = cv2.waitKey(1)
            if key == ord('c') and len(faces) == 1:
                (x, y, w, h) = faces[0]
                face = gray[y:y+h, x:x+w]
                name = input("Enter the name of the person or pet: ")
                role = input(f"Assign a role for {name} (e.g., Admin, Parent, Child, Pet): ")
                cv2.imwrite(f"registered_faces/{name}.jpg", face)
                roles[name] = role
                save_roles_to_json()  # Save roles persistently
                print(f"Registered {name} with role: {role}")
                break  # Exit the loop after capturing the face

            if key == ord('q'):
                print("Face registration cancelled.")
                break

        cam.release()
        cv2.destroyAllWindows()

    elif choice == "2":
        file_path = input("Enter the file path of the photo: ").strip()
        if os.path.exists(file_path):
            image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            faces = face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5)

            if len(faces) == 1:  # Ensure only one face is detected
                (x, y, w, h) = faces[0]
                face = image[y:y+h, x:x+w]
                name = input("Enter the name of the person or pet: ")
                role = input(f"Assign a role for {name} (e.g., Admin, Parent, Child, Pet): ")
                cv2.imwrite(f"registered_faces/{name}.jpg", face)
                roles[name] = role
                save_roles_to_json()  # Save roles persistently
                print(f"Registered {name} with role: {role}")
            else:
                print("Please ensure the photo contains exactly one face.")
        else:
            print("File not found. Please check the file path.")

    else:
        print("Invalid choice. Returning to the main menu.")


# Function to train the face recognizer
def train_faces():
    faces, labels =  [], []
    label_dict = {}
    current_label = 0

    for filename in os.listdir("registered_faces"):
        if filename.endswith(".jpg"):
            filepath = os.path.join("registered_faces", filename)
            image = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
            faces.append(image)
            name = os.path.splitext(filename)[0]
            if name not in label_dict:
                label_dict[name] = current_label
                current_label += 1
            labels.append(label_dict[name])

    if faces and labels:
        face_recognizer.train(faces, np.array(labels))
        print("Training completed.")
    else:
        print("No registered faces to train.")

    return label_dict


# Function for live face recognition
def recognize_faces(label_dict, cam_name):
    if cam_name not in areas:
        print(f"Invalid camera name. Please choose from {areas}.")
        return

    cam = cv2.VideoCapture(0)
    print("Press 'q' to quit live recognition.")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to access the webcam.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            face_resized = cv2.resize(face, (200, 200))
            label, confidence = face_recognizer.predict(face_resized)

            if confidence < 50:  # Threshold for recognition
                for name, lbl in label_dict.items():
                    if lbl == label:
                        role = roles.get(name, "Unknown Role")
                        allowed = roles_access.get(role, {}).get(cam_name, False)
                        if not allowed:
                            warning = f"WARNING: {role} not allowed in {cam_name}!"
                            cv2.putText(frame, warning, (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

                        display_text = f"{name} ({role})"
                        color = (0, 255, 0)
                        break
            else:
                display_text = "Unknown"
                color = (0, 0, 255)

            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, display_text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        info_text = f"Camera: {cam_name}"
        cv2.putText(frame, info_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.imshow("Live Face Recognition", frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()


# Main execution flow
if __name__ == "__main__":
    while True:
        print("\nChoose an option:")
        print("1. Register Faces")
        print("2. Train Recognizer")
        print("3. Recognize Faces")
        print("4. Exit")

        choice = input("Enter your choice (1/2/3/4): ").strip()

        if choice == "1":
            register_face()
        elif choice == "2":
            label_dict = train_faces()
        elif choice == "3":
            cam_name = input(f"Enter the name of the camera (choose from {areas}): ").strip()
            if os.path.exists("registered_faces"):
                label_dict = train_faces()
                recognize_faces(label_dict, cam_name)
            else:
                print("No registered faces found. Please register faces first.")
        elif choice == "4":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")
