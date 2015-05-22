import xbmcplugin
import xbmcgui
import xbmc
import xbmcaddon
import shutil
import xbmcaddon
import xbmcvfs
import os, sys
import time
import urllib
import xml.etree.ElementTree as etree
from xml.dom.minidom import parse
import json
import random
import base64

from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.etree import ElementTree
from xml.dom import minidom
import xml.etree.cElementTree as ET

doDebugLog = False


win = xbmcgui.Window( 10000 )
addon = xbmcaddon.Addon(id='script.titanskin.helpers')
addondir = xbmc.translatePath(addon.getAddonInfo('profile'))

__language__ = xbmc.getLocalizedString
__cwd__ = addon.getAddonInfo('path')

def logMsg(msg, level = 1):
    if doDebugLog == True:
        xbmc.log(msg)

def sendClick(controlId):
    win = xbmcgui.Window( 10000 )
    time.sleep(0.5)
    xbmc.executebuiltin('SendClick('+ controlId +')')

def defaultSettings():
    # skins default settings for artist slideshow
    if xbmc.getCondVisibility("System.HasAddon(script.artistslideshow)"):
        __settings__ = xbmcaddon.Addon(id='script.artistslideshow')
        __settings__.setSetting('transparent', "true")
      
def musicSearch():
    xbmc.executebuiltin( "ActivateWindow(MusicLibrary)" )
    xbmc.executebuiltin( "SendClick(8)" )

def videoSearch():
    xbmc.executebuiltin( "ActivateWindow(VideoLibrary)" )
    xbmc.executebuiltin( "SendClick(8)" )    
    
def showWidget():
    win = xbmcgui.Window( 10000 )
    linkCount = 0
    xbmc.executebuiltin('Control.SetFocus(77777,0)')
    while linkCount !=10 and not xbmc.getCondVisibility("ControlGroup(77777).HasFocus"):
        time.sleep(0.1)
        if not xbmc.getCondVisibility("ControlGroup(77777).HasFocus"):
            xbmc.executebuiltin('Control.SetFocus(77777,0)')
        linkCount += 1
    
def setWidget(containerID):
    win.clearProperty("activewidget")
    win.clearProperty("customwidgetcontent")
    skinStringContent = ""
    customWidget = False
    
    try:
        # workaround for numeric labels (get translated by xbmc)
        skinString = xbmc.getInfoLabel("Container(" + containerID + ").ListItem.Property(submenuVisibility)")
        skinString = skinString.replace("num-","")
        if xbmc.getCondVisibility("Skin.String(widget-" + skinString + ')'):
            skinStringContent = xbmc.getInfoLabel("Skin.String(widget-" + skinString + ')')
        
        # normal method by getting the defaultID
        if skinStringContent == "":
            skinString = xbmc.getInfoLabel("Container(" + containerID + ").ListItem.Property(defaultID)")
            if xbmc.getCondVisibility("Skin.String(widget-" + skinString + ')'):
                skinStringContent = xbmc.getInfoLabel("Skin.String(widget-" + skinString + ')')
           
        if skinStringContent != "":
     
            if "$INFO" in skinStringContent:
                skinStringContent = skinStringContent.replace("$INFO[Window(Home).Property(", "")
                skinStringContent = skinStringContent.replace(")]", "")
                skinStringContent = win.getProperty(skinStringContent)
                customWidget = True
            if "Activate" in skinStringContent:
                skinStringContent = skinStringContent.split(",",1)[1]
                skinStringContent = skinStringContent.replace(",return","")
                skinStringContent = skinStringContent.replace(",Return","")
                skinStringContent = skinStringContent.replace(")","")
                skinStringContent = skinStringContent.replace("\"","")
                customWidget = True
            if ":" in skinStringContent:
                customWidget = True
                
            if customWidget:
                 win.setProperty("customwidgetcontent", skinStringContent)
                 win.setProperty("activewidget","custom")
            else:
                win.clearProperty("customwidgetcontent")
                win.setProperty("activewidget",skinStringContent)

        else:
            win.clearProperty("activewidget")
        
        #also set spotlightwidget for enhancedhomescreen
        if xbmc.getCondVisibility("Skin.String(GadgetRows, enhanced)"):
            setSpotlightWidget(containerID)
    except: pass

