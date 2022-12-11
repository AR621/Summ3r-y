import os

import openai
from flask import Flask, redirect, render_template, request, url_for

openai.api_key = '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'

# openai.api_key_path = '.env'


def index():
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt(prompt),
        temperature=0.1,
    )
    # return redirect(url_for("index", result=response.choices[0].text))
    result = request.args.get("result")
    print(result)


def generate_prompt(prompt):
    # return """Suggest three names for a prompt that is a superhero.
    return """Summarize this text:
    \"{}\"""".format(
        prompt.capitalize()
    )

index()