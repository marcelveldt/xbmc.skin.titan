import xbmcplugin
import xbmcgui
import xbmcaddon


__settings__ = xbmcaddon.Addon(id='plugin.video.xbmb3c')


__settings__.setSetting(xbmc.getSkinDir()+ '_VIEW_' + str(sys.argv[1]),str(sys.argv[2]))
xbmc.executebuiltin("Container.Refresh") 