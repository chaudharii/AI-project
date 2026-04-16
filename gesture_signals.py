import cv2
import numpy as np
from datetime import datetime
from collections import deque

class GestureSignal:
    """Class to manage and display gesture signals on video"""
    
    def __init__(self, max_history=10):
        self.gesture_history = deque(maxlen=max_history)
        self.current_gesture = "IDLE"
        self.gesture_colors = {
            "HEADING RIGHT!": (0, 255, 255),                # Cyan
            "HEADING LEFT!": (255, 255, 0),                 # Yellow
            "MOVE LEFT!": (255, 0, 0),                      # Blue
            "MOVE RIGHT!": (0, 165, 255),                   # Orange
            "SPRINTING!": (0, 255, 0),                      # Green
            "LEFT KICK!": (147, 112, 219),                  # Blue Violet
            "RIGHT KICK!": (255, 0, 255),                   # Magenta
            "THROW-IN!": (255, 165, 0),                     # Dark Orange
            "SLIDE TACKLE LEFT!": (0, 0, 255),              # Red
            "SLIDE TACKLE RIGHT!": (255, 200, 100),         # Light Blue
            "DEFENSIVE STANCE!": (255, 200, 124),           # Steel Blue
            "IDLE - Ready to move": (200, 200, 200),        # Gray
            "WAITING FOR POSE...": (100, 100, 100),         # Dark Gray
        }
        
        self.gesture_icons = {
            "MOVE LEFT": "◄",
            "MOVE RIGHT": "►",
            "SPRINT": "⚡",
            "KICK": "●",
            "IDLE": "○",
        }
    
    def update(self, gesture_text):
        """Update current gesture"""
        self.current_gesture = gesture_text
        self.gesture_history.append({
            'gesture': gesture_text,
            'time': datetime.now(),
            'color': self.gesture_colors.get(gesture_text, (200, 200, 200))
        })
    
    def get_color(self):
        """Get color for current gesture"""
        return self.gesture_colors.get(self.current_gesture, (200, 200, 200))
    
    def draw_signal_box(self, frame, x, y, width, height):
        """Draw main gesture signal box"""
        h, w = frame.shape[:2]
        
        # Draw filled rectangle with gesture color
        color = self.get_color()
        cv2.rectangle(frame, (x, y), (x + width, y + height), color, -1)
        cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 255, 255), 3)
        
        # Add gesture text
        text = self.current_gesture
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.2
        thickness = 2
        
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        text_x = x + (width - text_size[0]) // 2
        text_y = y + (height + text_size[1]) // 2
        
        cv2.putText(frame, text, (text_x, text_y), font, font_scale, (0, 0, 0), thickness)
    
    def draw_history_bar(self, frame, x, y, width=300, height=60):
        """Draw gesture history timeline at bottom"""
        h, w = frame.shape[:2]
        
        # Draw background
        cv2.rectangle(frame, (x, y), (x + width, y + height), (30, 30, 30), -1)
        cv2.rectangle(frame, (x, y), (x + width, y + height), (150, 150, 150), 2)
        
        # Title
        cv2.putText(frame, "GESTURE HISTORY", (x + 10, y + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        # Draw each gesture in history
        num_gestures = len(self.gesture_history)
        if num_gestures > 0:
            box_width = (width - 20) // min(num_gestures, 5)
            
            for i, gesture_data in enumerate(list(self.gesture_history)[-5:]):
                # Draw colored box
                bx = x + 10 + (i * box_width)
                by = y + 30
                cv2.rectangle(frame, (bx, by), (bx + box_width - 5, by + 25), 
                            gesture_data['color'], -1)
                cv2.rectangle(frame, (bx, by), (bx + box_width - 5, by + 25), 
                            (255, 255, 255), 1)
                
                # Add number
                cv2.putText(frame, str(i + 1), (bx + 5, by + 18),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
    
    def draw_status_indicator(self, frame, is_detected, x=10, y=10):
        """Draw status indicator (pose detected or not)"""
        status_text = "✓ DETECTED" if is_detected else "✗ NOT DETECTED"
        status_color = (0, 255, 0) if is_detected else (0, 0, 255)
        bg_color = (34, 139, 34) if is_detected else (139, 0, 0)
        
        # Draw background
        cv2.rectangle(frame, (x, y), (x + 180, y + 35), bg_color, -1)
        cv2.rectangle(frame, (x, y), (x + 180, y + 35), status_color, 2)
        
        # Draw text
        cv2.putText(frame, status_text, (x + 15, y + 25),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    def draw_gesture_counter(self, frame, x, y):
        """Draw total gestures detected counter"""
        total = len(self.gesture_history)
        counter_text = f"SIGNALS: {total}"
        
        # Draw background
        cv2.rectangle(frame, (x, y), (x + 150, y + 40), (50, 50, 100), -1)
        cv2.rectangle(frame, (x, y), (x + 150, y + 40), (100, 150, 255), 2)
        
        # Draw text
        cv2.putText(frame, counter_text, (x + 10, y + 28),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (100, 255, 255), 2)
    
    def draw_all_signals(self, frame, is_detected):
        """Draw all signal elements on frame"""
        h, w = frame.shape[:2]
        
        # Status indicator (top left)
        self.draw_status_indicator(frame, is_detected, x=10, y=10)
        
        # Counter (top right)
        self.draw_gesture_counter(frame, x=w - 160, y=10)
        
        # Main signal box (center)
        signal_width = 400
        signal_height = 100
        signal_x = (w - signal_width) // 2
        signal_y = (h - signal_height) // 2 - 50
        self.draw_signal_box(frame, signal_x, signal_y, signal_width, signal_height)
        
        # History bar (bottom)
        self.draw_history_bar(frame, x=10, y=h - 80, width=w - 20)
    
    def draw_gesture_instruction(self, frame, x, y):
        """Draw animated gesture instruction"""
        instructions = [
            "1. Move LEFT SHOULDER = Move Left",
            "2. Move RIGHT SHOULDER = Move Right",
            "3. Raise HIPS = Sprint",
            "4. Raise LEFT LEG = Kick"
        ]
        
        # Draw semi-transparent background
        overlay = frame.copy()
        cv2.rectangle(overlay, (x, y), (x + 320, y + 150), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        
        # Draw border
        cv2.rectangle(frame, (x, y), (x + 320, y + 150), (100, 200, 255), 2)
        
        # Draw title
        cv2.putText(frame, "INSTRUCTIONS", (x + 10, y + 25),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 200, 255), 2)
        
        # Draw instructions
        text_y = y + 50
        for instruction in instructions:
            cv2.putText(frame, instruction, (x + 15, text_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
            text_y += 25
    
    def get_gesture_stats(self):
        """Get gesture statistics"""
        if not self.gesture_history:
            return {}
        
        gesture_counts = {}
        for item in self.gesture_history:
            gesture = item['gesture']
            gesture_counts[gesture] = gesture_counts.get(gesture, 0) + 1
        
        return gesture_counts
    
    def draw_stats(self, frame, x, y):
        """Draw gesture statistics"""
        stats = self.get_gesture_stats()
        
        if not stats:
            return
        
        h = len(stats) * 25 + 40
        w = 250
        
        # Draw background
        overlay = frame.copy()
        cv2.rectangle(overlay, (x, y), (x + w, y + h), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Draw border
        cv2.rectangle(frame, (x, y), (x + w, y + h), (150, 150, 255), 2)
        
        # Draw title
        cv2.putText(frame, "GESTURE STATS", (x + 10, y + 25),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (150, 150, 255), 1)
        
        # Draw stats
        text_y = y + 50
        for gesture, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
            gesture_short = gesture.split("!")[0][:15]
            cv2.putText(frame, f"{gesture_short}: {count}x", (x + 15, text_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
            text_y += 25