def setSpotlightWidget(containerID):
    win.clearProperty("spotlightwidgetcontent")
    skinStringContent = ""
    customWidget = False
    
    # workaround for numeric labels (get translated by xbmc)
    skinString = xbmc.getInfoLabel("Container(" + containerID + ").ListItem.Property(submenuVisibility)")
    skinString = skinString.replace("num-","")
    if xbmc.getCondVisibility("Skin.String(spotlightwidget-" + skinString + ')'):
        skinStringContent = xbmc.getInfoLabel("Skin.String(spotlightwidget-" + skinString + ')')
    
    # normal method by getting the defaultID
    if skinStringContent == "":
        skinString = xbmc.getInfoLabel("Container(" + containerID + ").ListItem.Property(defaultID)")
        if xbmc.getCondVisibility("Skin.String(spotlightwidget-" + skinString + ')'):
            skinStringContent = xbmc.getInfoLabel("Skin.String(spotlightwidget-" + skinString + ')')
       
    if skinStringContent != "":
 
        if "$INFO" in skinStringContent:
            skinStringContent = skinStringContent.replace("$INFO[Window(Home).Property(", "")
            skinStringContent = skinStringContent.replace(")]", "")
            skinStringContent = win.getProperty(skinStringContent)
        if "Activate" in skinStringContent:
            skinStringContent = skinStringContent.split(",",1)[1]
            skinStringContent = skinStringContent.replace(",return","")
            skinStringContent = skinStringContent.replace(")","")
            skinStringContent = skinStringContent.replace("\"","")

        win.setProperty("spotlightwidgetcontent", skinStringContent)

    else:
        win.clearProperty("spotlightwidgetcontent")        

def setSkinVersion():
    skin = xbmc.getSkinDir()
    skinLabel = xbmcaddon.Addon(id=skin).getAddonInfo('name')
    skinVersion = xbmcaddon.Addon(id=skin).getAddonInfo('version')
    win.setProperty("skinTitle",skinLabel + " (v" + skinVersion + ")")
        
def setCustomContent(skinString):
    #legacy
    skinStringContent = xbmc.getInfoLabel("Skin.String(" + skinString + ')')

    if "$INFO" in skinStringContent:
        skinStringContent = skinStringContent.replace("$INFO[Window(Home).Property(", "")
        skinStringContent = skinStringContent.replace(")]", "")
        skinStringContent = win.getProperty(skinStringContent)    

    if "Activate" in skinStringContent:
        skinStringContent = skinStringContent.split(",",1)[1]
        skinStringContent = skinStringContent.replace(",return","")
        skinStringContent = skinStringContent.replace(")","")
        skinStringContent = skinStringContent.replace("\"","")
           
        xbmc.executebuiltin("Skin.SetString(" + skinString + ','+ skinStringContent + ')')         

    win.setProperty("customwidgetcontent", skinStringContent)
        
def updatePlexlinks():
    logMsg("update plexlinks started...")
    xbmc.executebuiltin('RunScript(plugin.video.plexbmc,skin)')
    linkCount = 0
    logMsg("updateplexlinks started...")
    
    #wait for max 20 seconds untill the plex nodes are available
    count = 0
    while (count < 80 and win.getProperty("plexbmc.0.title") == ""):
        xbmc.sleep(250)
        count += 1
    
    #update plex window properties
    while linkCount !=14:
        plexstring = "plexbmc." + str(linkCount)
        link = win.getProperty(plexstring + ".title")
        logMsg(plexstring + ".title --> " + link)
        plexType = win.getProperty(plexstring + ".type")
        logMsg(plexstring + ".type --> " + plexType)            

        link = win.getProperty(plexstring + ".recent")
        logMsg(plexstring + ".recent --> " + link)
        link = link.replace("ActivateWindow(VideoLibrary, ", "")
        link = link.replace("ActivateWindow(VideoLibrary,", "")
        link = link.replace("ActivateWindow(MusicFiles,", "")
        link = link.replace("ActivateWindow(Pictures,", "")
        link = link.replace(",return)", "")
        win.setProperty(plexstring + ".recent.content", link)
        logMsg(plexstring + ".recent --> " + link)

        link = win.getProperty(plexstring + ".viewed")
        logMsg(plexstring + ".viewed --> " + link)
        link = link.replace("ActivateWindow(VideoLibrary, ", "")
        link = link.replace("ActivateWindow(VideoLibrary,", "")
        link = link.replace("ActivateWindow(MusicFiles,", "")
        link = link.replace("ActivateWindow(Pictures,", "")
        link = link.replace(",return)", "")
        win.setProperty(plexstring + ".viewed.content", link)
        logMsg(plexstring + ".viewed --> " + link)

        linkCount += 1
                       
def showInfoPanel():
    tryCount = 0
    secondsToDisplay = "4"
    secondsToDisplay = xbmc.getInfoLabel("Skin.String(ShowInfoAtPlaybackStart)")
    if win.getProperty("VideoScreensaverRunning") != "true":
        while tryCount !=50 and not xbmc.getCondVisibility("Window.IsActive(fullscreeninfo)"):
            time.sleep(0.1)
            if not xbmc.getCondVisibility("Window.IsActive(fullscreeninfo)") and xbmc.getCondVisibility("Player.HasVideo"):
                xbmc.executebuiltin('Action(info)')
            tryCount += 1
        
        # close info again
        time.sleep(int(secondsToDisplay))
        if xbmc.getCondVisibility("Window.IsActive(fullscreeninfo)"):
            xbmc.executebuiltin('Action(info)')

def addShortcutWorkAround():
    xbmc.executebuiltin('SendClick(301)')
    if xbmc.getCondVisibility("System.Platform.Windows"):
        xbmc.sleep(1000)
    else:
        xbmc.sleep(2500)
        if xbmc.getCondVisibility("System.Platform.Linux.RaspberryPi "):
            xbmc.sleep(1000)
    xbmc.executebuiltin('SendClick(401)')

