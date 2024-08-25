from flask import Flask, request, jsonify, render_template, send_file
import pandas as pd
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFilter
import io
import os
import os
import subprocess
import pyttsx3
import smtplib
from email.mime.text import MIMEText
from twilio.rest import Client
import pywhatkit as kit
import requests
from colorama import Fore, Style
from pyfiglet import figlet_format
import sys
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googlesearch import search
from twilio.rest import Client
import requests
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import pyttsx3
import os
import json
import boto3
import urllib.parse
import pymongo
import os
import sys
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import time
from datetime import datetime


app = Flask(__name__)
CORS(app)


# Index Route
@app.route('/')
def index():
    return render_template('index.html')

# 1. Send Email
@app.route('/send-email', methods=['GET', 'POST'])
def send_email():
    if request.method == 'POST':
        try:
            to_email = request.form.get('to_email')
            subject = request.form.get('subject')
            message = request.form.get('message')
            
            # Email sending logic (simplified)
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
            sender_email = 'luciary2004@gmail.com'  # Change to your email
            sender_password = 'jktn erjv phbk lyhb'      # Change to your password

            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            email_message = f"Subject: {subject}\n\n{message}"
            server.sendmail(sender_email, to_email, email_message)
            server.quit()

            return 'Email sent successfully!'
        except Exception as e:
            return f"Failed to send email: {e}"
    return render_template('send_email.html')

# 2. Send SMS
@app.route('/send-sms', methods=['GET', 'POST'])
def send_sms():
    if request.method == 'POST':
        # Get form data
        to_number = request.form.get('to_number')
        message = request.form.get('message')

        # Twilio configuration
        account_sid = 'AC640c7712bd697d63f2f25e98a17362ad'  # Replace with your Twilio SID
        auth_token = '426e3474ca8e3b15af817def247837aa'  # Replace with your Twilio Auth Token
        from_number = '+12565874564'  # Replace with your Twilio phone number

        client = Client(account_sid, auth_token)

        try:
            # Send SMS
            client.messages.create(body=message, from_=from_number, to=to_number)
            return jsonify({"status": "SMS sent successfully"})
        except Exception as e:
            print(f"Error sending SMS: {str(e)}")  # Print the error to console for debugging
            return jsonify({"status": "Failed to send SMS", "error": str(e)})
    return render_template('send_sms.html')


# 3. Scrape Google
@app.route('/scrape-google', methods=['GET', 'POST'])
def scrape_google():
    if request.method == 'POST':
        # Get form data
        query = request.form.get('query')

        if not query:
            return jsonify({"status": "Failed", "error": "No query provided"}), 400

        try:
            # Get the top 5 search results
            search_results = []
            for i, result in enumerate(search(query, num_results=5)):
                search_results.append({"rank": i+1, "url": result})

            return jsonify({"status": "Scraping done", "results": search_results})
        except Exception as e:
            return jsonify({"status": "Failed to scrape", "error": str(e)})
    
    return render_template('scrape_google.html')




# 4. Get Geo Coordinates
@app.route('/get-geo', methods=['GET'])
def get_geo():
    try:
        # Make a request to ipinfo API
        response = requests.get(f"https://ipinfo.io/json?token={IPINFO_API_KEY}")

        if response.status_code != 200:
            return jsonify({"status": "Failed to get geo-coordinates", "error": f"Non-successful status code {response.status_code}"})

        data = response.json()
        return jsonify({
            "status": "Success",
            "coordinates": data.get('loc'),
            "city": data.get('city'),
            "region": data.get('region'),
            "country": data.get('country')
        })
    except Exception as e:
        return jsonify({"status": "Failed to get geo-coordinates", "error": str(e)})


# 5. Convert Text to Audio
@app.route('/text-to-audio', methods=['GET', 'POST'])
def text_to_audio():
    if request.method == 'POST':
        # Get form data
        text = request.form['text']
        engine = pyttsx3.init()

        try:
            # Convert text to audio
            engine.save_to_file(text, 'output_audio.mp3')
            engine.runAndWait()
            return jsonify({"status": "Text converted to audio successfully"})
        except Exception as e:
            return jsonify({"status": "Failed to convert text to audio", "error": str(e)})
    return render_template('text_to_audio.html')

