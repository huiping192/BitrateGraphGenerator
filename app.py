import os
import tempfile
from flask import Flask, render_template, request
import ffmpeg
import matplotlib.pyplot as plt
import uuid
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        video_url = request.form['video_url']
        video_graph_filename, audio_graph_filename = generate_bitrate_graph(video_url)
        return render_template('index.html', video_graph_filename=video_graph_filename, audio_graph_filename=audio_graph_filename)
    return render_template('index.html', video_graph_filename=None, audio_graph_filename=None)

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
