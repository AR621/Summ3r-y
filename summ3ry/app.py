import requests as req
from flask import Flask, redirect, render_template, request, url_for, flash, session, send_file
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

ALLOWED_EXTANSIONS = {'.mp3'}

# paths to directories
UPLOAD_FOLDER = os.path.join(os.path.join(os.getcwd(), "summ3ry"), "uploads")
DOWNLOAD_FOLDER = os.path.join(
    os.path.join(os.getcwd(), "summ3ry"), "downloads")
TEXT_FOLDER = os.path.join(os.path.join(os.getcwd(), "summ3ry"), "text")

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
                path_uploaded_file = os.path.join(UPLOAD_FOLDER, new_filename)
                file.save(path_uploaded_file)

                # save the name as a cookie for individual client
                session['file_name'] = new_filename
                session['scenerio'] = "file"

                # transcribe audio
                filename = session["file_name"]
                transcript = transcriber.transcribe_audio(path_uploaded_file)
                save_to_file(transcript, os.path.join(
                    TEXT_FOLDER, filename[:-4]+".txt"))
                session['file_name'] = session['file_name'][:-4]

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

                # check if requested url is vaild
                if re.search(r'((http(s)?:\/\/)?)(www\.)?((youtube\.com\/)|(youtu.be\/))[\S]+', url):

                    # download a video and split it
                    new_dir = generate_unique_filename("video")
                    downloader.video_download(url, new_dir)
                    # downloader.divide_into_parts(new_dir)

                    # generate a transcript file
                    transcript_video = downloader.transcribe_all(new_dir)
                    path_to_transcript_file = os.path.join(
                        TEXT_FOLDER, new_dir+".txt")
                    save_to_file(transcript_video, path_to_transcript_file)
                    session['file_name'] = new_dir
                    session['scenerio'] = 'url'
                    return redirect(url_for("summary"))

                else:
                    flash('Invalid url')
            else:
                flash('Empty url')
    return render_template("index.html", latest_summary=check_if_last_summary_valid()), 200


@app.route("/summary")
# the right one
def summary():
    if "file_name" in session:
        if check_if_transcript_and_summary_exist(session["file_name"]):
            filename = session["file_name"]
            transcript_file_name = filename + ".txt"
            summary_file_name = 'summary_'+filename[:-4] + ".txt"

            transcript_path = os.path.join(TEXT_FOLDER, transcript_file_name)
            summary_path = os.path.join(TEXT_FOLDER, summary_file_name)
            transcript = read_from_file(transcript_path)
            summary = read_from_file(summary_path)
            return render_template("summary.html", audio_transcript=transcript, summary_text=summary,
                                   path_to_transcript=f"download/{os.path.basename(transcript_path)}", path_to_summary=f"download/{os.path.basename(summary_path)}", latest_summary=check_if_last_summary_valid())
        else:
            if check_if_transcript_file_exists(session["file_name"]):
                if session['scenerio'] == 'file':
                    # read text from unique text file
                    path_to_txt_file = os.path.join(
                        TEXT_FOLDER, session["file_name"]+ ".txt")
                    transcript = read_from_file(path_to_txt_file)

                    # partition transcript for summary needs
                    partitioned_transcript = partitioner.partition_text(
                        transcript)
                    summary = summarizer.request_summary(
                        partitioned_transcript)
                    filename = session["file_name"]
                    # file operations
                    summary_path = os.path.join(TEXT_FOLDER, "summary_")
                    path_to_summary_file = summary_path + \
                        filename[:-4] + ".txt"
                    save_to_file(summary, path_to_summary_file)
                    return render_template("summary.html", audio_transcript=transcript, summary_text=summary,
                                           path_to_transcript=f"download/{os.path.basename(path_to_txt_file)}",
                                           path_to_summary=f"download/{os.path.basename(path_to_summary_file)}", latest_summary=check_if_last_summary_valid())

                elif session['scenerio'] == 'url':
                    # read text from unique text file
                    path_to_txt_file = os.path.join(
                        TEXT_FOLDER, session["file_name"] + ".txt")
                    transcript = read_from_file(path_to_txt_file)

                    # partition transcript for summary needs
                    partitioned_transcript = partitioner.partition_text(
                        transcript)
                    summary = summarizer.request_summary(
                        partitioned_transcript)
                    filename = session["file_name"]
                    # file operations
                    summary_path = os.path.join(TEXT_FOLDER, "summary_")
                    path_to_summary_file = summary_path + \
                        filename[:-4] + ".txt"
                    save_to_file(summary, path_to_summary_file)

                    return render_template("summary.html", audio_transcript=transcript, summary_text=summary,
                                           path_to_transcript=f"download/{os.path.basename(path_to_txt_file)}", path_to_summary=f"download/{os.path.basename(path_to_summary_file)}", latest_summary=check_if_last_summary_valid())
            else:
                print('no transcript file')
                return redirect('/')
    else:
        print('no file name in session')
        return redirect("/")

# let the user download his individual files with summary or transcript


@app.route("/download/<basename>")
def download_file(basename):
    path = os.path.join(TEXT_FOLDER, basename)
    return send_file(path, as_attachment=True, attachment_filename=basename)


@app.route("/about")
def about():
    return render_template("about.html", latest_summary=check_if_last_summary_valid()), 200


@app.route("/example")
def example():
    return render_template("example.html", latest_summary=check_if_last_summary_valid()), 200


# upload file method
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


def check_if_transcript_and_summary_exist(filename) -> bool:
    content_of_TEXT_FOLDER = os.listdir(TEXT_FOLDER)
    summary_file = 'summary_'+filename[:-4] + ".txt"
    transcript_file = filename + ".txt"
    if summary_file in content_of_TEXT_FOLDER and transcript_file in content_of_TEXT_FOLDER:
        return True
    else:
        return False


def check_if_transcript_file_exists(filename) -> bool:
    print(f'{filename}')
    print('####')
    content_of_TEXT_FOLDER = os.listdir(TEXT_FOLDER)
    transcript_file = filename + ".txt"
    print(content_of_TEXT_FOLDER)
    print(f'{transcript_file}')
    if transcript_file in content_of_TEXT_FOLDER:
        return True
    else:
        return False


def check_if_last_summary_valid() -> bool:
    if 'file_name' in session:
        if check_if_transcript_and_summary_exist(session["file_name"]):
            return True
        else:
            return False
    else:
        return False


if __name__ == '__main__':
    app.run(debug=True)
