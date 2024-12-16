# -------------------------- WEB ChatBOT --------------------------
import os
import time

import gradio as gr
from dotenv import load_dotenv

from chatbot.chatAPI import Gemini

# # Load the environment variables
load_dotenv()

# Gemini chat
assert (
    "GEMINI_API_KEY" in os.environ
), "Please include GEMINI_API_KEY in the .env file"
myChatBot = Gemini(
    api_key=os.getenv("GEMINI_API_KEY"), model=os.getenv("MODEL")
)
print(myChatBot.send_request("Hello!"))

# start the chat
chat = myChatBot.chat_model.start_chat(history=[])


# Transform Gradio history to Gemini format
def transform_history(history):
    new_history = []
    for chat in history:
        new_history.append({"parts": [{"text": chat[0]}], "role": "user"})
        new_history.append({"parts": [{"text": chat[1]}], "role": "model"})
    return new_history


def response(message, history):
    global chat
    # The history will be the same as in Gradio,
    #  the 'Undo' and 'Clear' buttons will work correctly.
    chat.history = transform_history(history)
    response = chat.send_message(message)
    response.resolve()

    # Each character of the answer is displayed
    for i in range(len(response.text)):
        time.sleep(0.05)
        yield response.text[: i + 1]


gr.ChatInterface(
    response,
    title=f"Chat with [{myChatBot.model} ]",
    textbox=gr.Textbox(placeholder="Type your question"),
).launch(debug=True)
