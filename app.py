from flask import Flask, render_template, request, send_file
import plotbitrate
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        video_url = request.form['video_url']
        graph_image = generate_graph(video_url)
        return render_template('index.html', graph_image=graph_image)
    return render_template('index.html', graph_image=None)

def generate_graph(video_url):
    output_image = "static/graph.png"
    plotbitrate.plot_bitrate(video_url, output_image)
    return output_image

if __name__ == "__main__":
    app.run(debug=True)