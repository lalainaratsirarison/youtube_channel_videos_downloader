from utils import *

channel = input("Paste the channel URL: ")
channel = channel.strip()
videos = scrap_it(channel)
print(videos)
user_choices = split_input(input("Choose the videos you want to download (1,2,3... or 1-5 etc.): "), videos)
download(user_choices)
print("Thank you for using this program!")
print("Have a nice day!")
print("Lalaina Ratsirarison")