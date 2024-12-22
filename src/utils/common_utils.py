import json
import logging
import os
import sys
from pathlib import Path
from typing import Any

import joblib
import yaml
from box import ConfigBox
from box.exceptions import BoxValueError
from dotenv import find_dotenv, load_dotenv
from ensure import ensure_annotations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# setup GIT_PYTHON_REFRESH
os.environ["GIT_PYTHON_REFRESH"] = "quiet"


# functions
def init_logger():
    logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"

    log_dir = "logs"
    log_filepath = os.path.join(log_dir, "running_logs.log")
    os.makedirs(log_dir, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format=logging_str,
        handlers=[
            logging.FileHandler(log_filepath),
            logging.StreamHandler(sys.stdout),
        ],
    )

    logger = logging.getLogger("Project Logger")
    return logger


logger = init_logger()


@ensure_annotations
def setup_fastapi_server() -> object:
    app = FastAPI()

    origins = [
        "http://localhost:4200",
        "http://0.0.0.0:4200",
        "http://127.0.0.1:4200",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


@ensure_annotations
def load_env_variables(verbose: int = 0):
    if verbose > 0:
        print(" -> searching/load for the env files ...")
    list_env_file = [
        env_file
        for env_file in [find_dotenv(".env")] + [find_dotenv(".env-ip")]
        if env_file != ""
    ]
    assert (
        len(list_env_file) > 0
    ), f"\n Neither <.env> nor <.env-ip>  file was found in \
        \n {os.getcwd()}"

    print(f"list_env_file={list_env_file}")

    # loading the env variables
    if verbose > 0:
        print(" -> loading the env variables")
        print(f"\t- list_env_file={list_env_file}")

    for filepath in list_env_file:
        if verbose > 0:
            print(f"\t- loading: {filepath}")
        load_dotenv(filepath)


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """reads yaml file and returns

    Args:
        path_to_yaml (str): path like input

    Raises:
        ValueError: if yaml file is empty
        e: empty file

    Returns:
        ConfigBox: ConfigBox type
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """create list of directories

    Args:
        path_to_directories (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple dirs
        is to be created. Defaults to False.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")


@ensure_annotations
def save_json(path: Path, data: dict):
    """save json data

    Args:
        path (Path): path to json file
        data (dict): data to be saved in json file
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"json file saved at: {path}")


@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """load json files data

    Args:
        path (Path): path to json file

    Returns:
        ConfigBox: data as class attributes instead of dict
    """
    with open(path) as f:
        content = json.load(f)

    logger.info(f"json file loaded successfully from: {path}")
    return ConfigBox(content)


@ensure_annotations
def save_bin(data: Any, path: Path):
    """save binary file

    Args:
        data (Any): data to be saved as binary
        path (Path): path to binary file
    """
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file saved at: {path}")


@ensure_annotations
def load_bin(path: Path) -> Any:
    """load binary data

    Args:
        path (Path): path to binary file

    Returns:
        Any: object stored in the file
    """
    data = joblib.load(path)
    logger.info(f"binary file loaded from: {path}")
    return data


@ensure_annotations
def get_size(path: Path) -> str:
    """get size in KB

    Args:
        path (Path): path of the file

    Returns:
        str: size in KB
    """
    size_in_kb = round(os.path.getsize(path) / 1024)
    return f"~ {size_in_kb} KB"


@ensure_annotations
def plot_columns(
    df: object,
    x_column: list,
    y_columns: list,
    title: str = "",
    subplot: bool = True,
):
    import matplotlib.pyplot as plt

    x_ts = [val[x_column] for val in df.select(x_column).collect()]
    if subplot:
        fig, axs = plt.subplots(len(y_columns))
    for idx, y_column in enumerate(y_columns):
        y_ans_val = [val[y_column] for val in df.select(y_column).collect()]
        if subplot:
            axs[idx].plot(x_ts, y_ans_val, label=y_column)
            axs[idx].legend()  # loc="upper left")
            if idx < len(y_columns) - 1:
                axs[idx].set_xticks([])
        else:
            plt.plot(x_ts, y_ans_val, label=y_column)

    plt.xticks(rotation=80)
    plt.xlabel(x_column)
    plt.legend()  # loc="upper left")
    #  set the title
    if title == "":
        title = "Explore time-series variation"

    if subplot:
        fig.suptitle(title, fontsize=14)
    else:
        plt.title(title)
    # show the canvas
    plt.show()


@ensure_annotations
def save_dict_to_json(dict_: dict, filepath: Path):
    # Save dict to JSON file
    with open(filepath, "w") as outfile:
        json.dump(dict_, outfile)
    outfile.close()


@ensure_annotations
def load_dict_from_json(filepath: Path) -> dict:
    # read json file
    with open(filepath, "r") as file:
        dict_ = json.load(file)
    file.close()
    return dict_


@ensure_annotations
def generate_explode(nb_categories: int) -> list:
    explode = [1 / nb_categories for k in range(nb_categories)]
    return explode
