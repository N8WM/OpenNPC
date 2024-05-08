from openai import OpenAI
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import pickle
import os

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
model = "lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF"

sessions_file_path = "saved_sessions.pkl"

def load_sessions():
    if os.path.exists(sessions_file_path):
        # Read Pickle data back into a dictionary
        with open(sessions_file_path, "rb") as pickle_file:
            sessions = pickle.load(pickle_file)
        return sessions
    return None

def get_session(chat_id, sessions):
    if chat_id not in sessions:
        sessions[chat_id] = []
    return sessions[chat_id]

def send_system_preset(sessionID, preset, sessions):
    session = get_session(sessionID, sessions)
    completion = client.chat.completions.create(
        model=model,
        messages= session + [
            {"role": "system", "content": preset}
        ],
        temperature=0.7,
    )
    session.append({"role": "system", "content": preset})
    sessions[sessionID] = session
    return completion.choices[0].message.content

def send_chat(sessionID, chat, sessions):
    session = get_session(sessionID, sessions)
    completion = client.chat.completions.create(
        model=model,
        messages= session + [
            {"role": "user", "content": chat}
        ],
        temperature=0.7,
    )
    session.append({"role": "user", "content": chat})
    session.append({"role": "system", "content": completion.choices[0].message.content})
    sessions[sessionID] = session
    return completion.choices[0].message.content

def save_data(sessions):
    with open(sessions_file_path, "wb") as pickle_file:
        pickle.dump(sessions, pickle_file)