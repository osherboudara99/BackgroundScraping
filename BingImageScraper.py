from bs4 import BeautifulSoup as bs   
import requests
from PIL import Image   
from io import BytesIO as BIO
import os


def image_scrape():
    
    image_amount = input("How many images would you like to scrape? (No more than 12)")

    exceed = True
    while exceed == True:

        try:
            int(image_amount)
        except:
            image_amount = input("Value entered was not a number. Please enter a number >= 12:")
            continue

        if int(image_amount) > 12:
            image_amount = input("No more than 12 images can be saved. Please enter a new value: ")

            try:
                int(image_amount)
            except:
                image_amount = input("Value entered was not a number. Please enter a number >= 12:")
                continue
            if int(image_amount) > 12:
                continue
            else:
                exceed = False
        elif int(image_amount) <= 12:
            exceed = False


    user_search = input("Enter an image search:")
    bing_search_variable = {"q": user_search} 
    dir_name = user_search.replace(" ", "-") + "-images" 


    r = requests.get("http://www.bing.com/images/search", bing_search_variable)
    soup = bs(r.text, "html.parser")
    image_links = soup.findAll("a", {"class": "thumb"})

    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)

    i = 0
    print(image_amount, "images being saved to", dir_name, "directory.")
    
    for item in image_links:
        try:
            
            obj_img = requests.get(item.attrs["href"])
            print("Link of photo being saved:", item.attrs["href"], "\n")
            file_name= item.attrs["href"].split("/")[-1] 
            
            try:
                img = Image.open(BIO(obj_img.content))  
                img.save("./" + dir_name + "/" + file_name, img.format) 
                i += 1
                if i == image_amount:
                    break
            
            except:
                print("Image was not saved.")
        
        except:
            print("Image request failed.")

print("Scrape backgrounds from Bing Search Engine with this awesome image scraper. ")
start = input("Press enter to begin!")

running = True

while running == True:
    image_scrape()

    ans = input("Would you like to search again? (Enter 1 for yes or 2 for no)")

    if ans == 1:
        running = True
    elif ans == 2:
        running = False
    else:
        print("Input was invalid. Program exiting.")
        running = False



