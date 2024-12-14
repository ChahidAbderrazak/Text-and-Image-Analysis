import logging
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="[%(asctime)s]: %(message)s:")

# list of files to be created in the root directory of the project.
list_of_files_dirs = [
    "data/",
    "models/",
    ".github/workflows/.gitkeep",
    ".github/workflows/cml.yaml",
    "src/__init__.py",
    "src/utils/__init__.py",
    "src/utils/common.py",
    "src/api/__init__.py",
    "src/templates/index.html",
    "src/static/files/",
    "src/main.py",
    "src/webapp.py",
    "src/notebooks/trials.ipynb",
    "tests/test_app.py",
    "config/config.yaml",
    "setup.py",
    "README.md",
    ".env",
    "dvc.yaml",
    "Jenkinsfile",
    "Dockerfile",
    "docker-compose.yml",
    "requirements.txt",
]

# create the directories and files in the root directory of the project.
for filepath in list_of_files_dirs:
    # check/create if the <filepath> is a directory
    if filepath[-1] == "/":
        os.makedirs(filepath)

    else:  # check if the <filepath> is a file
        filepath = Path(filepath)
        directory, filename = os.path.split(filepath)
        if directory != "":
            os.makedirs(directory, exist_ok=True)
            logging.info("Creating directory; {directory} for the file: {filename}")

        if filename != "":
            if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):

                with open(filepath, "w") as f:
                    pass
                    logging.info(
                        f"Creating empty file: {filepath} "
                        + f"[size={os.path.getsize(filepath)}]"
                    )

            else:
                logging.info("{filename} is already exists")
