import requests as req
from flask import escape, Flask, redirect, render_template, request, url_for, flash, session, send_file
from werkzeug.utils import secure_filename
import secrets
import re
import os

# internal imports
from summ3ry import (
    partitioner,  # for partitioning transcript into smaller subtexts
    summarizer,  # for summary requests
    downloader,  # for video file handling
    transcriber,  # for generating transcripts
)
# import partitioner, summarizer, downloader

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTANSIONS = {'.mp3'}
URL = "https://whisper.lablab.ai/asr"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "bajo_bango"


@app.route("/", methods=["GET", "POST"])
def new_index():
    if request.method == "POST":
        print("############     POST    ##############")

        # upload file scenerio
        if request.form.get("upload_button", "") == "upload":
            print("upload button clicked!")

            # CODE BELOW DOES NOTHING, I WILL LET IT BE IN HERE, BECAUSE I AM AFRAID THAT THE SERVICE WILL COLAPSE
            if "file" not in request.files:
                print("not uploading a file")
                flash("no file to upload")

            file = request.files["file"]

            if file and allowed_file(file.filename):
                # save file to uploads directory and generate an unique name for it
                new_filename = generate_unique_filename(file.filename)
                path_uploaded_file = os.path.join(os.path.join(
                    os.path.join(os.getcwd(), "summ3ry"), "uploads"), new_filename)
                file.save(path_uploaded_file)

                # save the name as a cookie for individual client
                session['file_name'] = new_filename
                session['scenerio'] = "file"

                # transcribe audio
                filename = session["file_name"]
                transcript = transcriber.transcribe_audio(path_uploaded_file)
                path_transcript_dir = os.path.join(
                    os.path.join(os.getcwd(), "summ3ry"), "text")
                save_to_file(transcript, os.path.join(
                    path_transcript_dir, filename[:-4]+".txt"))

                return redirect(url_for("summary"))

            else:
                flash(
                    "Empty file or format is not allowed, try to upload file with .mp3 extension")
                return redirect(url_for('new_index'))

        # paste url scenerio
        elif request.form.get("url_button", "") == "paste":
            print("paste button clicked")

            # check if requested url is an empty string
            if request.form.get("video_url", "") != "":
                url = request.form.get("video_url", "")

                # check if requested url is invaild
                if re.search(r'((http(s)?:\/\/)?)(www\.)?((youtube\.com\/)|(youtu.be\/))[\S]+', url):

                    # download a video and split it
                    new_dir = generate_unique_filename("video")
                    downloader.video_download(url, new_dir)
                    # downloader.divide_into_parts(new_dir)

                    # generate a transcript file
                    transcript_video = downloader.transcribe_all(new_dir)
                    path_to_transcript_file = os.path.join(os.path.join(
                        os.path.join(os.getcwd(), "summ3ry"), "text"), new_dir+".txt")
                    save_to_file(transcript_video, path_to_transcript_file)
                    # print("text/" + new_dir + ".txt")
                    session['file_name'] = new_dir
                    session['scenerio'] = 'url'
                    return redirect(url_for("summary"))

                else:
                    flash('Invalid url')
            else:
                flash('Empty url')
    return render_template("index.html"), 200


@app.route("/summary")
# the right one
def summary():
    if "file_name" in session:
        if session['scenerio'] == 'file':
            # read text from unique text file
            path_to_txt_file = os.path.join(os.path.join(os.path.join(
                os.getcwd(), "summ3ry"), "text"), session["file_name"][:-4] + ".txt")

            transcript = read_from_file(path_to_txt_file)

            # partition transcript for summary needs
            partitioned_transcript = partitioner.partition_text(transcript)
            summary = summarizer.request_summary(partitioned_transcript)
            filename = session["file_name"]
            path = os.path.join(os.path.join(os.getcwd(), "summ3ry"), "text")
            summary_path = os.path.join(path, "summary_")
            save_to_file(summary, summary_path + filename[:-4] + ".txt")
            path_to_summary = summary_path + filename[:-4] + ".txt"
            return render_template("summary.html", audio_transcript=transcript, summary_text=summary,
                                   path_to_transcript=f"download/{os.path.basename(path_to_txt_file)}",
                                   path_to_summary=f"download/{os.path.basename(path_to_summary)}")

        elif session['scenerio'] == 'url':
            # read text from unique text file
            path_to_txt_file = os.path.join(os.path.join(os.path.join(
                os.getcwd(), "summ3ry"), "text"), session["file_name"] + ".txt")
            transcript = read_from_file(path_to_txt_file)

            # partition transcript for summary needs
            partitioned_transcript = partitioner.partition_text(transcript)
            summary = summarizer.request_summary(partitioned_transcript)
            filename = session["file_name"]
            path = os.path.join(os.path.join(os.getcwd(), "summ3ry"), "text")
            summary_path = os.path.join(path, "summary_")
            save_to_file(summary, summary_path +
                         filename[:-4] + ".txt")
            path_to_summary = summary_path + filename[:-4] + ".txt"

            return render_template("summary.html", audio_transcript=transcript, summary_text=summary,
                                   path_to_transcript=f"download/{os.path.basename(path_to_txt_file)}", path_to_summary=f"download/{os.path.basename(path_to_summary)}")
        else:
            return redirect('/')
    else:
        return redirect("/")

# let the user download his individual files with summary or transcript


@app.route("/download/<basename>")
def download_file(basename):
    path = os.path.join(os.path.join(os.path.join(
        os.getcwd(), "summ3ry"), "text"), basename)
    return send_file(path, as_attachment=True, attachment_filename=basename)


@app.route("/about")
def about():
    return render_template("about.html"), 200


@app.route("/example")
def example():
    return render_template("example.html"), 200


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
    with open(filename, 'r', encoding="utf-8") as file:
        return file.read()


def transcribe_external(filename):
    path = "uploads/" + filename
    payload = {}
    files = [('audio_file', (filename, open(
        path, 'rb'), 'audio/mpeg'))]
    return req.request("POST", URL, data=payload, files=files)


if __name__ == '__main__':
    app.run(debug=True)
