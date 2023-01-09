"""
WXS2S (WX-Sat-2-SSTV) v1.0.2
Copyright © Lilly Chapman 2023

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 or later of the License.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. 
"""

# <<< Import libraries  >>>

from pysstv.color import Robot36

from PIL import Image, ImageDraw
from pydub import AudioSegment

# <<< Use playsound version 1.2.2 >>>
from playsound import playsound

import urllib.request, os, time 
import shutil


# <<< Define a functions >>>
  
# A function to increment time in time.txt by 2 hours in unix time 
def increment_time():
    with open("time.txt", "r") as f:
        go_time = f.read()
        f.close()   
    go_time = int(go_time)
    go_time = go_time + 7201 # <<< Add one second because of rounding in converting to int 
    with open("time.txt", "w") as f:
        f.write(str(go_time))
        f.close()



def scheduler_setup():

    # Load time for get image and transmit form file 
    with open("time.txt", "r") as f:
        go_time = int(f.read())
        f.close() 

    if go_time < int(time.time()):
        print("Time is not set correctly...") 
        exit()

    #Clear the old stuff 
    try:
        os.remove(str(go_time - int(14400)) + ".jpg")
        os.remove(str(go_time - int(14400)) + ".wav")
    except FileNotFoundError:
        print("No >4h old files found...")
    
    # <<< Debug >>>
    #print(go_time)
    #print((go_time - int(time.time())))
    # <<< Debug >>>

    time.sleep((go_time - int(time.time())))
    get_image()


# Download https://kiwiweather.com/goes/himawari_9_fd_IR-sanchez.jpg from server and crop it then save it to file 

def get_image(): 

    # Get time from file 
    with open("time.txt", "r") as f:
        go_time = f.read()
        f.close()   
    
    # Download image from server
    try:
        urllib.request.urlretrieve("https://kiwiweather.com/goes/himawari_9_fd_IR-sanchez.jpg", "image.jpg")
        crop_image()

    except Exception:
        print("Something went wrong while trying to fetch the image from the internet...")
        shutil.copy("error.jpg", go_time + ".jpg")
        build_sstv()


def crop_image():
    # Get time from file 
    with open("time.txt", "r") as f:
        go_time = f.read()
        f.close()  

    # Crop image and resize it to 320x240 
    img = Image.open("image.jpg")
    img = img.crop((1086, 1561, 1750, 2059))
    img = img.resize((320, 240))
    #Save image as unix time of when it needs to be transmitted
    img.save(go_time + ".jpg")
    os.remove("image.jpg")
    build_sstv()


def build_sstv():
    # Get time from file 
    with open("time.txt", "r") as f:
        go_time = f.read()
        f.close()   

    #Watermark 
    background = Image.open(go_time + ".jpg")
    foreground = Image.open("overlay.png")

    background.paste(foreground, (0, 0), foreground)
    
    background.save(go_time + ".jpg")

    img = Image.open(go_time + ".jpg")
    sstv = Robot36(img, 44100, 16)
    sstv.write_wav(go_time + ".wav")

    #Add TTS Header 
    header_sound = AudioSegment.from_wav("Header.wav")
    sstv_sound = AudioSegment.from_wav(go_time + ".wav")
    
    combined_sounds = header_sound + sstv_sound
    combined_sounds.export((go_time + ".wav"), format="wav")
    print("Generation successful!")
    tx_sstv()


def tx_sstv():
    # Get time from file 
    with open("time.txt", "r") as f:
        go_time = f.read()
        f.close()   

    playsound(go_time + ".wav")
    increment_time()
    scheduler_setup()
    



# <<< Main Program >>>
print("\n")
print("WXS2S (WX-Sat-2-SSTV)")
print("Development Version! You need to remove these files and download the source form the releases tab!\n")
print("Copyright © Lilly Chapman 2023")
print("WXS2S is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. \nSee the GNU General Public License for more details.\n")
scheduler_setup()






