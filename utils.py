from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from pytube import YouTube


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
            print(new_height)
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


def download(videos):
    video_count = 1
    for video in videos:
        yt = YouTube(f"https://https://www.youtube.com/watch?v={video['link']}")
        print(f"({video_count + 1} / {len(videos)}) - {yt.title}")
        stream = yt.streams.get_highest_resolution()
        try:
            print(f"{video['title']}\nDownloading...")
            stream.download(output_path="/videos")
            print("Download complete")
        except:
            print("An error occured while downloading")


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
        else:
            result.append(choices[int(part) - 1])
    return result

