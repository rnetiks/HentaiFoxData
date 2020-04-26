# HentaiFoxData
Contains scraped datamaps and scripts to search them.

Tags v1 is outdated!

MultiSearch features an executable to search trough the entire HentaiFox database for galleries with the matching criteria.

MultiSearchv1 contains:
1. A datamap with every gallery on Hentaifox.com
2. A Search.exe to search for galleries with certian criteria.
3. An Updater.exe to update the datamap and search for gaps. I'd suggest running once or twice a week. The standard values are set for a fast update without searching for gaps in the whole datamap.
4. A counter.exe to rewrite the data.json, which contains the amount of galleries all having a certain criteria. I suggest running it from time to time (after updates to the datamap). You can also use the data.json to look how much entries each criteria has.

DO NOT CHANGE ANY .JSON FILES!

Don't worry if starting the .exe files takes a bit. 
This project is written in Python3.8 using PyQt5 as GUI. Conversion to executables by Pyinstaller.


How to use Search.exe:

The GUI is pretty self explanatory but anyways...
Select the type of criteria you want to filter the list for with the dropdownmenu.
You can type the frist letters of the criteria you're searching for if you don't want to search forever.
Select a criterian by clicking on it and add it to the searchcriterias (right list).
If you want to remove a criteria, select it in the right list and click the remove button.
You can add as many criterias as you like.
To start the searchengine just click the Search button at the bottom.
You can find the .txt containing the URLs to the galleries in a folder called "results".

How to use Updater.exe:

With the first slider you can select the first gallery which the script is going to search for.
With the second slider you can select the last gallery which the script is going to search for.
The script will search for every gallery inbetween these two numbers. The minimum is 1 and the maximum the currently newest gallery on HF.
The higher the number (last minus first), the longer takes the the script to finish. If you just want to update the datamap I suggest not changing the values and searching for the last 500 galleries.

How to use counter.exe:

Just run it.