# 6. Control Volume
@app.route('/control-volume', methods=['GET', 'POST'])
def control_volume():
    if request.method == 'POST':
        # Get form data
        level = request.form['level']

        try:
            # Set volume level (This works for Linux. Replace with your system-specific code if necessary)
            os.system(f"amixer -D pulse sset Master {level}%")
            return jsonify({"status": "Volume set successfully"})
        except Exception as e:
            return jsonify({"status": "Failed to set volume", "error": str(e)})
    return render_template('control_volume.html')

# 7. Bulk Email
@app.route('/bulk-email', methods=['GET'])
def bulk_email_form():
    return render_template('bulk_email.html')

@app.route('/send-bulk-email', methods=['POST'])
def send_bulk_email():
    if request.method == 'POST':
        # Get form data
        email_addresses = request.form.get('email')
        message_content = request.form.get('message')

        if not email_addresses or not message_content:
            return jsonify({"status": "Failed", "error": "Email or message is missing"}), 400

        # Split email addresses into a list
        email_list = [email.strip() for email in email_addresses.split(',')]

        try:
            # Send email to each address
            for email in email_list:
                send_email(email, message_content)
            return jsonify({"status": "Emails sent successfully"})
        except Exception as e:
            return jsonify({"status": "Failed to send emails", "error": str(e)})

def send_email(to_email, message_content):
    # Email configuration
    from_email = 'luciary2004@gmail.com'  # Replace with your email
    password = 'jktn erjv phbk lyhb'  # Replace with your email password
    
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = 'Bulk Email Subject'
    
    # Attach the message content
    msg.attach(MIMEText(message_content, 'plain'))
    
    # Connect to SMTP server and send email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
            print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
        raise

###################aws

def launch_rhel_gui_instance():
    # Replace these with your actual details
    rhel_ami_id = 'ami-022ce6f32988af5fa'  # Replace with your RHEL AMI ID (example)
    key_pair_name = 'launch-wizard-1'   # Replace with your Key Pair name
    security_group_id = 'sg-0188986c5be702581'  # Replace with your Security Group ID
    region = 'ap-south-1'  # Replace with your desired region

    # AWS credentials (should be stored securely in production)
    aws_access_key_id = 'AKIA2UC3AKX3XSYCNFZQ'
    aws_secret_access_key = 'i74LR09t0kbUELklsnRd5Y70BfCB4uOFDLCFvIdG'
    
    # Instance name
    instance_name = "MyRHELGUIInstance"

    try:
        ec2 = boto3.resource(
            'ec2',
            region_name=region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

        print("Launching EC2 instance...")
        instance = ec2.create_instances(
            ImageId=rhel_ami_id,
            InstanceType='t2.micro',
            MinCount=1,
            MaxCount=1,
            KeyName=key_pair_name,
            SecurityGroupIds=[security_group_id],
            UserData='''#!/bin/bash
                        yum update -y
                        yum groupinstall "Server with GUI" -y
                        systemctl set-default graphical.target
                        systemctl isolate graphical.target
                        '''
        )

        instance_id = instance[0].id
        print(f'Instance created with ID: {instance_id}')

        # Tag the instance with a name
        ec2.create_tags(
            Resources=[instance_id],
            Tags=[{'Key': 'Name', 'Value': instance_name}]
        )
        print(f'Instance {instance_id} named as {instance_name}')

        # Wait until the instance is running
        print("Waiting for the instance to start...")
        instance[0].wait_until_running()

        # Reload instance attributes to get the public IP address
        instance[0].reload()

        print(f'Instance is running. Public IP address: {instance[0].public_ip_address}')

        # Optionally, you could monitor for the instance to be fully initialized
        instance_state = instance[0].state['Name']
        while instance_state != 'running':
            print(f'Current instance state: {instance_state}')
            time.sleep(10)  # Wait for a few seconds before checking again
            instance[0].reload()
            instance_state = instance[0].state['Name']

        print(f'Instance {instance_id} is now fully running with IP address: {instance[0].public_ip_address}')

    except Exception as e:
        print(f'Error launching EC2 instance: {e}')

if _name_ == "_main_":
    launch_rhel_gui_instance()

# Function to access logs from CloudWatch
def access_cloud_logs():
    logs = boto3.client('logs')
    log_group = input("Enter the CloudWatch log group name: ")
    log_stream = input("Enter the CloudWatch log stream name: ")
    response = logs.get_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        startFromHead=True
    )
    for event in response['events']:
        print(event['message'])
