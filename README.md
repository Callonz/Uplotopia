# Uplotopia

Hey there!
I made this so I could use my custom uploader that I made for ShareX on Linux as well.

I use this script on my server:  https://pastebin.com/ReuYJka0

This project focuses on the custom uploader part, I'm not trying to copy ShareX entirely as there are many project out there doing this already.


## Features
* Take and upload a screenshot of the entire screen.
* Crop a screenshot and upload the area of said screenshot.
* Uploading text from clipboard.


## Upcoming features
* Uploading files from clipboard.
* GUI to configure the the values.



## Setup
* Download uplotopia.py.
* Edit the file and change the following variables set in the config block.
  * `url` corresponds to `$uploadhost` in the aforementioned script.
  * `passwd` corresponds to `$key`.
  * `folderpath` states where the screenshots will be saved.


## Usage
You can call this script from the terminal with 

`python uplotopia.py fullscreen` for a screenshot of the entire screen, or


`python uplotopia.py area` if you want to select an area. 


`python uplotopia.py text` to upload text in your clipboard. 

The easiest way of using this is if you create a custom keyboard shortcut and set either of these as commands for them.


## Dependencies
You will need to install the following packages:

`sudo apt-get install python-pil`

`sudo apt-get install python-tk`

`pip install pyscreenshot`

`pip install requests`

`pip install playsound`

`pip install pygame`

`pip install pygtk`

`sudo pip install pyperclip`

## Troubleshooting

You might be getting an error with pyperclip, this means there is no engine it can work with.

Possible fix: `sudo apt-get install xsel`

More information: https://pyperclip.readthedocs.io/en/latest/introduction.html
