import requests
import zipfile
import os
import shutil

def get_latest_release_info(repo):
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def download_asset(asset_url, dest_path):
    headers = {"Accept": "application/octet-stream"}
    response = requests.get(asset_url, headers=headers, stream=True)
    response.raise_for_status()
    with open(dest_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def get_local_version(version_file):
    try:
        with open(version_file, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "0.0.0"

def update_local_version(version_file, new_version):
    with open(version_file, "w") as f:
        f.write(new_version)
