import re
import cv2
import os
from dotenv import load_dotenv

def time_to_seconds(time_str):
    minutes, seconds = map(int, time_str.split(':'))
    return minutes * 60 + seconds

def get_frames_for_transcript(transcript_file):
    frames = []
    load_dotenv()
    video_path=os.getenv("VIDEO_PATH")

    cap = cv2.VideoCapture(video_path)  
    if not cap.isOpened():
        print("Video file can not be opened")
        return frames
    
    frame_rate = cap.get(cv2.CAP_PROP_FPS)  
    print(frame_rate)
    frame=0

    with open(transcript_file, 'r') as file:
        for line in file:
            time_match = re.match(r'(\d+):(\d+)', line.strip())
            if time_match:
                minutes, seconds = map(int, time_match.groups())
                print(minutes,"min ",seconds,"sec")
                time_seconds = minutes * 60 + seconds
                frame_number = round(time_seconds * frame_rate)
                frames.append(frame_number)
                frame+=1

    cap.release()
    return frames


transcript_file = "transcript-data.txt"
frames_for_transcript = get_frames_for_transcript(transcript_file)


print(frames_for_transcript)
