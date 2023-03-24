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
        graph_filename = generate_bitrate_graph(video_url)
        return render_template('index.html', graph_filename=graph_filename)
    return render_template('index.html', graph_filename=None)

def generate_bitrate_graph(video_url):
    # Create the bitrate graph
    graph_filename = f"static/bitrate_graph_{uuid.uuid4().hex}.png"

    # Run the plotbitrate command with the desired options
    command = f"plotbitrate -o {graph_filename} {video_url}"
    subprocess.run(command, shell=True, check=True)

    return graph_filename

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
