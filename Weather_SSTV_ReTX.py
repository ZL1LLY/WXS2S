from pysstv.color import Robot36

from PIL import Image
import urllib.request, os, sched, sys, struct


#img = Image.open("320x256rgb.png")
#sstv = MartinM1(img, 44100, 16)

# Define a functions
  
# A function to increment time in time.txt by 2 hours in unix time 
def increment_time():
    with open("time.txt", "r") as f:
        time = f.read()
        f.close()   
    time = int(time)
    time = time + 7200
    with open("time.txt", "w") as f:
        f.write(str(time))
        f.close()


def scheduler_setup():

    # Load time for get image and transmit form file 
    with open("time.txt", "r") as f:
        time = f.read()
        f.close() 

    # Setup scheduler
    s = sched.scheduler(time.time, time.sleep)
    s.enterabs(time, 1, get_image(), (s,))
    s.run()



# Download https://kiwiweather.com/goes/himawari_9_fd_IR-sanchez.jpg from server and crop it then save it to file 

def get_image(): 

    # Get time from file 
    with open("time.txt", "r") as f:
        time = f.read()
        f.close()   
    
    # Download image from server
    urllib.request.urlretrieve("https://kiwiweather.com/goes/himawari_9_fd_IR-sanchez.jpg", "image.jpg")
    # Crop image and resize it to 320x240 
    img = Image.open("image.jpg")
    img = img.crop((1086, 1561, 1750, 2059))
    img = img.resize((320, 240))
    #Save image as unix time of when it needs to be transmitted
    img.save(time + ".jpg")
    os.remove("image.jpg")
    build_sstv()

def build_sstv():
    # Get time from file 
    with open("time.txt", "r") as f:
        time = f.read()
        f.close()   
    img = Image.open(time + ".jpg")
    sstv = Robot36(img, 44100, 16)
    sstv.write_wav(time + ".wav")



# Main Program 

#scheduler_setup()
get_image()