def checkExtraFanArt():
        
    lastPath = None
    
    try:
        efaPath = None
        efaFound = False
        liArt = None
        liPath = xbmc.getInfoLabel("ListItem.Path")
        containerPath = xbmc.getInfoLabel("Container.FolderPath")
        
        if (liPath != None and (xbmc.getCondVisibility("Container.Content(movies) | Container.Content(seasons) | Container.Content(episodes) | Container.Content(tvshows)")) and not "videodb:" in liPath):
                           
            if xbmc.getCondVisibility("Container.Content(episodes)"):
                liArt = xbmc.getInfoLabel("ListItem.Art(tvshow.fanart)")
            
            # do not set extra fanart for virtuals
            if (("plugin://" in liPath) or ("addon://" in liPath) or ("sources" in liPath) or ("plugin://" in containerPath) or ("sources://" in containerPath) or ("plugin://" in containerPath)):
                win.clearProperty("ExtraFanArtPath")
                lastPath = None
            else:

                if xbmcvfs.exists(liPath + "extrafanart/"):
                    efaPath = liPath + "extrafanart/"
                else:
                    pPath = liPath.rpartition("/")[0]
                    pPath = pPath.rpartition("/")[0]
                    if xbmcvfs.exists(pPath + "/extrafanart/"):
                        efaPath = pPath + "/extrafanart/"
                        
                if xbmcvfs.exists(efaPath):
                    dirs, files = xbmcvfs.listdir(efaPath)
                    if files.count > 1:
                        efaFound = True
                        
                if (efaPath != None and efaFound == True):
                    if lastPath != efaPath:
                        win.setProperty("ExtraFanArtPath",efaPath)
                        lastPath = efaPath
                        
                else:
                    win.clearProperty("ExtraFanArtPath")
                    lastPath = None
        else:
            win.clearProperty("ExtraFanArtPath")
            lastPath = None
    
    except:
        xbmc.log("Titan skin helper: error occurred in assigning extra fanart background")
          
def focusEpisode():
    
    totalItems = 0
    curView = xbmc.getInfoLabel("Container.Viewmode") 
    viewId = int(getViewId(curView))
    
    wid = xbmcgui.getCurrentWindowId()
    window = xbmcgui.Window( wid )        
    control = window.getControl(int(viewId))
    totalItems = int(xbmc.getInfoLabel("Container.NumItems"))
    
    #only do a focus if we're on top of the list, else skip to prevent bouncing of the list
    if not int(xbmc.getInfoLabel("Container.Position")) > 1:
        if (xbmc.getCondVisibility("Container.SortDirection(ascending)")):
            curItem = 0
            control.selectItem(0)
            xbmc.sleep(250)
            while ((xbmc.getCondVisibility("Container.Content(episodes) | Container.Content(seasons)")) and totalItems >= curItem):
                if (xbmc.getInfoLabel("Container.ListItem(" + str(curItem) + ").Overlay") != "OverlayWatched.png" and xbmc.getInfoLabel("Container.ListItem(" + str(curItem) + ").Label") != ".." and not xbmc.getInfoLabel("Container.ListItem(" + str(curItem) + ").Label").startswith("*")):
                    if curItem != 0:
                        control.selectItem(curItem)
                    break
                else:
                    curItem += 1
        
        elif (xbmc.getCondVisibility("Container.SortDirection(descending)")):
            curItem = totalItems
            control.selectItem(totalItems)
            xbmc.sleep(250)
            while ((xbmc.getCondVisibility("Container.Content(episodes) | Container.Content(seasons)")) and curItem != 0):
                
                if (xbmc.getInfoLabel("Container.ListItem(" + str(curItem) + ").Overlay") != "OverlayWatched.png"):
                    control.selectItem(curItem-1)
                    break
                else:    
                    curItem -= 1
            
def getViewId(viewString):
    # get all views from views-file
    viewId = None
    skin_view_file = os.path.join(xbmc.translatePath('special://skin/extras'), "views.xml")
    tree = etree.parse(skin_view_file)
    root = tree.getroot()
    for view in root.findall('view'):
        if viewString == __language__(int(view.attrib['languageid'])):
            viewId=view.attrib['value']
    
    return viewId
        
