import xbmcplugin
import xbmcgui
import shutil
import xbmcaddon
import os

def setHomeItems(idToChange, moveDirection):

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


def setView(viewId, containerType):
    __settings__ = xbmcaddon.Addon(id='plugin.video.xbmb3c')
    
    
    __settings__.setSetting(xbmc.getSkinDir()+ '_VIEW_' + viewId, containerType)
    xbmc.executebuiltin("Container.Refresh")     

def restoreHomeItems():
    
    currentVersion = xbmc.getInfoLabel("System.AddonVersion(skin.titan)")
    previousVersion = xbmc.getInfoLabel("Skin.String(LastKnownVersion)")
    
    print('[Titanskin] currentVersion: ' + currentVersion)
    print('[Titanskin] previousVersion: ' + previousVersion)
    
    if currentVersion != previousVersion:
    
        fileName = str(xbmc.translatePath("special://skin/1080i/")) + "IncludesHomeMenuItems.xml"
    
        backuppath = str(xbmc.translatePath("special://userdata/addon_data/skin.titan"))
        if not os.path.exists(backuppath):
            os.makedirs(backuppath)
        fileName_backup =  backuppath + "/IncludesHomeMenuItems.xml"
        fileNameDef = backuppath + "/IncludesHomeMenuItems_default.xml"
    
        if os.path.isfile(fileName):
            shutil.copy(fileName, fileNameDef)
    
        if os.path.isfile(fileName_backup):
            shutil.copy(fileName_backup, fileName)
            print('[Titanskin] backup of home items is restored!')
    
        xbmc.executebuiltin('Skin.SetString(LastKnownVersion,' + currentVersion + ')')
        xbmc.executebuiltin('xbmc.ReloadSkin')
    
    else:
        print('[Titanskin] no action needed')
    
    
    # always set focus to panel 300
    xbmc.executebuiltin('SetFocus(300)')
    
#script init
action = ""
argument1 = ""
argument2 = ""

# get arguments
try:
    action = str(sys.argv[1])
except: 
    pass

try:
    argument1 = str(sys.argv[2])
except: 
    pass
   
try:
    argument2 = str(sys.argv[3])
except: 
    pass    

# select action
if action == "SETHOMEITEMS":
    setHomeItems(int(argument1), argument2)
elif action == "SETVIEW":
    setView(argument1, argument2)
elif action == "RESTORE":
    restoreHomeItems()
else:
    xbmc.executebuiltin("Notification(Titan Mediabrowser,you can not run this script directly)") 