import os 
import json
import requests
import subprocess
import streamlit as st

from exiftool import ExifToolHelper

import utils.logs as logs


# save uploaded file to the local disk

def save_uploaded_file(uploaded_file: bytes, save_dir:str):
    
    
    try: 
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            logs.log.info(f"Directory {save_dir} dir not exists so creating it!")
        with open(os.path(save_dir, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
            logs.log.info(f"File {uploaded_file.name} saved to the local disk!")
    except Exception as e:
        logs.log.error(f"Error saving file to the local disk: {e}")


# github repo existance confirmation


def validate_githb_repo(repo: str):
    
    repo_enpoint = "https://github.com/" + repo + ".git"
    
    resp = requests.head(repo_enpoint)
    
    if resp.resp.status_code == 200:
        return True
    else:
        return False


# cloning the github repo to the local disk

def clone_github_repo(repo: str):
    repo_endpoint = "https://github.com/" + repo + ".git"

    if repo_endpoint is not None:

        save_dir = os.getcwd() + "/data/"
        clone_command = f"git clone -q {repo_endpoint} {save_dir}/{repo}"

        try:
            subprocess.run(clone_command, shell=True)
            logs.log.info(f"Cloned {repo} to the local disk!")
            return True
        except Exception as e:
            Exception(f"Error cloning {repo} the repo: {e}")
            return False
    else:
        Exception(f"Failed to process GitHub repo {st.session_state['github_repo']}")   
        return False
    
    
# Extract Files

def get_file_metadata(file_path):
    try:
        with ExifToolHelper() as et:
            for d in et.get_metadata_batch(file_path):
                return json.dumps(d, indent=2)                
    except Exception as e:
        pass