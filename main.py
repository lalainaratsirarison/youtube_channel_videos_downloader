from utils import *

channel_url = input("Paste the channel URL: ")
channel_url = channel_url.strip()
videos = get_all_videos(channel_url)
print_videos(videos)
user_choices = split_input(input("Choose the videos you want to download (1,2,3... or 1-5 etc.): "), videos)
download(user_choices)
print("Thank you for using this program!")
print("Have a nice day!")
print("Lalaina Ratsirarison")