#!/bin/bash
clear
echo && echo " #################################################" 
echo " ##         LLM & NLP PROJECT           " 
echo " ##             [TENSORBOARD]           " 
echo " #################################################" && echo 

#--------------------------------------------------------
echo && echo " -> Show the previouly ran experiments"
tensorboard --logdir artifacts/models
