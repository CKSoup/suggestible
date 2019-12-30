# suggestible

This program accepts a CSV in the format of the given meals.csv file where you can set whether or not a meal should be included when generating the list “active” column, give meals names and set whether meals are vegetarian or not. Based on this csv and the past results saved in the log file a new list of suggestions is generated. Meals included in the last suggestions are less likely to be drawn in the current list. Using my app the CSV file can be edited graphically and all necessary parameters can be set graphically.

To successfully create a windows exe you first need to install all necessary dependencies then you can run:

pyinstaller --onedir --windowed --icon=icon.ico suggestible.py

In order for the suggestible.exe to work you will need to copy all plotly libraries to the suggestible folder as well as the meals.csv, log, main.py and tablegui.py, template_suggestions.html and suggestions.html.

Alternatively you can download the complete zip file here: 

https://mega.nz/#!DoYH2aZR!CXoBkv88zluIJFxVPAUA6zNZq6u2i7A83BCAHXzDRYQ

The author and copyright holder of this program is Noah Tropper, CKSoup. 