# Function for event-driven architecture with S3 and AWS Transcribe

def event_driven_transcription():
    print("Setting up event-driven transcription...")
    
    s3 = boto3.client('s3')
    transcribe = boto3.client('transcribe')
    
    bucket_name = input("Enter the S3 bucket name: ")
    file_key = input("Enter the S3 file key (e.g., audio.mp3): ")
    
    # Create a unique job name using the file name and timestamp
    job_name = f"{file_key.split('.')[0]}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Start the transcription job
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': f's3://{bucket_name}/{file_key}'},
        MediaFormat='mp3',
        LanguageCode='en-IN',
        OutputBucketName=bucket_name
    )
    print(f"Transcription job '{job_name}' started.")
    
    # Wait for the job to complete
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        job_status = status['TranscriptionJob']['TranscriptionJobStatus']
        if job_status in ['COMPLETED', 'FAILED']:
            break
        print("Waiting for transcription to complete...")
        time.sleep(5)
    
    if job_status == 'COMPLETED':
        transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        print(f"Transcription completed. Transcript URI: {transcript_uri}")
        
        # Fetch and print the transcription
        transcript_response = s3.get_object(Bucket=bucket_name, Key=f"{job_name}.json")
        transcript_text = transcript_response['Body'].read().decode('utf-8')
        
        import json
        transcript_data = json.loads(transcript_text)
        print("Transcribed Text:")
        print(transcript_data['results']['transcripts'][0]['transcript'])
    else:
        print(f"Transcription job '{job_name}' failed.")

# Function to connect Python to MongoDB using Lambda
def connect_python_to_mongodb():
   

    print("connecting.....")
    uri = "mongodb+srv://ritikkumar(username):<password>@cluster0.nudjced.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0&ssl=true&tlsAllowInvalidCertificates=true"

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))


    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    db = client.get_database('NewDb')  # Replace with your database name
    collection = db['Data']  # Replace with your collection name
    
    # Example operation
    document = {'hello': 'kaise ho'}
    collection.insert_one(document)
    
    print("Document inserted into MongoDB.") 

# Function to upload a file to S3
def upload_object_to_s3():
    s3 = boto3.client('s3')
    file_name_with_path = input("Enter the file name with path to upload: ")
    bucket = input("Enter the S3 bucket name: ")
    file_name = input("enter the file name to display: ")

    try:
        s3.upload_file(file_name_with_path, bucket, file_name)
        print(f"File '{file_name}' uploaded successfully to '{bucket}'.")
    except Exception as e:
        print(f"Error: {e}")

# Function to integrate Lambda with S3 and SES
def lambda_s3_ses_integration():
   s3 = boto3.client('s3')
    file_path = input("Enter the full file path of the email list file: ")
    bucket_name = input("Enter the S3 bucket name: ")
    file_name = os.path.basename(file_path)
    
    try:
        s3.upload_file(file_path, bucket_name, file_name)
        print(f"File '{file_name}' uploaded successfully to S3 bucket '{bucket_name}'.")
        print("Lambda function will be triggered to send emails.")
    except Exception as e:
        print(f"Error uploading file to S3: {e}")

# Data Processing Function
def process_data(file):
    df = pd.read_csv(file)
    # Example processing: return basic statistics
    return df.describe().to_dict()

# Image Processing Functions
def crop_face(image):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        return image[y:y+h, x:x+w]
    return image

def apply_filters(image, filter_type):
    pil_img = Image.fromarray(image)
    if filter_type == 'BLUR':
        pil_img = pil_img.filter(ImageFilter.BLUR)
    elif filter_type == 'CONTOUR':
        pil_img = pil_img.filter(ImageFilter.CONTOUR)
    elif filter_type == 'DETAIL':
        pil_img = pil_img.filter(ImageFilter.DETAIL)
    return np.array(pil_img)

