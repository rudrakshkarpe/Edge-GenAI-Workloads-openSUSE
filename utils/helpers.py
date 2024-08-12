import os
import json
import requests
import subprocess
import requests
import base64
from io import BytesIO
from PIL import Image

import streamlit as st

from exiftool import ExifToolHelper

import utils.logs as logs


# Save uploaded fileto the disk 

def save_uploaded_file(uploaded_file: bytes, save_dir: str):
    
    try:
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            logs.log.info(f"Directory {save_dir} did not exist so creating it")
        with open(os.path.join(save_dir, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
            logs.log.info(f"Upload {uploaded_file.name} saved to disk")
    except Exception as e:
        logs.log.error(f"Error saving upload to disk: {e}")


# validate github repo url 

def validate_github_repo(repo: str):

    repo_endpoint = "https://github.com/" + repo + ".git"
    resp = requests.head(repo_endpoint)
    if resp.status_code() == 200:
        return True
    else:
        return False


# clone gitub repo

def clone_github_repo(repo: str):
   
    repo_endpoint = "https://github.com/" + repo + ".git"
    if repo_endpoint is not None:
        save_dir = os.getcwd() + "/data"
        clone_command = f"git clone -q {repo_endpoint} {save_dir}/{repo}"
        try:
            subprocess.run(clone_command, shell=True)
            logs.log.info(f"Cloned {repo} repo")
            return True
        except Exception as e:
            Exception(f"Error cloning {repo} GitHub repo: {e}")
            return False

    else:
        Exception(f"Failed to process GitHub repo {st.session_state['github_repo']}")
        return False

# Extracting meta data

def get_file_metadata(file_path):
    
    try:
        with ExifToolHelper() as et:
            for d in et.get_metadata(file_path):
                return json.dumps(d, indent=2)
    except Exception:
        pass
    
# def img_to_base64(uploded_file):
#     buffered = BytesIO()
#     uploded_file.save(buffered, format="PNG")
    
#     return base64.b64encode(buffered.getvalue()).decode()