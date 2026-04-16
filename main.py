import cv2
from pose_detector import PoseDetector
from gesture_logic import process_gesture
from gesture_recorder import GestureRecorder
from gesture_signals import GestureSignal

try:
    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print(" ERROR: Could not open camera! Check if it's connected.")
        print("Available cameras: Try different indices (0, 1, 2, etc.)")
        exit()
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480) 
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)  
    cap.set(cv2.CAP_PROP_FPS, 20)  
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  
    
    detector = PoseDetector()
    recorder = GestureRecorder()
    signal = GestureSignal()
    
    recording = False
    frame_count = 0
    debug_mode = False  
    skip_frames = 2  

    print("🎮 AI Football Controller Started!")
    print("Press R to Record, S to Save, L to Load, D=Debug, ESC to Exit")
    print("\nOptimized Capture Settings:")
    print(f"  Resolution: {int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}")
    print(f"  Target FPS: 20")
    print(f"  Frame Skip: {skip_frames} (processes every {skip_frames}th frame)")
    print("\n✅ System Ready! Make body gestures to control the game...\n")

    while True:
        success, frame = cap.read()
        if not success:
            print(" Failed to capture frame")
            break
        frame = cv2.flip(frame, 1)
        frame_count += 1
        
    
        if frame_count % skip_frames != 0:
            continue
        
        landmarks, frame = detector.get_pose(frame)
        gesture = process_gesture(landmarks)
        signal.update(gesture)
        
        if recording:
            recorder.record_gesture(gesture, landmarks)
        
        if debug_mode and frame_count % 30 == 0:
            has_landmarks = len([l for l in landmarks if l != (0.5, 0.5, 0.5)]) > 10
            print(f"Frame: {frame_count} | Detected: {'✓ YES' if has_landmarks else '✗ NO'} | Gesture: {gesture}")
        
        h, w = frame.shape[:2]
        
        if recording:
            cv2.circle(frame, (30, 30), 10, (0, 0, 255), -1)
            cv2.putText(frame, "REC", (45, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("AI Football Controller", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 27: 
            break
        elif key == ord('r'): 
            if not recording:
                recording = True
                recorder.start_recording()
            else:
                recording = False
                recorder.stop_recording()
        elif key == ord('s'):  
            if recorder.gestures:
                recorder.save_recording()
        elif key == ord('l'):  
            files = recorder.get_recordings()
            if files:
                print(f"Available recordings: {files}")
        elif key == ord('d'):  
            debug_mode = not debug_mode
            status = "ON" if debug_mode else "OFF"
            print(f"🐛 Debug mode: {status}")
        elif key == ord('d'): 
            debug_mode = not debug_mode
            print(f"Debug mode: {'ON' if debug_mode else 'OFF'}")
                
except Exception as e:
    print(f"❌Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    cap.release()
    cv2.destroyAllWindows()
    print(" Application closed")
