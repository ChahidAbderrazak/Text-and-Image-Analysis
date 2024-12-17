import os

import pytest
from dotenv import load_dotenv

from chatbot.chatAPI import ChatGPT, Gemini, LLaMA

# Load the environment variables
load_dotenv(".env-CHATBOT")


@pytest.mark.skipif(False, reason="test not ready yet, Skip for now!")
class Test_TrainingModules:

    def test_chatAPI(self):
        # Run examples
        gpt = ChatGPT(api_key=os.getenv("OPENAI_API_KEY"))
        output = gpt.send_request("Hello!")

        gemini = Gemini(
            api_key=os.getenv("GEMINI_API_KEY"), model=os.getenv("MODEL")
        )
        output = gemini.send_request("Hello!")

        llama = LLaMA(api_key=os.getenv("LLAMA_API_KEY"))
        output = llama.send_request("Hello!")

        assert True  # all request are submitted without error
