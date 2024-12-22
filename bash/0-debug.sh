#!/bin/bash
pip3 install flake8 black black[jupyter]
# -------------------------- debugging the code -------------------------
echo && echo "[${PROJECT_NAME}][dev] Linting the codes."
###---------------------------------------------------------------------
echo && echo  "Debuging the code..."
python3 -m flake8 . --count --select=E9,F63,F7,F82 --ignore=F541 --show-source --statistics
python3 -m flake8 . --count --ignore=F541,W503 --max-complexity=10 --max-line-length=127 --statistics
python3 -m black . ###check --diff

# -------------------------- testing the code -------------------------
echo && echo "Testing the code..."
python3 -m pytest --verbose