def create_custom_image():
    img = np.zeros((200, 200, 3), dtype=np.uint8)
    img[50:150, 50:150] = [255, 0, 0]  # red square
    return img

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    data_summary = process_data(file)
    return jsonify(data_summary)

@app.route('/process_image', methods=['POST'])
def process_image():
    file = request.files['file']
    filter_type = request.form.get('filter', 'BLUR')
    
    img = Image.open(file.stream)
    img = np.array(img)
    
    cropped_img = crop_face(img)
    filtered_img = apply_filters(cropped_img, filter_type)
    
    img_pil = Image.fromarray(filtered_img)
    buf = io.BytesIO()
    img_pil.save(buf, format='PNG')
    buf.seek(0)
    
    return send_file(buf, mimetype='image/png')

@app.route('/create_image', methods=['GET'])
def create_image():
    custom_img = create_custom_image()
    img_pil = Image.fromarray(custom_img)
    buf = io.BytesIO()
    img_pil.save(buf, format='PNG')
    buf.seek(0)
    
    return send_file(buf, mimetype='image/png')
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def send_whatsapp_message(number, message):
    kit.sendwhatmsg_instantly(number, message)

def speak_command_output(command):
    output = subprocess.check_output(command, shell=True).decode()
    speak(output)
    print(output)

def send_email(subject, body, to_email):
    from_email = 'your_email@example.com'
    password = 'your_password'
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)

def send_sms(to_number, message):
    account_sid = 'your_account_sid'
    auth_token = 'your_auth_token'
    client = Client(account_sid, auth_token)
    client.messages.create(body=message, from_='your_twilio_number', to=to_number)

def post_to_social_media(platform, message):
    # Example for Twitter, extend for other platforms
    if platform == 'twitter':
        response = requests.post('https://api.twitter.com/2/tweets', data={'status': message})
        print(response.json())

def change_file_color(file_name, color):
    print(f"{color}{file_name}{Style.RESET_ALL}")

def read_ram():
    ram_info = subprocess.check_output("free -m", shell=True).decode()
    print(ram_info)
    speak(ram_info)

def change_gnome_terminal_appearance():
    # Example: Changing background color using gsettings
    subprocess.run(["gsettings", "set", "org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/", "background-color", "#000000"])

def create_user(username, password):
    subprocess.run(["sudo", "useradd", username])
    subprocess.run(["echo", f"{password}\n{password} | sudo passwd {username}"])

def run_linux_in_browser():
    # Example: Using a web-based terminal service
    pass

def google_search(query):
    subprocess.run(["xdg-open", f"https://www.google.com/search?q={query}"])

def run_windows_software(software):
    subprocess.run(["wine", software])

def sync_folders(source, destination):
    subprocess.run(["rsync", "-av", source, destination])

def text_to_ascii_art(text):
    ascii_art = figlet_format(text)
    print(ascii_art)

