import cv2
import mediapipe as mp
import numpy as np
import time

# --- INITIALIZATION ---
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.85, min_tracking_confidence=0.85)

# --- CONFIGURATION ---
GRID_SIZE = 25
WAIT_DURATION = 1.5  # Lock-on time (seconds)
COLORS = [
    (255, 191, 0),   # Electric Blue
    (60, 20, 220),   # Crimson Red
    (0, 255, 127),   # Spring Green
    (255, 0, 255)    # Deep Magenta
]
current_color_idx = 0

# Tracking Variables
voxels = {}      
start_timer = 0
is_pinching = False
is_drawing_active = False # New state for continuous drawing

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    current_time = time.time()

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Landmarks: Thumb Tip (4) and Index Tip (8)
            itip = hand_landmarks.landmark[8]
            btip = hand_landmarks.landmark[4]
            
            ix, iy = int(itip.x * w), int(itip.y * h)
            bx, by = int(btip.x * w), int(btip.y * h)
            
            # Distance for Pinch Gesture
            distance = np.hypot(ix - bx, iy - by)
            gx, gy = ix // GRID_SIZE, iy // GRID_SIZE
            vx, vy = gx * GRID_SIZE, gy * GRID_SIZE

            # --- 1. GHOST SILHOUETTE (Pre-interaction) ---
            # Show where the voxel WILL be before interaction
            if not is_drawing_active:
                cv2.rectangle(frame, (vx, vy), (vx + GRID_SIZE - 2, vy + GRID_SIZE - 2), (200, 200, 200), 1)

            # --- 2. INTERACTION LOGIC ---
            if distance < 35: # Pinch active
                if not is_pinching:
                    start_timer = current_time
                    is_pinching = True
                
                elapsed = current_time - start_timer
                progress = min(elapsed / WAIT_DURATION, 1.0)

                # Tech Radar UI
                if not is_drawing_active:
                    cv2.circle(frame, (ix, iy), 35, (70, 70, 70), 2)
                    angle = int(progress * 360)
                    cv2.ellipse(frame, (ix, iy), (35, 35), -90, 0, angle, COLORS[current_color_idx], 3)
                
                # --- 3. STREAM DRAWING (Continuous Mode) ---
                if elapsed >= WAIT_DURATION:
                    is_drawing_active = True # Drawing is now unlocked
                    voxels[(gx, gy)] = COLORS[current_color_idx] # Fill the voxel
            else:
                is_pinching = False
                is_drawing_active = False # Lock drawing when fingers separate

            # Skeleton Visuals
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=1, circle_radius=1),
                mp_drawing.DrawingSpec(color=COLORS[current_color_idx], thickness=2)
            )

    # --- RENDER STOCKED VOXELS ---
    for (gx, gy), color in voxels.items():
        vpx, vpy = gx * GRID_SIZE, gy * GRID_SIZE
        overlay = frame.copy()
        cv2.rectangle(overlay, (vpx, vpy), (vpx + GRID_SIZE - 2, vpy + GRID_SIZE - 2), color, -1)
        cv2.rectangle(overlay, (vpx, vpy), (vpx + GRID_SIZE - 2, vpy + GRID_SIZE - 2), (255, 255, 255), 1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

    # UI Top Bar
    cv2.rectangle(frame, (0, 0), (w, 40), (10, 10, 10), -1)
    mode_text = "STREAM ACTIVE" if is_drawing_active else "READY"
    cv2.putText(frame, f"MODE: {mode_text} | COLOR: {current_color_idx+1} | 'R': CYCLE | 'C': CLEAR", 
                (15, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

    cv2.imshow('Futuristic Voxel Studio', frame)

    key = cv2.waitKey(1)
    if key == ord('q'): break
    if key == ord('c'): voxels.clear()
    if key == ord('r'): current_color_idx = (current_color_idx + 1) % len(COLORS)

cap.release()
cv2.destroyAllWindows()