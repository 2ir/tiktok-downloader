import requests
import json
from bs4 import BeautifulSoup
import re
import os
import random
import urllib.request
import string




menu = """[1] Download Video
[2] Download Video Sound
[3] Download Profile Picture
"""


user_agents = []
with open("user_agents.json", "r", encoding="UTF-8") as user_agents_file:
    user_agents_json = json.loads(user_agents_file.read())
    for user_agent in user_agents_json:
        user_agents.append(user_agent["ua"])



def make_valid_filename(input_str):
    valid_chars = string.ascii_letters + string.digits + "_.-"
    input_str = "".join(c if c in valid_chars else "_" for c in input_str)
    input_str = re.sub(r'\.+', '.', input_str)
    input_str = re.sub(r'__+', '_', input_str)
    input_str = input_str.strip("._")
    if not input_str:
        input_str = "unnamed_file"
    return input_str


def get_video_id_app(url):
    try:
        r = requests.get(url, headers={"User-Agent": random.choice(user_agents)})
        soup = BeautifulSoup(r.text, "html.parser")
        meta_tag = soup.find("meta", attrs={"property": "al:ios:url"})
        content_value = meta_tag.get("content")
        match = re.search(r"/detail/(\d+)\?", content_value)
        if match:
            video_id = match.group(1)
            return video_id
        else:
            video_id = None
            print("[<] Not Found")
    except requests.exceptions.MissingSchema:
        video_id = None
        print("[<] Invalid url")
    return video_id


def get_video_id(url):
    pattern = r"/video/([^/?]+)"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        video_id = get_video_id_app(url)
        return video_id


def download_pfp(username):
    os.system("cls" if os.name == "nt" else "clear")
    print(f"[<] Downloading Profile Picture of @{username}\n\n")
    try:
        url = f"https://www.tiktok.com/@{username}/"
        r = requests.get(url, headers={"User-Agent": random.choice(user_agents)})
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            try:
                json_data = json.loads(soup.find(id="SIGI_STATE").text.strip())
                pfp_url = json_data["UserModule"]["users"][username]["avatarLarger"]
                pfp = requests.get(pfp_url, headers={"User-Agent": random.choice(user_agents)}).content
                file_path = os.path.join("profile pics", f"{username}_pfp.png")
                urllib.request.urlretrieve(pfp_url, file_path)
                print(f"[<] Profile Picture saved as {username}_pfp.png in the 'profile pics' folder")
            except Exception as e:
                print(r.text)
                print(f"Erorr: {e}")
        elif r.status_code == 404:
            print(f"[<] Username '{username}' Not Found")
        elif r.status_code == 403:
            print(r.status_code)
            print(r.text)
    except Exception as e:
        print(f"[<] Error: {e}")
    input()
    os.system("cls" if os.name == "nt" else "clear")
    

def download_video(video_id):
    try:
        url = f"https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={video_id}"
        r = requests.get(url, headers={"User-Agent": random.choice(user_agents)})
        video_url = r.json()["aweme_list"][0]["video"]["play_addr"]["url_list"][0]
        file_path = os.path.join("videos", f"{video_id}.mp4")
        urllib.request.urlretrieve(video_url, file_path)
        print(f"[<] Video saved as {video_id}.mp4 in the 'videos' folder")
    except Exception as e:
        print(f"[<] Error: {e}")
    input()
    os.system("cls" if os.name == "nt" else "clear")


def download_sound(video_id):
    try:
        url = f"https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={video_id}"
        r = requests.get(url, headers={"User-Agent": random.choice(user_agents)})
        sound_url = r.json()["aweme_list"][0]["music"]["play_url"]["url_list"][0]
        file_path = os.path.join("sounds", f"{video_id}.mp3")
        urllib.request.urlretrieve(sound_url, file_path)
        print(f"[<] Sound saved as {video_id}.mp3 in the 'sounds' folder")
    except Exception as e:
        print(f"[<] Error: {e}")
    input()
    os.system("cls" if os.name == "nt" else "clear")



def main():
    os.system("cls" if os.name == "nt" else "clear")
    while True:
        print(menu)
        option = input("[>] ")
        if option == "1":
            os.system("cls" if os.name == "nt" else "clear")
            print("[<] URL\n\n")
            video_url = input("[>] ")
            os.system("cls" if os.name == "nt" else "clear")
            
            video_id = get_video_id(url=video_url)
            if video_id:
                print("[<] Downloading...\n\n")
                download_video(video_id)
            else:
                input()
                os.system("cls" if os.name == "nt" else "clear")
        elif option == "2":
            os.system("cls" if os.name == "nt" else "clear")
            print("[<] URL\n\n")
            video_url = input("[>] ")
            os.system("cls" if os.name == "nt" else "clear")
            video_id = get_video_id(url=video_url)
            if video_id:
                print("[<] Downloading...\n\n")
                download_sound(video_id)
            else:
                input()
                os.system("cls" if os.name == "nt" else "clear")
        elif option == "3":
            os.system("cls" if os.name == "nt" else "clear")
            print("[<] username\n\n")
            username = input("[>] @")
            
            download_pfp(username)
        else:
            os.system("cls" if os.name == "nt" else "clear")


main()
