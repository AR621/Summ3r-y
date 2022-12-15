import openai

API_KEY = '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'
openai.api_key = API_KEY

def request_summary(input_text, temperature=0.1, max_tokens=768):
    summary = ""
    print(input_text)
    for text_partition in input_text:
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

#
# import text_examples
# import partitioner
#
# sum = request_summary(partitioner.partition_text(text_examples.qchnn_whole))
# print(sum)
