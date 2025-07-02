import cv2
import threading
import pickle
import numpy as np
import json
import os
import base64
import sys
import flet as ft
import sklearn
import pyvirtualcam
from collections import deque, Counter
import time

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

APP_NAME = "BisindoApp"
if sys.platform == "win32":
    APP_DATA_DIR = os.path.join(os.environ['APPDATA'], APP_NAME)
else:
    APP_DATA_DIR = os.path.join(os.path.expanduser('~'), '.config', APP_NAME)

os.makedirs(APP_DATA_DIR, exist_ok=True)
USER_SETTINGS_FILE = os.path.join(APP_DATA_DIR, "settings.json")

mp = None
model = [None]
labels_dict = [None]
model_loaded = [False]
ENABLE_VIRTUAL_CAM = sys.platform != "darwin"

settings = {
    "show_landmarks": True,
    "word_delay": 15,
}

def load_settings():
    global settings
    try:
        if os.path.exists(USER_SETTINGS_FILE):
            with open(USER_SETTINGS_FILE, 'r') as f:
                saved_settings = json.load(f)
                settings.update(saved_settings)
    except Exception as e:
        print(f"Gagal memuat pengaturan: {e}")

prediction_buffer = deque(maxlen=10)
constructed_sentence = ""
frame_counter = 0
last_detection_time = time.time()
hand_detected = False

LINE_SPACING_RATIO = 1.5

def load_heavy_dependencies():
    global mp
    import mediapipe as mp
    model_loaded[0] = True

def load_model():
    try:
        model_path = resource_path("model.p")
        labels_path = resource_path("label_dict.json")
        
        model_dict = pickle.load(open(model_path, 'rb'))
        model[0] = model_dict['model']
        with open(labels_path, 'r') as f:
            labels_dict[0] = json.load(f)
        model_loaded[0] = True
    except Exception as e:
        print(f"❌ Error loading model: {e}")

def generate_placeholder_image():
    blank_image = np.ones((480, 800, 3), dtype=np.uint8) * 255
    _, buffer = cv2.imencode(".png", blank_image)
    return base64.b64encode(buffer).decode("utf-8")

def draw_rounded_rectangle(img, pt1, pt2, color, thickness, radius):
    x1, y1 = pt1
    x2, y2 = pt2
    cv2.ellipse(img, (x1 + radius, y1 + radius), (radius, radius), 180, 0, 90, color, thickness)
    cv2.ellipse(img, (x2 - radius, y1 + radius), (radius, radius), 270, 0, 90, color, thickness)
    cv2.ellipse(img, (x1 + radius, y2 - radius), (radius, radius), 90, 0, 90, color, thickness)
    cv2.ellipse(img, (x2 - radius, y2 - radius), (radius, radius), 0, 0, 90, color, thickness)
    cv2.rectangle(img, (x1 + radius, y1), (x2 - radius, y2), color, thickness)
    cv2.rectangle(img, (x1, y1 + radius), (x2, y2 - radius), color, thickness)

def fix_feature_vector_length(data_aux, expected_length):
    if len(data_aux) < expected_length:
        data_aux += [0.0] * (expected_length - len(data_aux))
    elif len(data_aux) > expected_length:
        data_aux = data_aux[:expected_length]
    return data_aux

def reset_subtitle():
    global constructed_sentence, prediction_buffer, frame_counter, hand_detected
    constructed_sentence = ""
    prediction_buffer.clear()
    frame_counter = 0
    hand_detected = False

def update_sentence():
    global constructed_sentence, frame_counter
    if len(prediction_buffer) > 0:
        most_common = Counter(prediction_buffer).most_common(1)[0][0]
        if most_common != "Unknown":
            if not constructed_sentence or most_common != constructed_sentence.split()[-1]:
                constructed_sentence += (" " + most_common) if constructed_sentence else most_common
    prediction_buffer.clear()
    frame_counter = 0

def wrap_text(text, max_width, font, font_scale, thickness):
    if not text:
        return [], False
    words = text.split(' ')
    lines = []
    current_line = words[0]
    for word in words[1:]:
        test_line = f"{current_line} {word}"
        (width, _), _ = cv2.getTextSize(test_line, font, font_scale, thickness)
        if width > max_width:
            lines.append(current_line)
            current_line = word
        else:
            current_line = test_line
    lines.append(current_line)
    return lines, len(lines) > 2

