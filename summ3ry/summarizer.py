import openai
import os


def request_summary(input_text, temperature=0.1, max_tokens=768):
    print(input_text)
    openai.api_key = os.getenv("OPENAI_API_KEY")
    summary = ""
    for text_partition in input_text:
        if text_partition != '':
            response = openai.Completion.create(
                max_tokens=max_tokens,
                model="text-curie-001",
                prompt=summarize_prompt(text_partition),
                temperature=temperature,
            )
            summary = summary + str(response.choices[0].text)
    return summary


# GPT3 methods
def summarize_prompt(prompt):
    return """Could you precisely summarize this audio transcript? 
    \"{}\"""".format(prompt)


def reformat_prompt(prompt):
    return """Could you reformat this text? 
    \"{}\"""".format(prompt)