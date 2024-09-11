import xbmc
import xbmcaddon
addon = xbmcaddon.Addon()
addon1 = xbmcaddon.Addon().getSettings()
addon2 = xbmcaddon.Addon('service.test.getsettings').getSettings()
addon3 = addon.getSettings()
xbmc.log("ID addon: %s", id(addon))
xbmc.log("ID addon1: %s", id(addon1))
xbmc.log("ID addon2: %s", id(addon2))
xbmc.log("ID addon3: %s", id(addon3))

def print_settings():
    xbmc.log("Creating new instance", xbmc.LOGWARNING)
    current_addon = xbmcaddon.Addon().getSettings()
    xbmc.log("ID current addon: %s", id(current_addon))
    addon3 = addon.getSettings()
    xbmc.log("ID addon3: %s", id(addon3))
    xbmc.sleep(1000)
    xbmc.log("Setting addon1 = {}".format(addon1.getBool('Setting1')), xbmc.LOGWARNING)
    xbmc.sleep(1000)
    xbmc.log("Setting addon2 = {}".format(addon2.getBool('Setting1')), xbmc.LOGWARNING)
    xbmc.sleep(1000)
    xbmc.log("Setting addon3 = {}".format(addon3.getBool('Setting1')), xbmc.LOGWARNING)
    xbmc.sleep(1000)
    xbmc.log("Setting new addon = {}".format(current_addon.getBool('Setting1')), xbmc.LOGWARNING)
    xbmc.sleep(2000)


def run():
    monitor = xbmc.Monitor()
    state = True
    while not monitor.abortRequested():
        print_settings()
        state = not state
        addon.getSettings().setBool("Setting1", state)
        monitor.waitForAbort(10)


if __name__ == '__main__':
    run()

