import cv2
import mediapipe as mp

# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
mp_draw = mp.solutions.drawing_utils

# Create a Face Detection object
face_detection = mp_face_detection.FaceDetection(
    min_detection_confidence=0.5
)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Initialize webcam
cap = cv2.VideoCapture(1)  # Change to 0 if your webcam is at index 0

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Error: Could not read frame.")
        break

    # Flip the image horizontally to create a mirror effect
    image = cv2.flip(image, 1)

    # Convert the image to RGB for MediaPipe
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image with MediaPipe Face Detection
    face_results = face_detection.process(image_rgb)

    # Draw face detection results
    if face_results.detections:
        for detection in face_results.detections:
            mp_draw.draw_detection(image, detection)

    # Process image with MediaPipe Hands
    hand_results = hands.process(image_rgb)

    # Draw hand landmarks and connections
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display the image
    cv2.imshow('MediaPipe Face Detection and Hands', image)

    # Exit if 'q' is pressed
    if cv2.waitKey(5) & 0xFF == 27:
        break

# Release resources
cap.release()
cv2.destroyAllWindows()