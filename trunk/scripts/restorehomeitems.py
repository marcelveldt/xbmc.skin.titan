import xbmcplugin
import xbmcgui
import shutil

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
