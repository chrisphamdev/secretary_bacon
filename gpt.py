import openai

openai.api_key = ''

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=2000,
        n=1,
        stop=None,
        temperature=0.4,
    )
    return response.choices[0].text.strip()

def generate_sarcastic_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt="Be sarcastic. " + prompt,
        max_tokens=2000,
        n=1,
        stop=None,
        temperature=0.4,
    )
    return response.choices[0].text.strip()