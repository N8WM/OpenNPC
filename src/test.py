# Example: reuse your existing OpenAI setup
from openai import OpenAI
from bs4 import BeautifulSoup

# with open('inputs.xml', 'r') as f:
#     data = f.read()
# Bs_data = BeautifulSoup(data, "xml")
# # print(Bs_data)
# system_prompt = Bs_data.find('systemprompt').contents

# print(system_prompt)

with open('NPCmanager_prompt.txt', 'r') as f:
    NPCmanager_prompt = f.read()

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

completion = client.chat.completions.create(
    model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
    messages=[
        {"role": "user", "content": NPCmanager_prompt}
    ],
    temperature=0.7,
)
content = completion.choices[0].message.content
Bs_data = BeautifulSoup(content, "xml")



# inputs = ["Jett and Knox are villagers. Jett and Knox are friends, but they are currently fighting, because Knox keeps borrowing money from Jett without returning it. They met in a tavern when they were both traveling. Jett has never met the Player. Knox has never met the Player. Respond with \"Got it!\" and stop."]

# for input in inputs:
#     completion = client.chat.completions.create(
#     model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
#     messages=[
#         {"role": "system", "content": "Always answer in rhymes."},
#         {"role": "user", "content": "Introduce yourself."}
#     ],
#     temperature=0.7,
#     )

# print(completion.choices[0].message)