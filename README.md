# Subst
## Change long path into a drive letter
#### This is a simple program to substitute long folder paths (>255)  into an external drive letter, 

## Install
### Windows x64 
Download dist folder and run subst.exe.
Or you can build it using py2exe for setup.

```
python setup.py py2exe
```

if you like to run it from Python just run.
```
python main.py
```

This is a free program use as you wish (AS IS no liability ), All images copyrighted to owners.

## What is this
this a gui for subst command in windows, the program looks for unused letters and asks for required path . Just 
click on "Replace path" and get and new folder, press "Delete Letter" to unlink the letter.


when closing the program it will ask if you want to disconnect the letter. If "No" is selected windows will keep 
the letter for later, but to disconnect it later it must be manually done
```
subst x: /d
``` 
where x: is your drive letter, press on help icon to show this message.