def getImageFromPath(libPath, firstrun):
    
    logMsg("getting images for path " + libPath)
    if "$INFO" in libPath:
        libPath = libPath.replace("$INFO[Window(Home).Property(", "")
        libPath = libPath.replace(")]", "")
        libPath = win.getProperty(libPath)    

    if "Activate" in libPath:
        libPath = libPath.split(",",1)[1]
        libPath = libPath.replace(",return","")
        libPath = libPath.replace(")","")
        libPath = libPath.replace("\"","")
    
    #safety check: does the config directory exist?
    if not xbmcvfs.exists(addondir + os.sep):
        xbmcvfs.mkdir(addondir)
    
    # Blacklist checks
    txtb64 = base64.urlsafe_b64encode(libPath)
    if len(txtb64) > 20:
        txtb64 = txtb64[-20:]
    txtPath = os.path.join(addondir,txtb64 + ".cache")
    
    if win.getProperty(txtPath) == "blacklist":
        logMsg("path blacklisted - skipping for path " + libPath)
        return None
        
    blacklistPath = os.path.join(addondir,"blacklist.cache")
    if (xbmcvfs.exists(blacklistPath) and os.path.getsize(blacklistPath) > 0):
        blfile = open(blacklistPath, 'r')
        if libPath in blfile.read():
            logMsg("path blacklisted - skipping for path " + libPath)
            blfile.close()
            return None
        logMsg("path is NOT blacklisted (or blacklist file error) - continuing for path " + libPath)
        blfile.close()
    
    #no blacklist so read cache and/or path
    images = []
    
    #delete existing cache file if cache expired
    if xbmcvfs.exists(txtPath) and (win.getProperty(txtPath) != "loaded" and not firstrun):
        logMsg("cache file outdated, deleting... " + txtPath)
        xbmcvfs.delete(txtPath)
    
    #cache file exists and cache is not expired, load cache file
    if (xbmcvfs.exists(txtPath) and os.path.getsize(txtPath) > 0) and (win.getProperty(txtPath) == "loaded" or firstrun):
        txtfile = open(txtPath, 'r')
        logMsg("load random image from the cache file... " + libPath)
        image = None
        image = random.choice(list(open(txtPath)))
        if image:
            logMsg("loading done setting image from cache... " + image)
            return image
        else:
            logMsg("cache file empty...skipping...")
    else:
        #no cache file so try to load images from the path
        logMsg("get images from the path or plugin... " + libPath)
        if libPath.startswith("plugin://"):
            media_type = "files"
        else:
            media_type = "video"
        media_array = None
        media_array = getJSON('Files.GetDirectory','{ "properties": ["title","art"], "directory": "' + libPath + '", "media": "' + media_type + '", "limits": {"end":50}, "sort": { "order": "ascending", "method": "random", "ignorearticle": true } }')
        if(media_array != None and media_array.has_key('files')):
            for media in media_array['files']:
                if media.has_key('art'):
                    if media['art'].has_key('fanart'):
                        images.append(media['art']['fanart'])
                    if media['art'].has_key('tvshow.fanart'):
                        images.append(media['art']['tvshow.fanart'])
        else:
            logMsg("media array empty or error so add this path to temporary blacklist..." + libPath)
            if libPath.startswith("videodb://") or libPath.startswith("library://") or libPath.endswith(".xsp") or libPath.startswith("plugin://plugin.video.emby"):
                win.setProperty(txtPath,"blacklist")
                return None
            else:
                blacklistPath = os.path.join(addondir,"blacklist.cache")
                blfile = open(blacklistPath, 'a')
                blfile.write(libPath + '\n')
                blfile.close()
                win.setProperty(txtPath,"blacklist")
                return None
    
    #all is fine, we have some images to randomize and return one
    txtfile = open(txtPath, 'w')
    image = None
    if images != []:
        for image in images:
            txtfile.write(image + '\n')
        random.shuffle(images)
        image = images[0]
        logMsg("setting random image.... " + image)
    else:
        logMsg("image array or cache empty so skipping this path until next restart - " + libPath)
        win.setProperty(txtPath,"loaded")
        txtfile.write('skip')
    
    win.setProperty(txtPath,"loaded")
    txtfile.close()
    return image

