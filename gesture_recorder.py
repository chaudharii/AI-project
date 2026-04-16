import json
import os
from datetime import datetime
from collections import deque

class GestureRecorder:
    """Records and replays gesture sequences"""
    
    def __init__(self, save_dir="gesture_recordings"):
        self.save_dir = save_dir
        self.recording = False
        self.gestures = deque()
        self.timestamps = deque()
        
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
    
    def start_recording(self):
        """Start recording gestures"""
        self.recording = True
        self.gestures.clear()
        self.timestamps.clear()
        print("📹 Recording started...")
        return True
    
    def stop_recording(self):
        """Stop recording and save"""
        self.recording = False
        print("📹 Recording stopped")
        return len(self.gestures) > 0
    
    def record_gesture(self, gesture_text, landmarks):
        """Record a gesture with landmarks"""
        if self.recording:
            self.gestures.append({
                'gesture': gesture_text,
                'landmarks': landmarks,
                'timestamp': datetime.now().isoformat()
            })
            self.timestamps.append(datetime.now())
    
    def save_recording(self, filename=None):
        """Save recorded gestures to file"""
        if not filename:
            filename = f"gesture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = os.path.join(self.save_dir, filename)
        
        data = {
            'gestures': list(self.gestures),
            'duration': (self.timestamps[-1] - self.timestamps[0]).total_seconds() if len(self.timestamps) > 1 else 0,
            'count': len(self.gestures)
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"💾 Saved: {filepath}")
        return filepath
    
    def load_recording(self, filename):
        """Load recorded gestures from file"""
        filepath = os.path.join(self.save_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"❌ File not found: {filepath}")
            return False
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.gestures = deque(data['gestures'])
        print(f"📂 Loaded: {filepath} ({len(self.gestures)} gestures)")
        return True
    
    def get_recordings(self):
        """List all saved recordings"""
        files = os.listdir(self.save_dir)
        return [f for f in files if f.endswith('.json')]
    
    def playback_gesture(self, index):
        """Get gesture at specific index for playback"""
        if index < len(self.gestures):
            return self.gestures[index]
        return None
