from Flask import Flask, render_template, Response
import cv2
import numpy as np
import mediapipe as mp
import bmf
from fight_move_detector import *
app = Flask(__name__)

# Global variables
video_capture = None
bmf_graph = None
detected_video = None

def initialize_bmf():
    global bmf_graph, detected_video
    bmf_graph = bmf.graph()
    video = bmf_graph.decode({'input_path': 0})  # 0 for webcam
    detected_video = video['video'].module('fighting_move_detector')

def generate_frames():
    global bmf_graph, detected_video
    
    if bmf_graph is None or detected_video is None:
        initialize_bmf()
    
    for packet in bmf.encode(detected_video, None, {'output_path': '-'}).run_wo_block():
        if packet.timestamp == bmf.Timestamp.EOF:
            break
        
        frame = packet.get(bmf.VideoFrame).numpy()
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)