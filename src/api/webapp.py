import sys

import uvicorn
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from utils.serve_tensorflow import (
    loaded_clf_model,
    loaded_tokenizer,
    predict_text_sentiment,
)

IMAGE_DEMO = "static/files/prediction.jpg"
IMAGE_ERROR = "static/files/error.jpg"
CONFIG_FILE = "config/config.yml"


# initialize the Flask API
app = FastAPI()

# # initialize the DATABASE
# sql_cnx = utils.SQL_initializations(CONFIG_FILE)


try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
    templates = Jinja2Templates(directory="templates/")
except Exception as e:
    app.mount("/static", StaticFiles(directory="src/api/static"), name="static")
    templates = Jinja2Templates(directory="src/api/templates/")
    print(f"Error with mounting the templates and static directories {e}")
else:
    sys.exit()


@app.get("/")
def read_form(request: Request):
    result = "home"
    return templates.TemplateResponse(
        "index.html", context={"request": request, "result": result}
    )


# Define the prediction endpoint
@app.post("/predict", response_class=HTMLResponse)
async def predict_sentiment(request: Request, text: str = Form(...)):

    if text == "":
        status_AI = "Error: No text was inserted!!"
        msg_home_page = " No text was inserted!!.\nPlease type/copy English text."

        return templates.TemplateResponse(
            "index.html",
            context={
                "request": request,
                "text": text,
                "msg_home_page": msg_home_page,
                "status_AI": status_AI,
            },
        )

    else:
        # Predict the class
        text, prediction, prediction_msg = predict_text_sentiment(
            text=text,
            tokenizer=loaded_tokenizer,
            model=loaded_clf_model,
            verbose=1,
        )

        # get labels and score
        label = prediction["label"]
        score = prediction["score"]
        score_str = f"{round(100*score,1)}%"  # convert 0-1 score to percentage

        status_AI = " predicted successfully!"

        return templates.TemplateResponse(
            "predict_sentiment.html",
            context={
                "request": request,
                "text": text,
                "label": label,
                "score": score_str,
                "status_AI": status_AI,
            },
        )


def prepare_parser():
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Code template")
    parser.add_argument(
        "--port",
        default=8080,
        metavar="input port",
        help="API server port",
        type=str,
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        metavar="host IP address",
        help="API server IP address",
        type=str,
    )

    return parser


if __name__ == "__main__":
    # get the input parameters
    parser = prepare_parser()
    args = parser.parse_args()

    # run the UVICORN server
    uvicorn.run(app, host=args.host, port=args.port)
