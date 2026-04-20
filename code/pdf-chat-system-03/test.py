

from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-4.1-mini",
    input="Write a short poem about space"
)

print(response.output[0].content[0].text)