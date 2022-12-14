import os

import openai
import requests as req
from flask import Flask, redirect, render_template, request, url_for, flash, session
from werkzeug.utils import secure_filename
# internal imports
import text_examples        # debugging transcript
import partitioner          # for partitioning transcript into smaller subtexts

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTANSIONS = {'.mp3'}
URL = "https://whisper.lablab.ai/asr"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "bajo_bango"
openai.api_key = os.getenv("OPENAI_API_KEY")

test_transcript = text_examples.qchnn_good + \
    text_examples.qchnn_end + text_examples.qchnn_end

# extract partitioned string list from transcript
partitioned_prompt = partitioner.partition_text(test_transcript)

# Routes methods


@app.route("/index_OLD", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        # prompt = ex_prompt_1
        # prompt = text_examples.qchnn_bad
        # prompt = text_examples.qchnn_good + text_examples.qchnn_bad + text_examples.qchnn_end
        # print('PROMPT:\n{}'.format(prompt))
        summary = ""
        for prompt in partitioned_prompt:
            response = openai.Completion.create(
                # model="text-davinci-003",
                max_tokens=768,
                model="text-curie-001",
                prompt=summarize_prompt(prompt),
                temperature=0.1,
                # top_p=0.15
            )
            summary = summary + str(response.choices[0].text)
            # summary = summary + '\n'

        print('RESULT:{}'.format(summary))
        return redirect(url_for("index_OLD", result=summary))

    result = request.args.get("result")

    response = openai.Completion.create(
        # model="text-davinci-003",
        max_tokens=768,
        model="text-curie-001",
        prompt=reformat_prompt(result),
        temperature=0.1,
        # top_p=0.15
    )

    reformatted_result = response.choices[0].text

    return render_template("index_OLD.html", result=result)


@app.route("/", methods=["GET", "POST"])
def new_index():
    if request.method == "POST":
        print("############     POST    ##############")

        # upload file scenerio
        if request.form["upload_button"] == "upload":
            print("upload button clicked!")
            if "file" not in request.files:
                flash("no file to upload")
                return redirect(request.url)
            file = request.files["file"]
            if file and allowed_file(file.filename):
                print(file.filename)
                file.save("uploads/audio.mp3")
                print("file uploaded to uploads/audio.mp3")
                print("transcribe audio --------------------")
                payload = {}
                files = [('audio_file', ('audio.mp3', open(
                    'uploads/audio.mp3', 'rb'), 'audio/mpeg'))]
                response = req.request("POST", URL, data=payload, files=files)
                # extract raw text from the response
                transcript = eval(response.text)['text']
                # session is good for maximum 4000b so we will probable have to find another way
                session['transcript'] = transcript

                return redirect(url_for("summary"))

        # if request.form["paste_url"] == "paste":

        #     pass
    return render_template("index.html")


@app.route("/summary")
def summary():
    if "transcript" in session:
        transcript = session["transcript"]
        partioned_transcript = partitioner.partition_text(transcript)
        print(len(partioned_transcript))
        return render_template("summary.html", text=transcript)
    else:
        return redirect("/")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/example")
def example():
    return render_template("example.html")


# GPT3 methods
def summarize_prompt(prompt):
    # return """Suggest three names for a prompt that is a superhero.
    return """Could you precisely summarize this video? 
    \"{}\"""".format(prompt)


def reformat_prompt(prompt):
    # return """Suggest three names for a prompt that is a superhero.
    return """Could you reformat this text? 
    \"{}\"""".format(prompt)


# upload file methods
def allowed_file(filename):
    index_of_dot = filename.find('.')
    file_extansion = filename[index_of_dot:]
    if file_extansion in ALLOWED_EXTANSIONS:
        return True
    return False
