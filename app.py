import os
import tempfile
from flask import Flask, render_template, request
import ffmpeg
import matplotlib.pyplot as plt
import uuid

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        video_url = request.form['video_url']
        graph_filename = generate_bitrate_graph(video_url)
        return render_template('index.html', graph_filename=graph_filename)
    return render_template('index.html', graph_filename=None)

def generate_bitrate_graph(video_url):
    video_bitrates, audio_bitrates = extract_bitrates(video_url)

    plt.figure()
    plt.plot(video_bitrates, label='Video Bitrate (kbps)')
    plt.plot(audio_bitrates, label='Audio Bitrate (kbps)')
    plt.xlabel('Time (s)')
    plt.ylabel('Bitrate (kbps)')
    plt.legend()
    plt.title('Video and Audio Bitrate Graph')

    unique_id = uuid.uuid4()
    graph_filename = f'static/bitrate_graph_{unique_id}.png'
    plt.savefig(graph_filename)

    return graph_filename

def extract_bitrates(video_url):
    probe = ffmpeg.probe(video_url)
    video_bitrates = []
    audio_bitrates = []

    if 'packets' in probe:
        for packet in probe['packets']:
            if packet['codec_type'] == 'video':
                video_bitrates.append(int(packet['bit_rate']) / 1000)
            elif packet['codec_type'] == 'audio':
                audio_bitrates.append(int(packet['bit_rate']) / 1000)
    else:
        video_stream = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')
        audio_stream = next(stream for stream in probe['streams'] if stream['codec_type'] == 'audio')
        video_bitrates = [int(video_stream.get('bit_rate', 0)) / 1000] * int(float(video_stream['duration']))
        audio_bitrates = [int(audio_stream['bit_rate']) / 1000] * int(float(audio_stream['duration']))

    return video_bitrates, audio_bitrates

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
