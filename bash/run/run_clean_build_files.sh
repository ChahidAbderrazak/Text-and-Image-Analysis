#!/bin/bash
clear
echo && echo " #################################################" 
echo " ##         LLM & NLP PROJECT           " 
echo " ## Clean the build files "
echo " #################################################" && echo 

#--------------------------------------------------------
echo && echo " -> Clean the __pycache__ folders "
rm -rfv `find -type d -name *__pycache__*`

echo && echo " -> Clean the .pyc files "
rm -fv `find -type f -name *.pyc`

echo && echo " -> Clean the checkpoint folders "
rm -rfv `find -type d -name *checkpoint*`

echo && echo " -> Clean the pytest_cache folders "
rm -rfv `find -type d -name *.pytest_cache*`


echo && echo " -> Done"