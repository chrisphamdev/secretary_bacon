import openai

openai.api_key = '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'

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=2000,
        n=1,
        stop=None,
        temperature=0.4,
    )
    return response.choices[0].text.strip()