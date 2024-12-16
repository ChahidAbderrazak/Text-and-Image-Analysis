class HuggingFace_pipeline:

    def __init__(self, model):
        self.model = model

    def predict(self, text):
        if self.model == "facebook/bart-large-cnn":
            from transformers import (
                AutoTokenizer,
                BartForConditionalGeneration,
            )

            self.model = BartForConditionalGeneration.from_pretrained(
                "facebook/bart-large-cnn"
            )
            self.tokenizer = AutoTokenizer.from_pretrained(
                "facebook/bart-large-cnn"
            )
            inputs = self.tokenizer(
                [text], max_length=1024, return_tensors="pt"
            )
            # Generate Summary
            summary_ids = self.model.generate(
                inputs["input_ids"], num_beams=2, min_length=0, max_length=20
            )
            response = self.tokenizer.batch_decode(
                summary_ids,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=False,
            )[0]
            return response


if __name__ == "__main__":

    ARTICLE_TO_SUMMARIZE = (
        "PG&E stated it scheduled the blackouts in response to forecasts for high winds "
        "amid dry conditions. The aim is to reduce the risk of wildfires. Nearly 800 thousand customers were "
        "scheduled to be affected by the shutoffs which were expected to last through at least midday tomorrow."
    )
    chatbot = HuggingFace_pipeline(model="facebook/bart-large-cnn")
    response = chatbot.predict(ARTICLE_TO_SUMMARIZE)
    print(response)
