import os

import openai
from flask import Flask, redirect, render_template, request, url_for
import text_examples

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
partitioned_prompt = [text_examples.qchnn_good, text_examples.qchnn_bad, text_examples.qchnn_end]


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


@app.route("/")
def new_index():

    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/example")
def example():
    return render_template("example.html")
def summarize_prompt(prompt):
    # return """Suggest three names for a prompt that is a superhero.
    return """Could you precisely summarize this video? 
    \"{}\"""".format(prompt)


def reformat_prompt(prompt):
    # return """Suggest three names for a prompt that is a superhero.
    return """Could you reformat this text? 
    \"{}\"""".format(prompt)
