from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from settings import *
import time
import sys
import shutil
import os
import yt_dlp
import platform



def show_ffmpeg_install_guide():
    os_name = platform.system()

    print("FFmpeg is required.")
    print("This is how to install it :")

    if os_name == "Windows":
        print("- Go to https://www.gyan.dev/ffmpeg/builds/")
        print("- Download the 'release full' version")
        print("- Extract the ZIP file")
        print("- Add the 'bin' folder to your system PATH environment variable")
    elif os_name == "Linux":
        print("- Run: sudo apt install ffmpeg  (for Debian/Ubuntu)")
        print("- Or:  sudo pacman -S ffmpeg     (for Arch)")
    elif os_name == "Darwin":
        print("- Run: brew install ffmpeg")
    else:
        print("- Go to https://ffmpeg.org/download.html and follow the installation instructions for your system")

    sys.exit(1)
        

def download(videos):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Directory created : {output_folder}")

    for i, video in enumerate(videos):
        try:
            video_url = video['link']
            print(f"\n({i + 1} / {len(videos)}) - {video['title']}")
            print(f"Downloading... {video_url}")

            ydl_opts = {
                'format': f'bv*[height<={video_res}]+ba[ext=m4a]/b[height<={video_res}]',
                'merge_output_format': 'mp4',
                'outtmpl': 'videos/%(title)s.%(ext)s',
                'noplaylist': True,
                'quiet': False,
                'verbose': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])

        except Exception as e:
            print(f"\nAn error occurred: {e}\n")


def get_all_videos(channel_url):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(), options=options)
    driver.get(f'{channel_url}/videos')

    prev_height = 0
    footer = driver.find_element(By.ID, "footer")

    while True:
        delta_y = footer.rect['y']
        ActionChains(driver).scroll_by_amount(0, delta_y).perform()
        time.sleep(5)
        
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if prev_height == new_height:
            break
        prev_height = new_height

    contents_container = driver.find_element(By.ID, "contents")
    contents = contents_container.find_elements(By.ID, "video-title-link")
    videos_list = []
    for content in contents:
        videos_list.append({
            "title": content.get_attribute("title"),
            "link": content.get_attribute("href")
        })
        
    driver.quit()
    return videos_list


def print_videos(videos):
    for i, video in enumerate(videos):
        print(f"{i + 1} - {video['title']}\n")


def split_input(user_input, choices):
    result = []
    parts = user_input.split(",")

    for part in parts:
        part = part.strip()

        if "-" in part:
            start_num, end_num = part.split("-")
            start_num = int(start_num)
            end_num = int(end_num)

            for i in range(start_num, end_num + 1):
                if i > len(choices):
                    break
                result.append(choices[i - 1])
        elif part == "*":
            result.extend(choices)
        else:
            result.append(choices[int(part) - 1])
    return result

