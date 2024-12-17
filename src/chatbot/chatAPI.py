import os

import google.generativeai as genai
import openai
from dotenv import load_dotenv
from llamaapi import LlamaAPI

# Load the environment variables
load_dotenv(".env-CHATBOT")


class ChatAPI:
    def __init__(self, api_key, model):
        """Initialize with API key and model name."""
        self.api_key = api_key
        self.model = model

    def send_request(self, prompt):
        """Placeholder for sending requests to the API."""
        raise NotImplementedError(
            "This method should be implemented by subclasses."
        )


class ChatGPT(ChatAPI):
    def __init__(self, api_key, model="gpt-4o-mini"):
        super().__init__(api_key, model)
        self.chat_model = openai.OpenAI(api_key=api_key)
        self.model = model

    def send_request(self, prompt):
        """Send a request to OpenAI"s ChatGPT API."""
        response = self.chat_model.chat.completions.create(
            model=self.model, messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]


class Gemini(ChatAPI):

    def __init__(self, api_key, model="gemini-1.5-flash"):
        super().__init__(api_key, model)
        genai.configure(api_key=api_key)
        # Model configuration
        self.chat_model = genai.GenerativeModel(model)  # ("gemini-1.5-flash"")
        self.model = model

    def send_request(self, prompt):
        response = self.chat_model.generate_content(prompt)
        response.resolve()
        return response.text


class LLaMA(ChatAPI):

    def __init__(self, api_key, model="llama3.1-70b"):
        super().__init__(api_key, model)
        self.endpoint = "https://llama.api.endpoint/v1/generate"
        self.chat_model = LlamaAPI(api_key)
        self.model = model

    def send_request(self, prompt):
        """Send a request to the LLaMA API."""

        api_request_json = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        }

        # send the request
        response = self.chat_model.run(api_request_json)

        return response.json()["choices"][0]["message"]


if __name__ == "__main__":

    # Example usage
    gpt = ChatGPT(api_key=os.getenv("OPENAI_API_KEY"))
    print(gpt.send_request("Hello!"))

    gemini = Gemini(
        api_key=os.getenv("GEMINI_API_KEY"), model=os.getenv("MODEL")
    )
    print(gemini.send_request("Hello!"))

    llama = LLaMA(api_key=os.getenv("LLAMA_API_KEY"))
    print(llama.send_request("Hello!"))
