#!/bin/bash

# install the pytest-cov packages
echo && echo " - install the pytest-cov packages "
pip install pytest-cov

#--------------------------------------------------------
clear
echo && echo " #################################################" 
echo " ##         LLM & NLP PROJECT           " 
echo " ## Run code tests "
echo " #################################################" && echo 

echo && echo " -> measure  tests coverage report"
# pytest --cov=src/ tests/ --verbose --durations=5 -vv --cov-report html --cov-fail-under 60 
pytest --cov=src/ tests/ --verbose --durations=5 -vv --cov-report term-missing --cov-fail-under 60 

# save the report table as html 
python -m coverage html && rm -rf logs/htmlcov | mv  htmlcov logs/ && 

# show the report table
python -m coverage report
echo && echo "-> The coverage report is saved in : ./logs/htmlcov/index.html"

# ### ----------------   NOTIFICATION MESSAGE -------------------------
# notify-send "Testing execution is Finished!!"