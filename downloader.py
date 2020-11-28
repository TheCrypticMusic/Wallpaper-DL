from pathlib import Path
from bs4 import BeautifulSoup
import requests
import random


class WallpaperDownloader:
    images = []

    def __init__(self, wallpaper, resolution, folder_name):
        """Search for wallpaper and resolution"""
        self.wallpaper = wallpaper
        self.resolution = resolution
        self.website = f"https://wallhaven.cc/search?q={self.wallpaper}&categories=100&purity=100&resolutions={self.resolution}&sorting=relevance&order=desc"
        self.folder_name = folder_name
        self.number_of_wallpapers = None
        
    def search(self):
        res = requests.get(self.website)
        self.soup = BeautifulSoup(res.text, 'lxml')
        self.number_of_wallpapers = self.soup.h1.get_text()
        print(self.number_of_wallpapers)
        if self.number_of_wallpapers[0] == '0':
            print('Try again')
        else:

            return self.__add_images_to_list()

    def __add_images_to_list(self):
        for picture in self.soup.find_all('a', {'class': 'preview'}):
            url_link = picture['href']
            image_id = url_link.split('/')[4]
            self.images.append(image_id)

    def download_content(self, number_of_photos):
        # user_input = input('How many would you like to download?\n1:) One\n2:) Bulk\n')
        if number_of_photos == 'One':
            return self.__download_single_image()
        else:
            return self.__download_bulk_images()

    def __download_bulk_images(self):
        for image in self.images:
            with open(f"{self.folder_name}/{image}.jpg", 'wb') as f:
                self.download_link = f'https://w.wallhaven.cc/full/{image[0:2]}/wallhaven-{image}.jpg'
                print(f'Downloading: {self.download_link}')
                f.write(requests.get(self.download_link).content)

    def __download_single_image(self):
        single_image = random.choice(self.images)
        with open(f"{self.folder_name}/{single_image}.jpg", 'wb') as f:
            self.download_link = f'https://w.wallhaven.cc/full/{single_image[0:2]}/wallhaven-{single_image}.jpg'
            print(f'Downloading: {self.download_link}')
            f.write(requests.get(self.download_link).content)

