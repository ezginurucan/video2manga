import cv2
import os
from pytube import YouTube

def downloadyoutube_video(url, output_path):
    yt = YouTube(url)
    stream = yt.streams.filter(file_extension='mp4').get_highest_resolution()
    stream.download(output_path)
    return os.path.join(output_path, stream.default_filename)

def extract_frames(video_path, output_folder):
    # Video dosyasını aç
    cap = cv2.VideoCapture(video_path)

    # Video başarıyla açıldı mı kontrol et
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return

    # Çıktı klasörü mevcut değilse oluştur
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    frame_count = 0
    while True:
        # Frame'i oku
        ret, frame = cap.read()

        # Frame okuyamadıysak döngüden çık
        if not ret:
            break

        # Frame'i kaydet
        frame_filename = os.path.join(output_folder, f"frame{frame_count:04d}.jpg")
        cv2.imwrite(frame_filename, frame)

        # Frame sayacını artır
        frame_count += 1

    # Video dosyasını kapat
    cap.release()
    print(f"Extracted {frame_count} frames from {video_path} to {output_folder}")


youtube_url = 'https://www.youtube.com/watch?v=71xBu_VHTfY'
download_folder = 'downloaded_videos'
output_folder = 'output_frames'


video_path = download_youtube_video(youtube_url, download_folder)