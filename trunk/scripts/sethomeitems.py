import xbmcplugin
import xbmcgui


idToChange = int(sys.argv[1])
moveDirection = str(sys.argv[2])

#try:
    #import xml.etree.cElementTree as ET
#except ImportError:
    #import xml.etree.ElementTree as ET

currentLabel = None
currentIcon = None
currentThumb = None
currentOnClick = None
currentVisible = None

newLabel = None
newIcon = None
newThumb = None
newOnClick = None
newVisible = None


fileName = ""
fileName = str(xbmc.translatePath("special://skin/1080i/")) + "IncludesHomeMenuItems.xml"

backuppath = str(xbmc.translatePath("special://userdata/addon_data/skin.titan"))
if not os.path.exists(backuppath):
    os.makedirs(backuppath)
fileName_backup =  backuppath + "/IncludesHomeMenuItems.xml"

import xml.etree.ElementTree as ET
tree = ET.parse(fileName)
root = tree.getroot()

newId = None

if (moveDirection == "DOWN"):
    newId = idToChange - 1
else:
    newId = idToChange + 1
    
include = root.find("include")

# first we get current values
for item in include:
    if (item.get("id") == str(newId)):
        currentLabel = item.find("label").text
        currentIcon = item.find("icon").text
        currentThumb = item.find("thumb").text
        currentOnClick = item.find("onclick").text
        currentVisible = item.find("visible").text
    if (item.get("id") == str(idToChange)):
        newLabel = item.find("label").text
        newIcon = item.find("icon").text
        newThumb = item.find("thumb").text
        newOnClick = item.find("onclick").text   
        newVisible = item.find("visible").text

# now we set new values
for item in include:
    if (item.get("id") == str(newId)):
        item.find("label").text = newLabel
        item.find("icon").text = newIcon
        item.find("thumb").text = newThumb
        item.find("onclick").text = newOnClick
        item.find("visible").text = newVisible
    if (item.get("id") == str(idToChange)):
        item.find("label").text = currentLabel
        item.find("icon").text = currentIcon
        item.find("thumb").text = currentThumb
        item.find("onclick").text = currentOnClick
        item.find("visible").text = currentVisible
        

tree.write(fileName)
tree.write(fileName_backup)

win = xbmcgui.Window(xbmcgui.getCurrentWindowId())

curpos = int(win.getProperty("CurrentPos"))
if (moveDirection == "DOWN"):
    curpos = curpos - 1
else:
    curpos = curpos + 1

xbmc.executebuiltin('xbmc.ReloadSkin')
xbmc.executebuiltin('Control.SetFocus(100,4)')
xbmc.executebuiltin('Control.SetFocus(4008,' + str(curpos) + ')')