def getPicturesBackground(firstrun):

    txtPath = os.path.join(addondir,"pictures.cache")
    
    customPath = xbmc.getInfoLabel("skin.string(CustomPicturesBackgroundPath)")
    oldcustomPath = win.getProperty("CustomPicturesBackgroundPath")
    customPath = xbmc.getInfoLabel("skin.string(CustomPicturesBackgroundPath)")
    if (oldcustomPath != customPath and not firstrun):
        win.clearProperty(txtPath)
        
    win.setProperty("CustomPicturesBackgroundPath",customPath)

    try:
        if (xbmcvfs.exists(txtPath) and os.path.getsize(txtPath) > 0) and (win.getProperty(txtPath) == "loaded" or firstrun):
            #get random image from our global cache file
            image = None
            image = random.choice(list(open(txtPath)))
            if image:
                logMsg("setting random image.... " + image)
            return image 
        else:
            #load the pictures from the custom path or from all picture sources
            txtfile = open(txtPath, 'w')
            images = []
            
            if customPath:
                #load images from custom path
                dirs, files = xbmcvfs.listdir(customPath)
                #pick all images from path
                for file in files:
                    if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".JPG") or file.endswith(".PNG"):
                        image = os.path.join(customPath,file)
                        txtfile.write(image + '\n')
                        images.append(image)
            else:
                #load picture sources
                media_array = getJSON('Files.GetSources','{"media": "pictures"}')
                if(media_array != None and media_array.has_key('sources')):
                    for source in media_array['sources']:
                        if source.has_key('file'):
                            if not "plugin://" in source["file"]:
                                dirs, files = xbmcvfs.listdir(source["file"])
                                if dirs:
                                    #pick 10 random dirs
                                    randomdirs = []
                                    randomdirs.append(os.path.join(source["file"],random.choice(dirs)))
                                    randomdirs.append(os.path.join(source["file"],random.choice(dirs)))
                                    randomdirs.append(os.path.join(source["file"],random.choice(dirs)))
                                    randomdirs.append(os.path.join(source["file"],random.choice(dirs)))
                                    randomdirs.append(os.path.join(source["file"],random.choice(dirs)))
                                    randomdirs.append(os.path.join(source["file"],random.choice(dirs)))
                                    randomdirs.append(os.path.join(source["file"],random.choice(dirs)))
                                    randomdirs.append(os.path.join(source["file"],random.choice(dirs)))
                                    randomdirs.append(os.path.join(source["file"],random.choice(dirs)))
                                    randomdirs.append(os.path.join(source["file"],random.choice(dirs)))
                                    
                                    #pick 5 images from each dir
                                    for dir in randomdirs:
                                        subdirs, files = xbmcvfs.listdir(dir)
                                        count = 0
                                        for file in files:
                                            if ((file.endswith(".jpg") or file.endswith(".png") or file.endswith(".JPG") or file.endswith(".PNG")) and count < 5):
                                                image = os.path.join(dir,file)
                                                txtfile.write(image + '\n')
                                                images.append(image)
                                                count += 1
                                if files:
                                    #pick 10 images from root
                                    count = 0
                                    for file in files:
                                        if ((file.endswith(".jpg") or file.endswith(".png") or file.endswith(".JPG") or file.endswith(".PNG")) and count < 10):
                                            image = os.path.join(source["file"],file)
                                            txtfile.write(image + '\n')
                                            images.append(image)
                                            count += 1
                                
            txtfile.close()
            if images != []:
                random.shuffle(images)
                image = images[0]
                logMsg("setting random image.... " + image)
                return image
            else:
                logMsg("image sources array or cache empty so skipping this path until next restart - " + libPath)
                return None
    #if something fails, return None
    except:
        logMsg("exception occured in getPicturesBackground.... ")
        return None            
        

def getGlobalBackground(firstrun):
    
    #just get all images from all cache files and just pick a random image
    if xbmcvfs.exists(addondir + os.sep):
        
        txtPath = os.path.join(addondir,"global.cache")
        
        if (xbmcvfs.exists(txtPath) and os.path.getsize(txtPath) > 0) and (win.getProperty(txtPath) == "loaded" or firstrun):
            #get random image from our global cache file
            image = None
            image = random.choice(list(open(txtPath)))        
            return image 
        else:    
            #at first run we create the global cache file
            if firstrun:
                xbmcvfs.delete(txtPath)
                global_txtfile = open(txtPath, 'w')
                dirs, files = xbmcvfs.listdir(addondir)
                images = []
                for file in files:
                    if file.endswith(".cache"):
                        txtfile = open(os.path.join(addondir,file), 'r')
                        for line in txtfile.readlines():
                            if not "skip" in line:
                                images.append(line)
                                global_txtfile.write(line)
                        txtfile.close()
                global_txtfile.close()
                if images != []:
                    random.shuffle(images)
                    image = images[0]
                    return image
                else:
                    return None

    
