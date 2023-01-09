# WXS2S (WX-Sat-2-SSTV)
**Please read the manual**

WXS2S or WX-Sat-2-SSTV is a program designed to fetch satellite images from a web server periodically then transmit them in the Robot 36 SSTV format with an overlay. 

By default the program is set up to fetch images from KiwiWether.com (Thanks to ZL1MDE for their work on KiwiWeather!) and transmit them every 2 hours.

**WXS2S is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. Images produced SHOULD NOT be used for meteorological use.**

## Installation and Setup 
1. Download the latest release from the [releases page](https://github.com/ZL1LCD/WXS2S/releases) **Do not git clone the repository**.
2. Unzip the file to a folder of your choice. 
3. Set a UNIX timestamp in the time.txt file to when you next want it to transmit an image. **The program will automatically increment this after initially being set* 
4. Replace overlay.png and Header.wav with your own files. **Do not transmit on the air with the default files!** 
5. Run pip install -r requirements.txt to install the requirements
6. Run WXS2S_Main.py

## Common Errors 
- **Time not set correctly**,  The UNIX timestamp is not set correctly please check the time.txt file.
- **Something went wrong while trying to fetch the image from the internet...**, The program was unable to fetch the image from the internet. Check your internet connection and try again, an error message will be transmitted instead of an image.

## If The Program Stops
If the program stops (or your computer restarts) you can restart the program. The program sound continue on and transmit on the time that is in the time.txt file, if this time has passed the program will produce a "Time not set correctly" error if so please manually update the time.

## To Do
- [ ] Add support for adding the time the image was taken to the overlay. 

 