def start_inference(stop_flag, model_ready, virtual_cam, camera_placeholder, camera_frame, status_text, page):
    def inference_thread():
        status_text.value = "🔄 Model dimuat. Memulai deteksi..."
        page.update()
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            status_text.value = "❌ Kamera tidak ditemukan!"
            page.update()
            return
        _, test_frame = cap.read()
        H, W, _ = test_frame.shape
        
        # Responsive subtitle settings
        text_size = max(0.4, W / 1200)
        text_thickness = max(1, int(text_size * 2))
        margin_bottom = int(H * 0.05) 
        padding = int(W * 0.02)        
        radius = int(padding * 0.8)   
        
        import mediapipe as mp
        hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6
        )
        stop_flag[0] = False
        if ENABLE_VIRTUAL_CAM:
            virtual_cam[0] = pyvirtualcam.Camera(width=W, height=H, fps=30, fmt=pyvirtualcam.PixelFormat.RGB)
        camera_placeholder.content = camera_frame
        page.update()
        global frame_counter, last_detection_time, hand_detected
        while not stop_flag[0]:
            ret, frame = cap.read()
            if not ret: break
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            results = hands.process(frame_rgb)
            
            if results.multi_hand_landmarks:
                if not hand_detected: reset_subtitle()
                hand_detected = True
                last_detection_time = time.time()
                frame_counter += 1
                
                data_aux = []
                x_coords = []
                y_coords = []

                for hand_landmarks in results.multi_hand_landmarks:
                    if settings["show_landmarks"]:
                        mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
                    
                    for lm in hand_landmarks.landmark:
                        x_coords.append(lm.x)
                        y_coords.append(lm.y)

                if x_coords and y_coords:
                    min_x, max_x = min(x_coords), max(x_coords)
                    min_y, max_y = min(y_coords), max(y_coords)
                    
                    hand_height = max_y - min_y
                    if hand_height == 0: hand_height = 1e-6

                    for i in range(len(x_coords)):
                        normalized_x = (x_coords[i] - min_x) / hand_height
                        normalized_y = (y_coords[i] - min_y) / hand_height
                        data_aux.append(normalized_x)
                        data_aux.append(normalized_y)
                
                    data_aux = fix_feature_vector_length(data_aux, 21 * 2 * 2)
                    
                    if model_ready[0]:
                        prediction = model[0].predict([np.asarray(data_aux)])
                        predicted_class = int(prediction[0])
                        predicted_character = labels_dict[0].get(str(predicted_class), "Unknown")
                        prediction_buffer.append(predicted_character)

            if frame_counter >= settings["word_delay"]: update_sentence()

            if hand_detected and time.time() - last_detection_time < 3:
                lines, exceeded = wrap_text(constructed_sentence, W - (padding * 4), cv2.FONT_HERSHEY_SIMPLEX, text_size, text_thickness)
                if lines:
                    (text_w, text_h), _ = cv2.getTextSize(lines[0], cv2.FONT_HERSHEY_SIMPLEX, text_size, text_thickness)
                    line_height = int(text_h * LINE_SPACING_RATIO)
                    
                    total_text_height = len(lines) * line_height - int(text_h * (LINE_SPACING_RATIO - 1))
                    
                    subtitle_bg_height = total_text_height + (padding * 2)
                    subtitle_y_start = H - margin_bottom - subtitle_bg_height
                    
                    overlay = frame.copy()
                    
                    max_line_width = max([cv2.getTextSize(line, cv2.FONT_HERSHEY_SIMPLEX, text_size, text_thickness)[0][0] for line in lines])
                    subtitle_bg_width = max_line_width + (padding * 2)
                    text_x_start = (W - subtitle_bg_width) // 2

                    draw_rounded_rectangle(overlay, (text_x_start, subtitle_y_start), (text_x_start + subtitle_bg_width, subtitle_y_start + subtitle_bg_height), (0, 0, 0), -1, radius)
                    cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
                    
                    for i, line in enumerate(lines):
                        (line_w, line_h), _ = cv2.getTextSize(line, cv2.FONT_HERSHEY_SIMPLEX, text_size, text_thickness)
                        line_x = text_x_start + (subtitle_bg_width - line_w) // 2
                        line_y = subtitle_y_start + padding + line_h + (i * line_height)
                        cv2.putText(frame, line, (line_x, line_y), cv2.FONT_HERSHEY_SIMPLEX, text_size, (255, 255, 255), text_thickness, cv2.LINE_AA)
                
                if exceeded: reset_subtitle()
            else:
                reset_subtitle()

            if ENABLE_VIRTUAL_CAM and virtual_cam[0]: virtual_cam[0].send(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            _, buffer = cv2.imencode(".png", frame)
            camera_frame.src_base64 = base64.b64encode(buffer).decode("utf-8")
            page.update()
        
        cap.release()
        stop_inference(stop_flag, virtual_cam, camera_placeholder, status_text, page)
    
    threading.Thread(target=inference_thread, daemon=True).start()
    status_text.value = "🔄 Deteksi dimulai..."
    page.update()

def stop_inference(stop_flag, virtual_cam, camera_placeholder, subtitle_text, page):
    stop_flag[0] = True
    subtitle_text.value = "⏹️ Deteksi dihentikan."
    camera_placeholder.content = ft.Text("📷", size=100)
    if ENABLE_VIRTUAL_CAM and virtual_cam[0]:
        virtual_cam[0].close()
        virtual_cam[0] = None
    page.update()

load_settings()