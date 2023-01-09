# <<< Import libraries  >>>

from pysstv.color import Robot36

from PIL import Image
from pydub import AudioSegment
from pydub.playback import play
import urllib.request, os, sched, sys, struct, time 
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

    #sstv_wav = AudioSegment.from_wav(go_time + ".wav")
    #play(sstv_wav)
    increment_time()
    scheduler_setup()
    



# <<< Main Program >>>

scheduler_setup()





