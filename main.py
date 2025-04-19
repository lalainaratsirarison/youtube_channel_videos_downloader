from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from pytube import YouTube

def scrap_it(channel_url):
    options = Options()
    options.headless = True
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
            print("Fin du chargement")
            print(new_height)
            break
        prev_height = new_height

    contents_container = driver.find_element(By.ID, "contents")
    contents = contents_container.find_elements(By.ID, "video-title-link")
    videos_list = set()
    for content in contents:
        videos_list.add({
            "title": content.get_attribute("title"),
            "link": content.get_attribute("href")
        })
        
    driver.quit()
    

def download_it(video_desc):
    yt = YouTube(f"https://https://www.youtube.com/watch?v={video_desc}")
    print(f"Titre {yt.title}")
    print("Résolutions disponible:\n")
    stream = yt.streams.get_highest_resolution()
    try:
        print(f"{video_desc.title}\nTéléchargement en cours...")
        stream.download(output_path="/videos")
        print("Téléchargement terminé")
    except:
        print("Une erreur est survénue")


def download_all(videos):
    for video in videos:
        download_it(video)


def download_partial(videos, choosen_videos):
    for video in choosen_videos:
        download_it(videos[video])


def get_videos_numbers(choices):
    videos_list = set()
    # if(choices.split(",") )


if __name__ == '__main__':
    channel = input("Coller le lien de la chaine Youtube ici: ") + "/videos"
    videos = scrap_it(channel)
    print(videos)
    # print("Choisir les vidéos à télécharger:\n"
    #     "(exemple: 1 ou 1-9 ou 1,2,5,6)\n")
    # for video in videos:
    #     print(f"{videos.index(video)+1} - {video.title}")
    # choices = input()
