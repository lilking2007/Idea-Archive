import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands module
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Initialize variables for drawing
brush_size = 10
brush_color = (0, 0, 0)  # Default color (Black)
drawing = False

# Define a set of colors to choose from at the bottom of the screen
colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0)]
color_rectangles = []

# Create a blank canvas
canvas = np.ones((480, 640, 3), dtype=np.uint8) * 255  # White canvas

# Function to check if the index finger is over any color box
def check_color_selection(x, y):
    for i, (color, rect) in enumerate(zip(colors, color_rectangles)):
        if rect[0] < x < rect[0] + rect[2] and rect[1] < y < rect[1] + rect[3]:
            return color
    return None

# Open the webcam
cap = cv2.VideoCapture(1)

# MediaPipe Hands configuration
with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame horizontally for a later selfie-view display
        frame = cv2.flip(frame, 1)

        # Convert the image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame and get the results
        results = hands.process(rgb_frame)

        # Draw color boxes at the bottom
        color_height = 50
        for i, color in enumerate(colors):
            rect_x = i * (frame.shape[1] // len(colors))
            rect_y = frame.shape[0] - color_height
            color_rectangles.append((rect_x, rect_y, frame.shape[1] // len(colors), color_height))
            cv2.rectangle(frame, (rect_x, rect_y), (rect_x + frame.shape[1] // len(colors), rect_y + color_height), color, -1)

        # Draw the selected brush color (the rectangle of color)
        cv2.putText(frame, "Brush Color", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, brush_color, 2, cv2.LINE_AA)

        # If hand landmarks are detected
        if results.multi_hand_landmarks:
            for landmarks in results.multi_hand_landmarks:
                # Draw landmarks
                mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

                # Get the position of the index finger tip (landmark 8)
                index_finger_tip = landmarks.landmark[8]

                # Convert the normalized coordinates to pixel values
                h, w, _ = frame.shape
                x = int(index_finger_tip.x * w)
                y = int(index_finger_tip.y * h)

                # Check if the index finger is over a color box to select the color
                selected_color = check_color_selection(x, y)
                if selected_color:
                    brush_color = selected_color

                # Draw on the canvas with the selected brush color
                if drawing:
                    cv2.circle(canvas, (x, y), brush_size, brush_color, -1)

                # Draw the circle representing the index finger
                cv2.circle(frame, (x, y), brush_size, brush_color, -1)

                # Detect when the user starts or stops drawing
                if landmarks.landmark[8].y < landmarks.landmark[7].y:  # If index tip is above the joint
                    drawing = True
                else:
                    drawing = False

        # Show the canvas (drawing area)
        combined_frame = cv2.addWeighted(frame, 0.7, canvas, 0.3, 0)
        cv2.imshow("Hand Tracking - Draw with your index finger", combined_frame)

        # Exit if the user presses 'q'
        if cv2.waitKey(1) & 0xFF == 27: # 27 is the ASCII code for the ESC key
            break

# Release resources
cap.release()
cv2.destroyAllWindows()