def UpdateBackgrounds(firstrun=False):
    
    #get all movies  
    win.setProperty("AllMoviesBackground",getImageFromPath("videodb://movies/titles/",firstrun))
    
    #get all tvshows  
    win.setProperty("AllTvShowsBackground",getImageFromPath("videodb://tvshows/titles/",firstrun))
    
    #get all musicvideos  
    win.setProperty("AllMusicVideosBackground",getImageFromPath("videodb://musicvideos/titles/",firstrun))
    
    #get all music  
    win.setProperty("AllMusicBackground",getImageFromPath("musicdb://artists/",firstrun))
    
    #get global fanart background 
    win.setProperty("GlobalFanartBackground",getGlobalBackground(firstrun))
    
    #get in progress movies  
    win.setProperty("InProgressMovieBackground",getImageFromPath("special://skin/extras/widgetplaylists/inprogressmovies.xsp",firstrun))

    #get recent and unwatched movies
    win.setProperty("RecentMovieBackground",getImageFromPath("videodb://recentlyaddedmovies/",firstrun))
    
    #unwatched movies
    win.setProperty("UnwatchedMovieBackground",getImageFromPath("special://skin/extras/widgetplaylists/unwatchedmovies.xsp",firstrun))
  
    #get in progress tvshows
    win.setProperty("InProgressShowsBackground",getImageFromPath("library://video/inprogressshows.xml",firstrun))

    #get recent episodes
    win.setProperty("RecentEpisodesBackground",getImageFromPath("videodb://recentlyaddedepisodes/",firstrun))

    #smart shortcuts --> emby nodes
    if xbmc.getCondVisibility("Skin.HasSetting(SmartShortcuts.emby)"):
        
        #wait for max 20 seconds untill the emby nodes are available
        count = 0
        while (count < 80 and win.getProperty("Emby.nodes.total") == ""):
            xbmc.sleep(250)
            count += 1
        
        embyProperty = win.getProperty("Emby.nodes.total")
        contentStrings = ["", ".recent", ".inprogress", ".unwatched", ".recentepisodes", ".inprogressepisodes", ".nextepisodes"]
        if embyProperty:
            totalNodes = int(embyProperty)
            for i in range(totalNodes):
                for contentString in contentStrings:
                    path = win.getProperty("Emby.nodes.%s%s.content"%(str(i),contentString))
                    if path:
                        image = getImageFromPath(path,firstrun)
                        if image:
                            win.setProperty("Emby.nodes.%s%s.image"%(str(i),contentString),image)
        
    #smart shortcuts --> playlists
    if xbmc.getCondVisibility("Skin.HasSetting(SmartShortcuts.playlists)"):
        try:
            playlistCount = 0
            path = "special://profile/playlists/video/"
            if xbmcvfs.exists( path ):
                dirs, files = xbmcvfs.listdir(path)
                for file in files:
                    if file.endswith(".xsp"):
                        playlist = path + file
                        label = file.replace(".xsp","")
                        image = getImageFromPath(playlist,firstrun)
                        if image != None:
                            playlist = "ActivateWindow(Videos," + playlist + ",return)"
                            win.setProperty("playlist." + str(playlistCount) + ".image", image)
                            win.setProperty("playlist." + str(playlistCount) + ".label", label)
                            win.setProperty("playlist." + str(playlistCount) + ".action", playlist)
                            playlistCount += 1
        except:
            #something wrong so disable the smartshortcuts for this section for now
            xbmc.executebuiltin("Skin.Reset(SmartShortcuts.playlists)")
    
    #smart shortcuts --> favorites
    if xbmc.getCondVisibility("Skin.HasSetting(SmartShortcuts.favorites)"):
        try:
            favoritesCount = 0
            fav_file = xbmc.translatePath( 'special://profile/favourites.xml' ).decode("utf-8")
            if xbmcvfs.exists( fav_file ):
                doc = parse( fav_file )
                listing = doc.documentElement.getElementsByTagName( 'favourite' )
                
                for count, favourite in enumerate(listing):
                    name = favourite.attributes[ 'name' ].nodeValue
                    path = favourite.childNodes [ 0 ].nodeValue
                    if (path.startswith("ActivateWindow(Videos") or path.startswith("ActivateWindow(10025") or path.startswith("ActivateWindow(videos") or path.startswith("ActivateWindow(Music") or path.startswith("ActivateWindow(10502")) and not "script://" in path:
                        image = getImageFromPath(path,firstrun)
                        if image != None:
                            win.setProperty("favorite." + str(favoritesCount) + ".image", image)
                            win.setProperty("favorite." + str(favoritesCount) + ".label", name)
                            win.setProperty("favorite." + str(favoritesCount) + ".action", path)
                            favoritesCount += 1
        except:
            #something wrong so disable the smartshortcuts for this section for now
            xbmc.executebuiltin("Skin.Reset(SmartShortcuts.favorites)")    
    
    #get plex nodes
    if xbmc.getCondVisibility("System.HasAddon(plugin.video.plexbmc)"):
        
        if firstrun:
            updatePlexlinks()
        
        totalNodes = 14
        for i in range(totalNodes):
            if win.getProperty("plexbmc.%s.title" %str(i)):
                plexcontent = win.getProperty("plexbmc.%s.content" %str(i))
                plextype = win.getProperty("plexbmc.%s.type" %str(i))
                image = getImageFromPath(plexcontent,firstrun)
                if image:
                    win.setProperty("plexbmc.%s.background" %str(i),image)
                    if plextype == "movie":
                        win.setProperty("plexfanartbg", image)

    #get pictures background
    win.setProperty("PicturesBackground", getPicturesBackground(firstrun))

def getJSON(method,params):
    json_response = xbmc.executeJSONRPC('{ "jsonrpc" : "2.0" , "method" : "' + method + '" , "params" : ' + params + ' , "id":1 }')

    jsonobject = json.loads(json_response.decode('utf-8','replace'))
   
    if(jsonobject.has_key('result')):
        return jsonobject['result']
    else:
        xbmc.log("no result " + str(jsonobject),xbmc.LOGDEBUG)
        return None


