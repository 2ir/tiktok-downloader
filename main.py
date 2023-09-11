import requests
import json
from bs4 import BeautifulSoup
import re
import os
import random
import urllib.request




menu = """
[1] Download Video
[2] Download Sound
[3] Download Profile Picture
"""


user_agents = []
with open("user_agents.json", "r", encoding="UTF-8") as user_agents_file:
    user_agents_json = json.loads(user_agents_file.read())
    for user_agent in user_agents_json:
        user_agents.append(user_agent["ua"])


def get_video_id_app(url):
    r = requests.get(url, headers={"User-Agent": random.choice(user_agents)})
    soup = BeautifulSoup(r.text, "html.parser")
    meta_tag = soup.find("meta", attrs={"property": "al:ios:url"})
    content_value = meta_tag.get("content")
    match = re.search(r"/detail/(\d+)\?", content_value)
    video_id = match.group(1)
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
    print(f"[<] Downloading Profile Picture of @{username}")
    try:
        url = f"https://www.tiktok.com/@{username}/"
        r = requests.get(url, headers={"User-Agent": random.choice(user_agents)})
        soup = BeautifulSoup(r.text, 'html.parser')
        json_data = json.loads(soup.find(id="SIGI_STATE").text.strip())
        pfp_url = json_data["UserModule"]["users"][username]["avatarLarger"]
        pfp = requests.get(pfp_url, headers={"User-Agent": random.choice(user_agents)}).content
        with open(f"{username}_pfp.png", "wb") as file:
            file.write(pfp)
        print(f"[<] Saved as {username}_pfp.png")
    except Exception as e:
        print(f"[<] Error: {e}")
    input()
    os.system("cls" if os.name == "nt" else "clear")
    

def download_video(video_id):
    try:
        url = f"https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={video_id}"
        r = requests.get(url, headers={"User-Agent": random.choice(user_agents)})
        video_url = r.json()["aweme_list"][0]["video"]["play_addr"]["url_list"][0]
        urllib.request.urlretrieve(video_url, f"{video_id}.mp4")
        print(f"[<] Saved as {video_id}.mp4")
    except Exception as e:
        print(f"[<] Error: {e}")
    input()
    os.system("cls" if os.name == "nt" else "clear")


def download_sound(video_id):
    try:
        url = f"https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={video_id}"
        r = requests.get(url, headers={"User-Agent": random.choice(user_agents)})
        sound_url = r.json()["aweme_list"][0]["music"]["play_url"]["url_list"][0]
        urllib.request.urlretrieve(sound_url, f"{video_id}.mp3")
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
            video_id = get_video_id(url=video_url)
            print(f"\n\n[<] {video_id}")
            download_video(video_id)
            
        elif option == "2":
            os.system("cls" if os.name == "nt" else "clear")
            print("[<] URL\n\n")
            video_url = input("[>] ")
            video_id = get_video_id(url=video_url)
            print(f"\n\n[<] {video_id}")
            download_sound(video_id)
            
        elif option == "3":
            os.system("cls" if os.name == "nt" else "clear")
            print("[<] username")
            username = input("[>] @")
            download_pfp(username)



main()
