# -*- coding: utf-8 -*-
from os.path import exists

from Screens.Setup import Setup
from Components.config import config, ConfigSubsection, ConfigSelection
from Plugins.Plugin import PluginDescriptor

from . import _

modelist = [("1", _("Off")), ("2", _("On")), ("3", _("Auto"))]

config.plugins.FanSetup = ConfigSubsection()
config.plugins.FanSetup.mode = ConfigSelection(choices=modelist, default="3")


class FanSetupScreen(Setup):
	def __init__(self, session):
		Setup.__init__(self, session, "fansetup", plugin="SystemPlugins/VentonFancontrol", PluginLanguageDomain="VentonFancontrol")
		self.onClose.append(self.__onClose)

	def __onClose(self):
		applySettings(int(config.plugins.FanSetup.mode.value))

	def changedEntry(self):
		self.setPreviewSettings()
		Setup.changedEntry(self)

	def setPreviewSettings(self):
		if self["config"].getCurrent():
			applySettings(int(self["config"].getCurrent()[1].value))


def applySettings(mode):
	setMode = ""
	if mode == 1:
		setMode = "1"

	elif mode == 2:
		setMode = "2"

	else:
		setMode = "3"

	try:
		with open("/proc/stb/fp/fan", "w") as file:
			file.write(setMode)
	except OSError:
		return


def setConfiguredSettings():
	applySettings(int(config.plugins.FanSetup.mode.value))


def main(session, **kwargs):
	session.open(FanSetupScreen)


def startup(reason, **kwargs):
	setConfiguredSettings()


def FanMain(session, **kwargs):
	session.open(FanSetupScreen)


def FanSetup(menuid, **kwargs):
	if menuid == "system":
		return [(_("FAN Control"), FanMain, "fan_control", None)]
	else:
		return []


def Plugins(**kwargs):
	if exists("/proc/stb/fp/fan"):
		return [PluginDescriptor(name=_("Fan Control"), description=_("switch Fan On/Off"), where=PluginDescriptor.WHERE_MENU, fnc=FanSetup),
					PluginDescriptor(name="Fan Control", description="", where=PluginDescriptor.WHERE_SESSIONSTART, fnc=startup)]
	return []
