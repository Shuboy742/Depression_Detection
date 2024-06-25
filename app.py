# Importing the libraries
import numpy as np
import requests

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import session
import detection_emotion_practice as validate

from flask_migrate import Migrate
import os
import cv2
import keras

from keras.models import load_model

import os, os.path
import cv2
import numpy as np
import cv2
import pickle

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow info and warning messages

app = Flask(__name__)

app.secret_key = '31206b7b80bb51fafd95fcea504e7edc'
app.config['UPLOAD_FOLDER'] = 'static'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# # Initialize Flask-Migrate
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


import pygame
import time

def play_audio(file_path):
    pygame.init()
    pygame.mixer.init()

    try:
        pygame.mixer.music.load(file_path)
        print(f"Playing {file_path}")
        pygame.mixer.music.play()

        # Allow time for the audio to play
        while pygame.mixer.music.get_busy():
            time.sleep(2)

    except pygame.error as e:
        print(f"Error: {e}")

    finally:
        pygame.mixer.quit()

def audio(audio_path):
        # Install and import the necessary libraries
    import speech_recognition as sr

    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Replace 'user_audio.wav' with the actual path to your extracted audio file
    #audio_path = "audio.wav"  # Update this with your audio file's name

    # Function to convert audio speech to text
    def speech_to_text(audio_path):
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            return text


    # Perform speech-to-text conversion on the extracted audio
    text = speech_to_text(audio_path)
    print("Text from video speech:", text)

    from textblob import TextBlob

    # Function to perform sentiment analysis on the text
    def sentiment_analysis(text):
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity
        if sentiment >= 0:
            return "Person is Normal or not Depressed"
        else:
            return "Person is Depressed"

    # Perform sentiment analysis on the text from the audio
    sentiment = sentiment_analysis(text)
    print("Tone of voice:", sentiment)
    return sentiment


from moviepy.editor import VideoFileClip

def detect_emotions(video):

    
    #video = "video/v2.mp4"
    model = Sequential()
    
    model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48,48,1)))
    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    
    model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    
    model.add(Flatten())
    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(7, activation='softmax'))
    
    model.load_weights('models/model.h5')
    
    # Haar cascade classifier for face detection
    face_cascade = cv2.CascadeClassifier('models/haarcascade_frontalface_default.xml')

    # dictionary which assigns each label an emotion (alphabetical order)
    emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
    
    # Initialize counters for each emotion
    emotion_counts = {emotion: 0 for emotion in emotion_dict.values()}
    
    # Initialize total frame count
    total_frames = 0
    
    # Open the video file
    cap = cv2.VideoCapture(video)
    
    # Initialize moviepy video file
    video_clip = VideoFileClip(video)
    # Extract audio file
    audio_clip = video_clip.audio
    audio_clip.write_audiofile("audio/audio.wav")
    
    # Initialize audio file for playing separately
    audio_path = "audio/audio.wav"

    sentiment = audio(audio_path)
    
    
    
    while True:
        ret, img = cap.read()
        if not ret:
            break
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
            prediction = model.predict(cropped_img)
            maxindex = int(np.argmax(prediction))
            emotion = emotion_dict[maxindex]
            emotion_counts[emotion] += 1
            total_frames += 1
            
            cv2.rectangle(img, (x, y - 50), (x + w, y + h + 10), (255, 0, 0), 2)
            cv2.putText(img, emotion, (x + 20, y - 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(img, 'Number of Faces: ' + str(len(faces)), (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 0, 0), 2)
        
        cv2.imshow('Video', cv2.resize(img, (500, 800), interpolation=cv2.INTER_CUBIC))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # Save the complete video
    #video_clip.write_videofile("complete_video.mp4")
    
    
    cap.release()
    cv2.destroyAllWindows()


    


    
    # Calculate percentage of each emotion
    emotion_percentages = {emotion: count / total_frames * 100 for emotion, count in emotion_counts.items()}
    print("emotion_percentages",emotion_percentages)
    
    return emotion_percentages,audio_path,sentiment



    #return maxindex


@app.route('/')
def index():
    return render_template('index.html', video_path=None, emotions=None, audio_path=None, audio_detect=None)

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return redirect(request.url)

    video_file = request.files['video']
    if video_file.filename == '':
        return redirect(request.url)

    if video_file:
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_file.filename)
        video_file.save(video_path)
        
        # Perform emotion detection and audio analysis
        emotions_detected, audio_path, audio_detect = detect_emotions(video_path)
        print(emotions_detected)
        print(audio_path)
        print(audio_detect)
        play_audio(audio_path)
        
        return render_template('index.html', video_path=video_file.filename, emotions=emotions_detected, audio_path=audio_path, audio_detect=audio_detect)

# Render the HTML file for home page
@app.route("/")
def homemain():
    return render_template("home.html")

@app.route("/homepage")
def homepage():
    return render_template("home.html")

@app.route("/depression_session")
def depression_session():
    return render_template("a.html")

@app.route("/home")
def home():
    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # Check if the username or email already exists in the database
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return 'Username already exists!'
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            return 'Email already exists!'

        # Create a new user instance and add it to the database
        new_user = User(full_name=full_name, email=email, username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

       # return 'Registration successful!'

    #return render_template('registration.html')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            # Store the user's ID in the session
            session['user_id'] = user.id
            # Redirect the user to the home page
            return redirect(url_for('home'))
        else:
            message = 'Invalid username or password'
            return redirect(url_for('login'),comment_text =  {message})

    return render_template('login.html')

@app.route('/logout')
def logout():
    # Clear the session data
    session.clear()
    # Redirect the user to the login page
    return redirect(url_for('login'))
 
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

# # For AWS
# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=8080)