def setMovieSetDetails():
    #get movie set details -- thanks to phil65 - used this idea from his skin info script
    dbId = xbmc.getInfoLabel("ListItem.DBID")
    
    win.clearProperty('MovieSet.Title')
    win.clearProperty('MovieSet.Runtime')
    win.clearProperty('MovieSet.Writer')
    win.clearProperty('MovieSet.Director')
    win.clearProperty('MovieSet.Genre')
    win.clearProperty('MovieSet.Country')
    win.clearProperty('MovieSet.Studio')
    win.clearProperty('MovieSet.Years')
    win.clearProperty('MovieSet.Year')
    win.clearProperty('MovieSet.Count')
    win.clearProperty('MovieSet.Plot')
            
    if dbId != "":
        json_response = getJSON('VideoLibrary.GetMovieSetDetails', '{"setid": %s, "properties": [ "thumbnail" ], "movies": { "properties":  [ "rating", "art", "file", "year", "director", "writer","genre" , "thumbnail", "runtime", "studio", "plotoutline", "plot", "country", "streamdetails"], "sort": { "order": "ascending",  "method": "year" }} }' % dbId)
        #clear_properties()
        if ("setdetails" in json_response):
            
            count = 1
            runtime = 0
            writer = []
            director = []
            genre = []
            country = []
            studio = []
            years = []
            plot = ""
            title_list = ""
            title_header = "[B]" + str(json_response['setdetails']['limits']['total']) + " " + xbmc.getLocalizedString(20342) + "[/B][CR]"
            set_fanart = []
            for item in json_response['setdetails']['movies']:
                art = item['art']
                set_fanart.append(art.get('fanart', ''))
                title_list += "[I]" + item['label'] + " (" + str(item['year']) + ")[/I][CR]"
                if item['plotoutline']:
                    plot += "[B]" + item['label'] + " (" + str(item['year']) + ")[/B][CR]" + item['plotoutline'] + "[CR][CR]"
                else:
                    plot += "[B]" + item['label'] + " (" + str(item['year']) + ")[/B][CR]" + item['plot'] + "[CR][CR]"
                runtime += item['runtime']
                count += 1
                if item.get("writer"):
                    writer += [w for w in item["writer"] if w and w not in writer]
                if item.get("director"):
                    director += [d for d in item["director"] if d and d not in director]
                if item.get("genre"):
                    genre += [g for g in item["genre"] if g and g not in genre]
                if item.get("country"):
                    country += [c for c in item["country"] if c and c not in country]
                if item.get("studio"):
                    studio += [s for s in item["studio"] if s and s not in studio]
                years.append(str(item['year']))
            win.setProperty('MovieSet.Plot', plot)
            if json_response['setdetails']['limits']['total'] > 1:
                win.setProperty('MovieSet.ExtendedPlot', title_header + title_list + "[CR]" + plot)
            else:
                win.setProperty('MovieSet.ExtendedPlot', plot)
            win.setProperty('MovieSet.Title', title_list)
            win.setProperty('MovieSet.Runtime', str(runtime / 60))
            win.setProperty('MovieSet.Writer', " / ".join(writer))
            win.setProperty('MovieSet.Director', " / ".join(director))
            win.setProperty('MovieSet.Genre', " / ".join(genre))
            win.setProperty('MovieSet.Country', " / ".join(country))
            win.setProperty('MovieSet.Studio', " / ".join(studio))
            win.setProperty('MovieSet.Years', " / ".join(years))
            win.setProperty('MovieSet.Year', years[0] + " - " + years[-1])
            win.setProperty('MovieSet.Count', str(json_response['setdetails']['limits']['total']))
            
            count = 40
            while dbId == xbmc.getInfoLabel("ListItem.DBID") and set_fanart != []:
                #rotate fanart from movies in set while listitem is in focus
                if count == 40:
                    random.shuffle(set_fanart)
                    win.setProperty('ExtraFanArtPath', set_fanart[0])
                    count = 0
                else:
                    count += 1
                xbmc.sleep(125)
            
def setView(containerType,viewId):

    if viewId=="00":
        curView = xbmc.getInfoLabel("Container.Viewmode")
        viewId = getViewId(curView)
        
    else:
        viewId=viewId    

    if xbmc.getCondVisibility("System.HasAddon(plugin.video.netflixbmc)"):
        __settings__ = xbmcaddon.Addon(id='plugin.video.netflixbmc')

        if containerType=="MOVIES":
            __settings__.setSetting('viewIdVideos', viewId)
        elif containerType=="SERIES":
            __settings__.setSetting('viewIdEpisodesNew', viewId)
        elif containerType=="SEASONS":
            __settings__.setSetting('viewIdEpisodesNew', viewId)
        elif containerType=="EPISODES":
            __settings__.setSetting('viewIdEpisodesNew', viewId)
        else:
            __settings__.setSetting('viewIdActivity', viewId)
            
    if xbmc.getCondVisibility("System.HasAddon(plugin.video.xbmb3c)"):
        __settings__ = xbmcaddon.Addon(id='plugin.video.xbmb3c')
        if __settings__.getSetting(xbmc.getSkinDir()+ '_VIEW_' + containerType) != "disabled":
            __settings__.setSetting(xbmc.getSkinDir()+ '_VIEW_' + containerType, viewId)

