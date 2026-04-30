import cv2
import os
import glob

video_path = "Man_focused_on_laptop_202604301742.mp4"
output_dir = "static/frames"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Clear existing frames
existing_frames = glob.glob(os.path.join(output_dir, "ezgif-frame-*.webp"))
for f in existing_frames:
    try:
        os.remove(f)
    except Exception as e:
        print(f"Error removing {f}: {e}")

cap = cv2.VideoCapture(video_path)
total_frames_in_video = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)

print(f"Video has {total_frames_in_video} frames at {fps} fps.")

TARGET_FRAMES = 240

if total_frames_in_video <= 0:
    print("Error reading video.")
    exit(1)

# We want exactly TARGET_FRAMES. We can select indices evenly spaced.
indices = [int(i * total_frames_in_video / TARGET_FRAMES) for i in range(TARGET_FRAMES)]

frame_count = 0
extracted_count = 0
current_target_idx = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
        
    while current_target_idx < TARGET_FRAMES and frame_count == indices[current_target_idx]:
        out_name = f"ezgif-frame-{current_target_idx + 1:03d}.webp"
        out_path = os.path.join(output_dir, out_name)
        # webp compression: quality 80
        cv2.imwrite(out_path, frame, [cv2.IMWRITE_WEBP_QUALITY, 100])
        extracted_count += 1
        current_target_idx += 1
        
    frame_count += 1
    
    if current_target_idx >= TARGET_FRAMES:
        break

cap.release()
print(f"Extracted {extracted_count} frames to {output_dir}")
