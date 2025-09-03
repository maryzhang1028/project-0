# tests/create_test_videos.py
"""Create test videos for CI/CD testing"""

import cv2
import numpy as np
import os

def create_test_video(filename, pattern='line', duration=3, fps=30):
    """Create a synthetic test video with dancers"""
    
    width, height = 640, 480
    frames = []
    
    for frame_idx in range(int(duration * fps)):
        # White background
        img = np.ones((height, width, 3), dtype=np.uint8) * 255
        
        t = frame_idx / fps
        
        if pattern == 'line':
            # Horizontal line of dancers
            for i in range(5):
                x = int(100 + i * 110)
                y = int(240 + 20 * np.sin(t * 2))
                cv2.circle(img, (x, y), 25, (0, 0, 0), -1)
                cv2.circle(img, (x, y - 30), 15, (0, 0, 0), -1)  # Head
                
        elif pattern == 'circle':
            # Circle formation
            for i in range(6):
                angle = i * 2 * np.pi / 6 + t
                x = int(320 + 100 * np.cos(angle))
                y = int(240 + 100 * np.sin(angle))
                cv2.circle(img, (x, y), 25, (0, 0, 0), -1)
                cv2.circle(img, (x, y - 30), 15, (0, 0, 0), -1)
                
        elif pattern == 'v_shape':
            # V formation
            for i in range(7):
                if i < 4:
                    x = int(320 - (i + 1) * 60)
                    y = int(200 + (i + 1) * 40)
                else:
                    x = int(320 + (i - 3) * 60)
                    y = int(200 + (i - 3) * 40)
                cv2.circle(img, (x, y), 25, (0, 0, 0), -1)
                cv2.circle(img, (x, y - 30), 15, (0, 0, 0), -1)
        
        frames.append(img)
    
    # Save video
    out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    for frame in frames:
        out.write(frame)
    out.release()
    
    return filename

def create_formation_video(filename, pattern='line', duration=3, fps=30):
    """Create a formation visualization video"""
    
    width, height = 640, 480
    frames = []
    
    # Define colors for dancers
    colors = [(255, 107, 107), (78, 205, 196), (69, 183, 209), 
              (150, 206, 180), (254, 202, 87), (221, 160, 221)]
    
    for frame_idx in range(int(duration * fps)):
        # Dark background
        img = np.ones((height, width, 3), dtype=np.uint8) * 44  # Dark gray
        
        # Draw grid
        for x in range(0, width, 40):
            cv2.line(img, (x, 0), (x, height), (68, 68, 68), 1)
        for y in range(0, height, 40):
            cv2.line(img, (0, y), (width, y), (68, 68, 68), 1)
        
        t = frame_idx / fps
        
        if pattern == 'line':
            for i in range(5):
                x = int(100 + i * 110)
                y = int(240 + 20 * np.sin(t * 2))
                color = colors[i % len(colors)]
                cv2.circle(img, (x, y), 20, color, -1)
                cv2.putText(img, str(i+1), (x-7, y+7), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
        elif pattern == 'circle':
            for i in range(6):
                angle = i * 2 * np.pi / 6 + t
                x = int(320 + 100 * np.cos(angle))
                y = int(240 + 100 * np.sin(angle))
                color = colors[i % len(colors)]
                cv2.circle(img, (x, y), 20, color, -1)
                cv2.putText(img, str(i+1), (x-7, y+7), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        frames.append(img)
    
    out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    for frame in frames:
        out.write(frame)
    out.release()
    
    return filename

if __name__ == "__main__":
    # Create test videos in /content/ directory
    os.makedirs('content', exist_ok=True)
    
    # Create three test video pairs
    patterns = ['line', 'circle', 'v_shape']
    
    for i, pattern in enumerate(patterns, 1):
        # Original dance video
        input_file = f'content/{i}_input.mov'
        create_test_video(input_file, pattern=pattern, duration=2)
        print(f"Created {input_file}")
        
        # Formation video (ground truth)
        output_file = f'content/{i}_output.mov'
        create_formation_video(output_file, pattern=pattern, duration=2)
        print(f"Created {output_file}")
    
    print("✅ Test videos created successfully!")
