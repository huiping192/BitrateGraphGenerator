import os
import tempfile
from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import uuid
import subprocess
import json
import datetime
from fractions import Fraction

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        video_url = request.form['video_url']
        
        video_info = get_video_info(video_url)
        
        frame_rate_graph_filename = f"static/frame_rate_graph_{uuid.uuid4().hex}.png"
        generate_frame_rate_graph(video_url, frame_rate_graph_filename)

        video_bitrate_graph_filename, audio_bitrate_graph_filename = generate_bitrate_graph(video_url)
        
        return render_template('index.html', video_info=video_info, video_bitrate_graph_filename=frame_rate_graph_filename, audio_bitrate_graph_filename=audio_bitrate_graph_filename)
    return render_template('index.html', video_info=None, video_bitrate_graph_filename=None, audio_bitrate_graph_filename=None)

def get_video_info(video_url):
    # Create a temporary file to store the FFprobe output
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as fp:
        # Run FFprobe to get the video information
        subprocess.run(['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', video_url], stdout=fp)
        fp.flush()

        # Load the JSON data from the file
        with open(fp.name) as f:
            data = json.load(f)

    # Extract the video information from the FFprobe output
    video_info = {}
    for stream in data['streams']:
        if stream['codec_type'] == 'video':
            video_info['codec'] = stream['codec_name']
            video_info['resolution'] = f"{stream['width']}x{stream['height']}"
            video_info['frame_rate'] = f"{Fraction(stream['r_frame_rate']).limit_denominator()}"
            video_info['duration'] = f"{datetime.timedelta(seconds=float(data['format']['duration']))}"
            break
    return video_info

def extract_frame_rates(video_url):
    # Run FFprobe to get the video information
    command = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', video_url]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    # Extract the frame rates from the FFprobe output
    frame_rates = []
    for stream in json.loads(result.stdout)['streams']:
        if stream['codec_type'] == 'video':
            try:
                rate = float(stream['r_frame_rate'])
            except ValueError:
                # Convert the frame rate to a fraction and extract the numerator and denominator
                rate = float(Fraction(stream['r_frame_rate']))
            frame_rates.append(rate)

    return frame_rates

def generate_frame_rate_graph(video_url, frame_rate_graph_filename):
    # Extract the frame rates from the video
    frame_rates = extract_frame_rates(video_url)

    # Run FFprobe to get the duration of the video
    command = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', video_url]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    duration = float(json.loads(result.stdout)['format']['duration'])

    # Plot the frame rate graph
    plt.plot(range(len(frame_rates)), frame_rates)
    plt.xlabel('Frame')
    plt.ylabel('Frame Rate (fps)')
    plt.title(f'Frame Rate vs. Frame Index (Duration: {duration:.2f}s)')
    plt.savefig(frame_rate_graph_filename)
    
def generate_bitrate_graph(video_url):
    # Create the bitrate graphs
    video_graph_filename = f"static/video_bitrate_graph_{uuid.uuid4().hex}.png"
    audio_graph_filename = f"static/audio_bitrate_graph_{uuid.uuid4().hex}.png"

    # Run the plotbitrate command with the desired options for video and audio bitrate graphs
    video_command = f"plotbitrate -o {video_graph_filename} {video_url}"
    subprocess.run(video_command, shell=True, check=True)

    audio_command = f"plotbitrate -o {audio_graph_filename} -s audio {video_url}"
    subprocess.run(audio_command, shell=True, check=True)

    return video_graph_filename, audio_graph_filename

    return graph_filename

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
