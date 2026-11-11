import os
import subprocess

def make_round(input_path, folder):
    output_path = os.path.join(folder, "round.mp4")

    command = [
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-t", "60",
        "-vf", "crop=min(iw\\,ih):min(iw\\,ih),scale=384:384",
        "-c:v", "libx264",
        "-preset", "fast",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "128k",
        "-movflags", "+faststart",
        output_path
    ]

    subprocess.run(command, check=True, capture_output=True)
    return output_path