def main():
    while True:
        print("Choose an option:")
        print("1. Send WhatsApp message")
        print("2. Speak command output")
        print("3. Send email")
        print("4. Send SMS")
        print("5. Post to social media")
        print("6. Change file color")
        print("7. Read RAM")
        print("8. Change GNOME terminal appearance")
        print("9. Create user")
        print("10. Run Linux in browser")
        print("11. Google search")
        print("12. Run Windows software")
        print("13. Sync folders")
        print("14. Text to ASCII art")
        print("15. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            number = input("Enter number: ")
            message = input("Enter message: ")
            send_whatsapp_message(number, message)
        elif choice == '2':
            command = input("Enter command: ")
            speak_command_output(command)
        elif choice == '3':
            subject = input("Enter subject: ")
            body = input("Enter body: ")
            to_email = input("Enter recipient email: ")
            send_email(subject, body, to_email)
        elif choice == '4':
            to_number = input("Enter number: ")
            message = input("Enter message: ")
            send_sms(to_number, message)
        elif choice == '5':
            platform = input("Enter platform (e.g., twitter): ")
            message = input("Enter message: ")
            post_to_social_media(platform, message)
        elif choice == '6':
            file_name = input("Enter file name: ")
            color = input("Enter color (e.g., red): ")
            change_file_color(file_name, color)
        elif choice == '7':
            read_ram()
        elif choice == '8':
            change_gnome_terminal_appearance()
        elif choice == '9':
            username = input("Enter username: ")
            password = input("Enter password: ")
            create_user(username, password)
        elif choice == '10':
            run_linux_in_browser()
        elif choice == '11':
            query = input("Enter search query: ")
            google_search(query)
        elif choice == '12':
            software = input("Enter software path: ")
            run_windows_software(software)
        elif choice == '13':
            source = input("Enter source folder: ")
            destination = input("Enter destination folder: ")
            sync_folders(source, destination)
        elif choice == '14':
            text = input("Enter text: ")
            text_to_ascii_art(text)
        elif choice == '15':
            break
        else:
            print("Invalid choice")


def run_python_program():
    print("Running Python program...")
    # Add your Python code here

def run_gui_program():
    print("Running GUI program...")
    subprocess.run(["./scripts/run_gui.sh"])

def run_ml_model():
    print("Running ML model...")
    subprocess.run(["./scripts/run_ml_model.sh"])

def run_vlc():
    print("Running VLC player...")
    subprocess.run(["./scripts/run_vlc.sh"])

def run_webserver():
    print("Running webserver...")
    subprocess.run(["./scripts/run_webserver.sh"])

def ssh_into_container():
    print("Connecting to SSH...")
    subprocess.run(["docker", "exec", "-it", "ssh_container", "bash"])

def main():
    if len(sys.argv) < 2:
        print("Usage: python app.py [command]")
        sys.exit(1)

    command = sys.argv[1]
    
    if command == "python":
        run_python_program()
    elif command == "gui":
        run_gui_program()
    elif command == "ml":
        run_ml_model()
    elif command == "vlc":
        run_vlc()
    elif command == "web":
        run_webserver()
    elif command == "ssh":
        ssh_into_container()
    else:
        print("Unknown command")


@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    audio_data = request.files['audio'].read()
    # Process audio_data with a speech-to-text library or API
    # Example: response = some_speech_to_text_service(audio_data)
    return jsonify({"text": "Transcribed text goes here"})

# Example endpoint for capturing a photo
@app.route('/capture-photo', methods=['POST'])
def capture_photo():
    photo_data = request.files['photo'].read()
    # Save or process photo_data
    return jsonify({"message": "Photo captured successfully"})

# Example endpoint for recording a video
@app.route('/record-video', methods=['POST'])
def record_video():
    video_data = request.files['video'].read()
    # Save or process video_data
    return jsonify({"message": "Video recorded successfully"})

# Example endpoint for posting to Instagram
@app.route('/post-to-instagram', methods=['POST'])
def post_to_instagram():
    video_url = request.json['video_url']
    # Example API call to Instagram (authentication and API setup required)
    # response = requests.post('https://api.instagram.com/v1/media/upload', data={'url': video_url})
    return jsonify({"message": "Posted to Instagram successfully"})

# Example endpoint for searching Google (you'll need an API key)
@app.route('/search-google', methods=['GET'])
def search_google():
    query = request.args.get('query')
    api_key = 'YOUR_GOOGLE_API_KEY'
    cx = 'YOUR_CUSTOM_SEARCH_ENGINE_ID'
    response = requests.get(f'https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cx}')
    results = response.json()
    return jsonify(results)

# Example endpoint for generating a ChatGPT response
@app.route('/chatgpt', methods=['POST'])
def chatgpt():
    user_input = request.json['input']
    api_key = 'YOUR_OPENAI_API_KEY'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': user_input}]
    }
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, data=json.dumps(data))
    response_data = response.json()
    return jsonify({"response": response_data['choices'][0]['message']['content']})

# Example endpoint for fetching Docker metrics (this is a placeholder)
@app.route('/docker-metrics', methods=['GET'])
def docker_metrics():
    # You can use Docker API to fetch metrics
    metrics = {
        "memory_usage": "100MB",  # Example values
        "status": "Running",
        "storage": "1GB"
    }
    return jsonify(metrics)


if __name__ == '__main__':
    app.run(debug=True)