def checkNotifications(notificationType):
    
    if notificationType == "weather":
        winw = xbmcgui.Window(12600)
        if (winw.getProperty("Alerts.RSS") != "" and winw.getProperty("Current.Condition") != ""):
            dialog = xbmcgui.Dialog()
            dialog.notification(xbmc.getLocalizedString(31294), winw.getProperty("Alerts"), xbmcgui.NOTIFICATION_WARNING, 8000)
    
    if notificationType == "nextaired":
        if (win.getProperty("NextAired.TodayShow") != ""):
            dialog = xbmcgui.Dialog()
            dialog.notification(xbmc.getLocalizedString(31295), win.getProperty("NextAired.TodayShow"), xbmcgui.NOTIFICATION_WARNING, 8000)    
            
            
def showSubmenu(showOrHide,doFocus):

    submenuTitle = xbmc.getInfoLabel("Container(300).ListItem.Label")
    submenu = win.getProperty("submenutype")
    submenuloading = ""
    if xbmc.getCondVisibility("Skin.HasSetting(AutoShowSubmenu)"):
        submenuloading = win.getProperty("submenuloading")

    # SHOW SUBMENU    
    if showOrHide == "SHOW":
        if submenuloading != "loading":
            if submenu != "":
                win.setProperty("submenu", "show")
                if doFocus != None:
                    win.setProperty("submenuTitle", submenuTitle)
                    xbmc.executebuiltin('Control.SetFocus('+ doFocus +',0)')
                    time.sleep(0.2)
                    xbmc.executebuiltin('Control.SetFocus('+ doFocus +',0)')
            else:
                win.setProperty("submenu", "hide")
        else:
            win.setProperty("submenuloading", "")

    #HIDE SUBMENU
    elif showOrHide == "HIDE":
        win.setProperty("submenuloading", "loading")
        win.setProperty("submenu", "hide")
        if doFocus != None:
            win.setProperty("submenu", "show")
            xbmc.executebuiltin('Control.SetFocus('+ doFocus +',0)')
            time.sleep(0.5)
            xbmc.executebuiltin('Control.SetFocus('+ doFocus +',0)')
            win.setProperty("submenuloading", "loading")
            win.setProperty("submenu", "hide")
            
def getFavourites():
    try:
        xbmcplugin.setContent(int(sys.argv[1]), 'files')
        favoritesCount = 0
        fav_file = xbmc.translatePath( 'special://profile/favourites.xml' ).decode("utf-8")
        if xbmcvfs.exists( fav_file ):
            doc = parse( fav_file )
            listing = doc.documentElement.getElementsByTagName( 'favourite' )
            
            for count, favourite in enumerate(listing):
                label = ""
                image = "special://skin/extras/hometiles/favourites.png"
                for (name, value) in favourite.attributes.items():
                    if name == "name":
                        label = value
                    if name == "thumb":
                        image = value
                path = favourite.childNodes [ 0 ].nodeValue
                
                path="plugin://script.titanskin.helpers?LAUNCHAPP&&&" + path
                li = xbmcgui.ListItem(label, path=path)
                li.setThumbnailImage(image)
                li.setProperty('IsPlayable', 'false')
                
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=path, listitem=li, isFolder=False)
    except: pass        
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
    
def selectView():
    import Dialogs as dialogs
    
    #get current content type
    contenttype = "other"
    if xbmc.getCondVisibility("Container.Content(episodes)"):
        contenttype = "episodes"
    elif xbmc.getCondVisibility("Container.Content(movies)"):
        contenttype = "movies"
    elif xbmc.getCondVisibility("Container.Content(sets)"):
        contenttype = "sets"
    elif xbmc.getCondVisibility("Container.Content(tvshows)"):
        contenttype = "tvshows"
    elif xbmc.getCondVisibility("Container.Content(seasons)"):
        contenttype = "seasons"
    elif xbmc.getCondVisibility("Container.Content(musicvideos)"):
        contenttype = "musicvideos"
    
    allViews = []
    views_file = xbmc.translatePath( 'special://skin/extras/views.xml' ).decode("utf-8")
    if xbmcvfs.exists( views_file ):
        doc = parse( views_file )
        listing = doc.documentElement.getElementsByTagName( 'view' )
        for count, view in enumerate(listing):
            label = __language__(int(view.attributes[ 'languageid' ].nodeValue))
            id = view.attributes[ 'value' ].nodeValue
            type = view.attributes[ 'type' ].nodeValue
            if type == "all" or contenttype in type:
                image = "special://skin/extras/viewthumbs/%s.jpg" %id
                listitem = xbmcgui.ListItem(label=label, iconImage=image)
                listitem.setProperty("id",id)
                listitem.setProperty("icon",image)
                allViews.append(listitem)
    w = dialogs.DialogSelect( "DialogSelect.xml", __cwd__, listing=allViews, windowtitle="select view",multiselect=True )
    w.doModal()
    selectedItem = w.result
    if selectedItem:
        label = allViews[selectedItem].getLabel()
        id = allViews[selectedItem].getProperty("id")
        xbmc.executebuiltin("Container.SetViewMode(%s)" %id)
    del w