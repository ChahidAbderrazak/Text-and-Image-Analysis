#!/bin/bash
# # ! TODO - bug: does not run inside docker. 
# echo && echo " - install the Node.js and npm packages "
apt-get install -y nodejs npm 
apt-get install -y default-jre

echo && echo " - install selenium-side-runner package "
npm install -g selenium-side-runner

npm install -g chromedriver

#--------------------------------------------------------
clear
echo && echo " #################################################" 
echo " ##         LLM & NLP PROJECT           " 
echo " ## Run selenium-side-runner tests "
echo " #################################################" && echo 

echo && echo " -> Run  Selenium Tests"
selenium-side-runner  tests/selenium-tests/LSTM_sentiment-analysis.side 


# ### ----------------   NOTIFICATION MESSAGE -------------------------
# notify-send "Selenium Testing execution is Finished!!"