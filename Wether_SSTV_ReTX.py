import pysstv
from PIL import Image
import urllib
import sched, time

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
    s.enterabs(time, 1, # FUNCTION NAME HERE # , (s,))
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
    img = img.crop((1058, 1521, 1870, 2179))
    img = img.resize((320, 240))
    img.save(time + "jpg")

  


# Main 

#scheduler_setup()
get_image()




