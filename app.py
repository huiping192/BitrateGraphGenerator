import os
import tempfile
from flask import Flask, render_template, request
import ffmpeg
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        video_url = request.form['video_url']
        generate_bitrate_graph(video_url)
        return render_template('index.html')
    return render_template('index.html')

def generate_bitrate_graph(video_url):
    # Extract the video and audio bitrates
    video_bitrates, audio_bitrates = extract_bitrates(video_url)

    # Generate the bitrate graph
    fig, ax = plt.subplots()
    ax.plot(video_bitrates, label='Video')
    ax.plot(audio_bitrates, label='Audio')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Bitrate (kbps)')
    ax.legend()

    # Save the graph to a temporary file
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        plt.savefig(f.name)
        graph_path = f.name

    return graph_path

def extract_bitrates(video_url):
    probe = ffmpeg.probe(video_url)
    video_bitrates = []
    audio_bitrates = []

    for packet in probe['packets']:
        if packet['codec_type'] == 'video':
            video_bitrates.append(int(packet['bit_rate']) / 1000)
        elif packet['codec_type'] == 'audio':
            audio_bitrates.append(int(packet['bit_rate']) / 1000)

    return video_bitrates, audio_bitrates

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
