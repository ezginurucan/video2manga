import cv2
import numpy as np
from scipy.spatial import distance
import os

def estimate_motion_parameters(frame1, frame2):
    # Convert frames to grayscale
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    
    # Calculate optical flow using Lucas-Kanade method
    flow = cv2.calcOpticalFlowFarneback(gray1, gray2, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    
    # Flatten flow vectors and compute motion parameters
    flow_flat = flow.reshape(-1, 2)
    x, y = np.indices(gray1.shape)
    x_flat = x.flatten()
    y_flat = y.flatten()
    A = np.column_stack((np.ones_like(x_flat), x_flat, y_flat))
    motion_params, _, _, _ = np.linalg.lstsq(A, flow_flat, rcond=None)
    
    return motion_params

def classify_motion_parameters(motion_params):
    a0, a1, a2, a3, a4, a5 = motion_params.flatten()
    b_pan = a0
    b_tilt = a3
    b_zoom = (a1 + a5) / 2
    b_rot = (a4 - a2) / 2
    b_hyp = np.abs((a1 - a5) / 2) + np.abs((a4 + a2) / 2)
    
    catID=max(b_pan,b_tilt,b_zoom,b_rot,b_hyp)
    if (b_pan == b_tilt == b_zoom == b_rot == b_hyp == 0):
        category="static"
    elif(catID==b_pan):
        category="pan"
    elif(catID==b_tilt):
        category="tilt"
    elif(catID==b_zoom):
         category="zoom"
    elif(catID==b_hyp):
         category="hyp"
    elif(catID==b_rot):
         category="rot"
    
    return {
        'category':category
    }

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    shot_segments = []
    frame_count = 0
    
    ret, frame1 = cap.read()
    
    while ret:
        ret, frame2 = cap.read()
        
        if not ret:
            break
        
        motion_params = estimate_motion_parameters(frame1, frame2)
        
        motion_classification = classify_motion_parameters(motion_params)
        
        motion_classification['frame'] = frame_count
        
        shot_segments.append(motion_classification)
       
        frame_count += 1
        
        frame1 = frame2
    
    cap.release()
    
    return shot_segments, frame_count

def group_shot_segments(shot_segments):
    grouped_segments = []
    current_segment = None
    
    for segment in shot_segments:
        if current_segment is None:
            current_segment = segment
        elif current_segment['category'] == segment['category']:
            current_segment['end_frame'] = segment['frame']
        else:
            grouped_segments.append(current_segment)
            current_segment = segment
            current_segment['start_frame'] = segment['frame']
            current_segment['end_frame'] = segment['frame']
    
    if current_segment is not None:
        grouped_segments.append(current_segment)
    
    return grouped_segments

video_path = "C:\\Users\\LENOVO\\Downloads\\Meet Buckbeak  Harry Potter and the Prisoner of the Azkaban.mp4"
shot_segments, total_frames = process_video(video_path)

grouped_segments = group_shot_segments(shot_segments)
for segment in grouped_segments:
    print(segment)
