# na_scratch_paper
A tool that gives the ability to make simple to fairly complex Qt PySide2 UIs in a short period for those small 
convenience functions we all write during the course of the day but never get around to making UIs for.
###
###

Created by Noah Alzayer

www.NoahAlzayer.net

[scratchpaper@noahalzayer.net](mailto:scratchpaper@noahalzayer.net)

This tool was made testing in Maya 2019 and 2018 in both 1080 and 4K resolutions. If any issues crop up with use in 
other versions of Maya or different resolutions, let me know.

In case the license doesn't fully indicate, there are no strings attached for use, though it would just be kinda be cool if users 
let me know of any cool unconventional uses they might find or little edits that might worth rolling in to the tool for others.

If there's an input widget you'd like to be added, just let me know via email or raise an issue in the Github.

##
### Installation:
##### Maya
1) Drag maya_install.py in to the viewport in Maya
2) Fill out Shelf Button Preferences
3) Click to Open The Tool

###

What maya_install.py Does:

It simply copies over the script files to the Maya internalVar user script directory and the images to the icons directory.
It then brings up a dialog to auto-add a shelf button to call the tool with na_scratch_paper.run_maya()

##### Others

For Vanilla Python or other programs with PySide2, add the files in the scripts directory to a directory in the Python Path

If you do use this in other programs and would like me to add a run command for it, just let me know and I can try to add it.

#
### Use:
For instructions on setting up UIs and general use, consult the [Wiki](https://github.com/noahalzayer/na_scratch_paper/wiki)