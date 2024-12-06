# Home Security System Using Face Recognition

## Problem Statement

This project addresses the need for a secure access control system in homes, enabling role-based monitoring and restricting access to specific areas. For example, children entering restricted zones like the kitchen trigger a warning, while adults have access without restrictions.

---

## Overview of the Approach

This system employs **Local Binary Patterns Histogram (LBPH)** for face recognition, combined with role-based access control. Key features include:

1. **Face Registration**: Capturing and storing faces with corresponding roles.
2. **Training**: Building a face recognition model using registered data.
3. **Live Recognition**: Identifying individuals in real-time and validating their access permissions.

---

## How It Works

### Input:

- Webcam feed or photo uploads for face registration.
- Predefined roles and access permissions configured in JSON files.
- Real-time camera feed for face recognition.

### Output:

- Live recognition feed with names and roles displayed.
- Warning messages for unauthorized access based on roles and zones.

### Workflow:

1. **Registration**:
   - Captures a face via webcam or uploads a photo.
   - Saves the face image and maps it to a role (e.g., Parent, Child, Pet).
   - Updates role mappings in `roles.json`.
2. **Training**:
   - Trains an LBPH face recognizer using registered faces.
3. **Recognition**:
   - Detects and identifies faces in real-time video.
   - Validates roles against access permissions for specific zones.
   - Displays warnings for unauthorized access.

---

## Challenges Faced

1. **Face Detection**:
   - Improved accuracy by ensuring one face per image during registration.
2. **Role-Based Access Mapping**:
   - Simplified management using JSON files for roles and permissions.
3. **Performance**:
   - Optimized detection and recognition for real-time processing.

---

## System Architecture

1. **Face Registration**:
   - Captures faces via webcam or file upload.
   - Saves grayscale images and role mappings.
2. **Face Recognition**:
   - LBPH recognizer trained on registered faces.
3. **Role-Based Access Control**:
   - Permissions configured in `roles.json` and `roles_access.json`.
4. **Live Monitoring**:
   - Real-time recognition and access validation with a warning system.

---

## Dataset

- **Registered Faces**: Saved grayscale `.jpg` images.
- **Configurations**:
  - `roles.json`: Maps names to roles.
  - `roles_access.json`: Defines role-based access permissions.
  - `areas.json`: Specifies monitored zones.

---

## Evaluation Metrics

- **Recognition Accuracy**:
  - Acceptable predictions: Confidence > 50%.
- **Detection Precision**:
  - Verified during face registration.
- **Access Control Validation**:
  - Tested by enforcing role-specific restrictions for each zone.

---

## Results

- **Usability**:
  - Simple registration and configuration process.
  - Effective role-based access monitoring.
- **Performance**:
  - Fast and reliable recognition in real-time.
  - Accurate classification with minimal false positives.

---

## Future Enhancements

1. **Multi-Camera Support**: Extend the system to monitor multiple zones.
2. **Spoof Detection**: Add liveness detection to prevent fake face attacks.
3. **Mobile Integration**: Send real-time alerts and access logs to mobile devices.
4. **Advanced Models**: Integrate deep learning models for improved accuracy.

---

## How to Run

1.  **Install dependencies:**
    ```bash
    pip install opencv-python opencv-contrib-python numpy
    ```
2.  **Run the Script:**
    Execute the main script to start the program
    ```bash
    python home_security_system.py
    ```
3.  **Follow the On-Screen Instructions:**

    - Register Faces: Capture or upload photos to register individuals with roles.

    - Train the Recognizer: Train the face recognition model using registered data.

    - Live Recognition: Start real-time monitoring and enforce role-based access control.

4.  **Ensure Directory Structure:** The program automatically creates necessary directories and files if they don't exist:

    ```bash
    ├── home_security_system.py       # Main script
    ├── registered_faces/             # Directory for saved face images
    ├── roles.json                    # Role mappings
    ├── roles_access.json             # Role-based access permissions
    ├── areas.json                    # Monitored zones

    ```

5.  **Optional Configuration:**
    Customize the following files as needed:

        - roles.json: Add or update roles for registered faces.
        - roles_access.json: Define access permissions for each role.
        - areas.json: Specify the monitored zones or camera names.
