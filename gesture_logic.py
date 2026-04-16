from controller import press, release
from config import *


def process_gesture(landmarks):
    if len(landmarks) < 27:
        return "WAITING FOR POSE..."

    head = landmarks[0]
    left_shoulder = landmarks[11]
    right_shoulder = landmarks[12]
    left_elbow = landmarks[13]
    right_elbow = landmarks[14]
    left_wrist = landmarks[15]
    right_wrist = landmarks[16]
    left_hip = landmarks[23]
    right_hip = landmarks[24]
    left_knee = landmarks[25]
    right_knee = landmarks[26]

    shoulder_diff = left_shoulder[1] - right_shoulder[1]
    hip_center_y = (left_hip[1] + right_hip[1]) / 2
    hip_center_x = (left_hip[0] + right_hip[0]) / 2
    
    gesture = "IDLE - Ready to move"

    # HEAD MOVEMENT - HEADING
    if head[0] > HEAD_RIGHT_THRESHOLD:
        press('h')
        gesture = "HEADING RIGHT!"
    elif head[0] < HEAD_LEFT_THRESHOLD:
        press('g')
        gesture = "HEADING LEFT!"
    else:
        release('h')
        release('g')

    # LEFT / RIGHT MOVE (SHOULDER)
    if shoulder_diff > SHOULDER_LEFT_THRESHOLD:
        press('a')
        release('d')
        if gesture == "IDLE - Ready to move":
            gesture = "MOVE LEFT!"
    elif shoulder_diff < SHOULDER_RIGHT_THRESHOLD:
        press('d')
        release('a')
        if gesture == "IDLE - Ready to move":
            gesture = "MOVE RIGHT!"
    else:
        release('a')
        release('d')

    # SPRINT
    if hip_center_y < HIP_SPRINT_THRESHOLD:
        press('shift')
        if gesture == "IDLE - Ready to move":
            gesture = "SPRINTING!"
    else:
        release('shift')

    # LEFT KICK
    if left_knee[1] < hip_center_y - LEG_KICK_THRESHOLD:
        press('q')
        gesture = "LEFT KICK!"
    else:
        release('q')

    # RIGHT KICK
    if right_knee[1] < hip_center_y - LEG_KICK_THRESHOLD:
        press('e')
        gesture = "RIGHT KICK!"
    else:
        release('e')

    # THROW-IN (both arms raised)
    if left_wrist[1] < ARM_RAISE_THRESHOLD and right_wrist[1] < ARM_RAISE_THRESHOLD:
        press('t')
        gesture = "THROW-IN!"
    else:
        release('t')

    # SLIDE TACKLE (body lean)
    body_lean = left_hip[0] - right_hip[0]
    if body_lean > LEAN_RIGHT_THRESHOLD:
        press('r')
        gesture = "SLIDE TACKLE RIGHT!"
    elif body_lean < LEAN_LEFT_THRESHOLD:
        press('l')
        gesture = "SLIDE TACKLE LEFT!"
    else:
        release('r')
        release('l')

    # DEFENSIVE STANCE (elbow raised)
    if left_elbow[1] < ELBOW_RAISE_THRESHOLD or right_elbow[1] < ELBOW_RAISE_THRESHOLD:
        press('d')
        gesture = "DEFENSIVE STANCE!"
    else:
        release('d')
    
    return gesture

