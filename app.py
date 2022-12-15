import os

import openai
import requests as req
from flask import Flask, redirect, render_template, request, url_for, flash, session
from werkzeug.utils import secure_filename
import secrets

# internal imports
import text_examples        # debugging transcript
import partitioner          # for partitioning transcript into smaller subtexts
import summarizer           # for summary requests

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTANSIONS = {'.mp3'}
URL = "https://whisper.lablab.ai/asr"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "bajo_bango"

test_transcript = text_examples.qchnn_good + \
text_examples.qchnn_end + text_examples.qchnn_end


@app.route("/", methods=["GET", "POST"])
def new_index():
    if request.method == "POST":
        print("############     POST    ##############")

        # upload file scenerio
        if request.form.get("upload_button", "") == "upload":
            print("upload button clicked!")
            if "file" not in request.files:
                flash("no file to upload")
                return redirect(request.url)
            file = request.files["file"]
            if file and allowed_file(file.filename):
                # save file to uploads directory and generate an unique name for it
                new_filename = generate_unique_filename(file.filename)
                file.save("uploads/"+new_filename)

                # save the name as a cookie for individual client
                session['file_name'] = new_filename

                # transcribe audio
                filename = session["file_name"]
                response = transcribe_external(filename)
                # extract raw text from the response and save it to txt file in text directory
                transcript = eval(response.text)['text']
                # save_to_file(transcript, "text/"+filename[:-4]+".txt")
                save_to_file(transcript, "text/"+filename[:-4]+".txt")

                return redirect(url_for("summary"))

        # paste url scenerio
        elif request.form.get("url_button", "") == "paste":
            print("paste button clicked")
            if request.form.get("video_url", "") != "":
                url = request.form.get("video_url", "")
                print(url)
            else:
                print("an empty string")
            pass
        else:
            pass
    return render_template("index.html")


@app.route("/summary")
def summary():
    if "file_name" in session:
        # read text from unique text file
        path_to_txt_file = "text/" + session["file_name"][:-4] + ".txt"
        transcript = read_from_file(path_to_txt_file)

        # partition transcript for summary needs
        partioned_transcript = partitioner.partition_text(transcript)
        summary = summarizer.request_summary(partioned_transcript)
        filename = session["file_name"]
        save_to_file(summary, "text/" + 'summary_' + filename[:-4] + ".txt")
        path_to_summary = summary, "text/" + 'summary_' + filename[:-4] + ".txt"

        return render_template("summary.html", audio_transcript=transcript, summary_text=summary, path_to_transcript=path_to_txt_file, path_to_summary=path_to_summary)
    else:
        return redirect("/")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/example")
def example():
    return render_template("example.html")

# upload file methods
def allowed_file(filename):
    index_of_dot = filename.find('.')
    file_extansion = filename[index_of_dot:]
    if file_extansion in ALLOWED_EXTANSIONS:
        return True
    return False


# string file operations
def generate_unique_filename(filename):
    random_string = secrets.token_hex(16)
    return f'{random_string}_{filename}'


def save_to_file(text, filename):
    with open(filename, 'w') as file:
        file.write(text)


def read_from_file(filename):
    with open(filename, 'r') as file:
        return file.read()


def transcribe_external(filename):
    path = "uploads/" + filename
    payload = {}
    files = [('audio_file', (filename, open(
    path, 'rb'), 'audio/mpeg'))]
    return req.request("POST", URL, data=payload, files=files)


app.run(debug=False, host='0.0.0.0', port=2137)
