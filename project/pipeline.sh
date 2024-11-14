#!/bin/bash

#As a pre-requisite, 
#   1. Please make sure to be signed in to kaggle
#   2. Go to kaggle settings and create a new token (under API section). This will generate a "kaggle.json" file
#   3. Make a kaggle folder in your home directory (C:\Users\{your_username}\.kaggle).
#      You may use this command to check your home directory in command prompt: echo %USERPROFILE%
#   4. Place the "kaggle.json" file in the folder you created in step3
#   5. Please install the following imports before running the pipeline:
#        import requests
#        import sqlite3
#        import pandas as pd
#        import os
#        import zipfile
#        import kagglehub

python3 ./project/pipeline.py