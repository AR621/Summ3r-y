import os

import openai
import requests as req
from flask import Flask, redirect, render_template, request, url_for, flash
from werkzeug.utils import secure_filename
import text_examples

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTANSIONS = {'.mp3', '.flac'}
URL = "https://whisper.lablab.ai/asr"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
openai.api_key = os.getenv("OPENAI_API_KEY")
partitioned_prompt = [text_examples.qchnn_good,
                      text_examples.qchnn_bad, text_examples.qchnn_end]


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
        return redirect(url_for("index", result=summary))

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

    return render_template("index_OLD.html", result=result, formatted_result=reformatted_result)


@app.route("/", methods=["GET", "POST"])
def new_index():
    if request.method == 'POST':
        if request.form["submit"] == "upload":
            print("You clicked upload   ##########################")
            if 'file' not in request.files:
                print("no file part")
                return redirect(request.url)
            file = request.files['file']
            print(file)
            file.save("uploads/audio.mp3")
            print("file uploaded to uploads/audio.mp3")
            print("transcribe audio --------------------")
            payload={}
            files = [('audio_file',('audio.mp3',open('uploads/audio.mp3','rb'),'audio/mpeg'))]
            response = req.request("POST", URL, data=payload, files=files)
            print(response.text)

    return render_template("index.html")


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
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTANSIONS