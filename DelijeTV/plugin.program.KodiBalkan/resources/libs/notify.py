############################################################################
#				            $$ $										   #
#				       $$$$$$$$$$										   #
#				  $ $$$$ $      $ 									       #
#				$$$$$            $$										   #
#				 $               $										   #
#				  $              $$										   #
#				  $$              $										   #
#				   $     $ $$$$$    $									   #
#				    $$$$$   $  $   $								       #
#				    $   $   $  $    $									   #
#				    $ $ $$   $$     $$$									   #
#				     $$$$ $$$       $$$									   #
#				      $ $$        $$$  $							       #
#				       $$      $$$$ $ $$$$$ $							   #
#				       $$   $$$$$$$ $$$   $$$$$$$						   #
#				        $$$$     $$$$$$$      $$$$$$					   #
#				                   $$$$$$$  $$$$$$  $$					   #
#				                  $$$$$ $$$$        $					   #
#				                   $$$    $      $$  $					   #
#				                   $$$   $$      $  $					   #
#				                      $   $$     $$ $ 					   #
#				                     $   $$    $  $						   #
#				                     $$   $ $  $  $						   #
#				                   $    $ $  $   $$						   #
#				                   $ $   $$$$$  $$$$$					   #
#				                     $$$$$$$$$$$$$$$					   #
#				                     $$$ $$$$$$$$$$$$					   #
#				                    $$$$$$$$ $ $$$$$					   #
#				                  $$$$$$$$$$ $$ $$$$$$					   #
#				                  $$$$$$$$$$$							   #
############################################################################

import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys, xbmcvfs, glob
import shutil
import urllib2,urllib
import re
import uservar
import time
from resources.libs import yt, wizard as wiz
from datetime import date, datetime, timedelta

ADDON_ID       = uservar.ADDON_ID
ADDON          = wiz.addonId(ADDON_ID)
VERSION        = wiz.addonInfo(ADDON_ID,'version')
ADDONPATH      = wiz.addonInfo(ADDON_ID,'path')
ADDONTITLE     = uservar.ADDONTITLE
BUILDERNAME    = uservar.BUILDERNAME
DIALOG         = xbmcgui.Dialog()
DP             = xbmcgui.DialogProgress()
HOME           = xbmc.translatePath('special://home/')
ADDONS         = os.path.join(HOME,     'addons')
USERDATA       = os.path.join(HOME,     'userdata')
PLUGIN         = os.path.join(ADDONS,   ADDON_ID)
PACKAGES       = os.path.join(ADDONS,   'packages')
ADDONDATA      = os.path.join(USERDATA, 'addon_data', ADDON_ID)
FANART         = os.path.join(ADDONPATH,   'fanart.jpg')
ICON           = os.path.join(ADDONPATH,   'icon.png')
ART            = os.path.join(ADDONPATH,   'resources', 'art')
SKINFOLD       = os.path.join(ADDONPATH,   'resources', 'skins', 'DefaultSkin', 'media')
ADVANCED       = os.path.join(USERDATA,  'advancedsettings.xml')
NOTIFY         = wiz.getS('notify')
NOTEID         = wiz.getS('noteid')
NOTEDISMISS    = wiz.getS('notedismiss')
BUILDNAME      = wiz.getS('buildname')
BUILDVERSION   = wiz.getS('buildversion')
LATESTVERSION  = wiz.checkBuild(BUILDNAME, 'version')
TODAY          = date.today()
KODIV          = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
TOMORROW       = TODAY + timedelta(days=1)
THREEDAYS      = TODAY + timedelta(days=3)
UPDATECHECK    = uservar.UPDATECHECK if str(uservar.UPDATECHECK).isdigit() else 1
NEXTCHECK      = TODAY + timedelta(days=UPDATECHECK)
NOTIFICATION   = uservar.NOTIFICATION
ENABLE         = uservar.ENABLE
HEADERTYPE     = uservar.HEADERTYPE if uservar.HEADERTYPE == 'Image' else 'Text'
HEADERMESSAGE  = uservar.HEADERMESSAGE
BACKGROUND     = uservar.BACKGROUND
HEADERIMAGE    = uservar.HEADERIMAGE
THEME1         = uservar.THEME1
THEME2         = uservar.THEME2
THEME3         = uservar.THEME3
THEME4         = uservar.THEME4
THEME5         = uservar.THEME5
COLOR1         = uservar.COLOR1
COLOR2         = uservar.COLOR2
COLOR3         = uservar.COLOR3
COLOR4         = uservar.COLOR4
COLOR5         = uservar.COLOR5
CONTACTICON    = uservar.CONTACTICON if not uservar.CONTACTICON == 'http://' else ICON 
CONTACTFANART  = uservar.CONTACTFANART if not uservar.CONTACTFANART == 'http://' else FANART

if BACKGROUND == '': BACKGROUND = FANART
elif not wiz.workingURL(BACKGROUND): BACKGROUND = FANART

ACTION_PREVIOUS_MENU 			=  10	## ESC action
ACTION_NAV_BACK 				=  92	## Backspace action
ACTION_MOVE_LEFT				=   1	## Left arrow key
ACTION_MOVE_RIGHT 				=   2	## Right arrow key
ACTION_MOVE_UP 					=   3	## Up arrow key
ACTION_MOVE_DOWN 				=   4	## Down arrow key
ACTION_MOUSE_WHEEL_UP 			= 104	## Mouse wheel up
ACTION_MOUSE_WHEEL_DOWN			= 105	## Mouse wheel down
ACTION_MOVE_MOUSE 				= 107	## Down arrow key
ACTION_SELECT_ITEM				=   7	## Number Pad Enter
ACTION_BACKSPACE				= 110	## ?
ACTION_MOUSE_LEFT_CLICK 		= 100
ACTION_MOUSE_LONG_CLICK 		= 108

def artwork(file):
	if   file == 'button': return os.path.join(SKINFOLD, 'Button', 'button-focus_lightblue.png'), os.path.join(SKINFOLD, 'Button', 'button-focus_grey.png')
	elif file == 'radio' : return os.path.join(SKINFOLD, 'RadioButton', 'MenuItemFO.png'), os.path.join(SKINFOLD, 'RadioButton', 'MenuItemNF.png'), os.path.join(SKINFOLD, 'RadioButton', 'radiobutton-focus.png'), os.path.join(SKINFOLD, 'RadioButton', 'radiobutton-nofocus.png')
	elif file == 'slider': return os.path.join(SKINFOLD, 'Slider', 'osd_slider_nib.png'), os.path.join(SKINFOLD, 'Slider', 'osd_slider_nibNF.png'), os.path.join(SKINFOLD, 'Slider', 'slider1.png'), os.path.join(SKINFOLD, 'Slider', 'slider1.png')

def autoConfig(msg='', TxtColor='0xFFFFFFFF', Font='font10', BorderWidth=10):
	class MyWindow(xbmcgui.WindowDialog):
		scr={};
		def __init__(self,msg='',L=0,T=0,W=1280,H=720,TxtColor='0xFFFFFFFF',Font='font10',BorderWidth=10):
			buttonfocus, buttonnofocus = artwork('button')
			radiobgfocus, radiobgnofocus, radiofocus, radionofocus = artwork('radio')
			slidernibfocus, slidernibnofocus, sliderfocus, slidernofocus = artwork('slider')
			image_path = os.path.join(ART, 'ContentPanel.png')
			boxbg = os.path.join(ART, 'bgg2.png')
			self.border = xbmcgui.ControlImage(L,T,W,H, image_path)
			self.addControl(self.border); 
			self.BG=xbmcgui.ControlImage(L+BorderWidth,T+BorderWidth,W-(BorderWidth*2),H-(BorderWidth*2), FANART, aspectRatio=0, colorDiffuse='0x5FFFFFFF')
			self.addControl(self.BG)
			top = T+BorderWidth
			leftside = L+BorderWidth
			rightside = L+(W/2)-(BorderWidth*2)
			firstrow = top+30
			secondrow = firstrow+275+(BorderWidth/2)
			currentwidth = ((W/2)-(BorderWidth*4))/2
			
			header = '[COLOR lime]Konfigurator naprednih postavki[/COLOR]'
			self.Header=xbmcgui.ControlLabel(L, top, W, 30, header, font='font13', textColor=TxtColor, alignment=0x00000002)
			self.addControl(self.Header)
			top += 30+BorderWidth
			self.bgarea = xbmcgui.ControlImage(leftside, firstrow, rightside-L, 275, boxbg, aspectRatio=0, colorDiffuse='0x5FFFFFFF')
			self.addControl(self.bgarea)
			self.bgarea2 = xbmcgui.ControlImage(rightside+BorderWidth+BorderWidth, firstrow, rightside-L, 275, boxbg, aspectRatio=0, colorDiffuse='0x5FFFFFFF')
			self.addControl(self.bgarea2)
			self.bgarea3 = xbmcgui.ControlImage(leftside, secondrow, rightside-L, 275, boxbg, aspectRatio=0, colorDiffuse='0x5FFFFFFF')
			self.addControl(self.bgarea3)
			self.bgarea4 = xbmcgui.ControlImage(rightside+BorderWidth+BorderWidth, secondrow, rightside-L, 275, boxbg, aspectRatio=0, colorDiffuse='0x5FFFFFFF')
			self.addControl(self.bgarea4)
			
			header = '[COLOR white]Predmemorija videozapisa (Buffering)[/COLOR]'
			self.Header2=xbmcgui.ControlLabel(leftside+BorderWidth, firstrow+5, (W/2)-(BorderWidth*2), 20, header, font='font13', textColor=TxtColor, alignment=0x00000002)
			self.addControl(self.Header2)
			freeMemory = int(float(wiz.getInfo('System.Memory(free)')[:-2])*.33)
			recMemory = int(float(wiz.getInfo('System.Memory(free)')[:-2])*.23)
			msg3 = "[COLOR lime]Bajtovi koji se koriste za pohranu stream-ova. Postavkom na[/COLOR] [COLOR white]0[/COLOR] [COLOR lime]predmemorija ce se zapisivati na Hard disk umjesto u RAM.[/COLOR] [COLOR white]Napomena[/COLOR][COLOR lime]: Kodi zahtijeva 3x vise slobodne RAM memorije. Vrijednost ove postavke moze uzrokovati rusenje Kodi-a. 1/3 slobodne memorije[/COLOR] [COLOR white]%s[/COLOR]" % (freeMemory)
			self.Support3=xbmcgui.ControlTextBox(leftside+int(BorderWidth*1.5), firstrow+30+BorderWidth, (W/2)-(BorderWidth*4), 150, font='font12', textColor=TxtColor)
			self.addControl(self.Support3)
			self.Support3.setText(msg3)
			try: self.videoCacheSize=xbmcgui.ControlSlider(leftside+int(BorderWidth*1.5), firstrow+210,(W/2)-(BorderWidth*5),20, textureback=sliderfocus, texture=slidernibnofocus, texturefocus=slidernibfocus, orientation=xbmcgui.HORIZONTAL)
			except: self.videoCacheSize=xbmcgui.ControlSlider(leftside+int(BorderWidth*1.5), firstrow+210,(W/2)-(BorderWidth*5),20, textureback=sliderfocus, texture=slidernibnofocus, texturefocus=slidernibfocus)
			self.addControl(self.videoCacheSize)
			self.videomin = 0; self.videomax = freeMemory if freeMemory < 2000 else 2000
			self.recommendedVideo = recMemory if recMemory < 500 else 500; self.currentVideo = self.recommendedVideo
			videopos = wiz.percentage(self.currentVideo, self.videomax)
			self.videoCacheSize.setPercent(videopos)
			current1 = '[COLOR lime]Trenutno:[/COLOR] [COLOR white]%s MB[/COLOR]' % ( self.currentVideo)
			recommended1 = '[COLOR lime]Preporuceno:[/COLOR] [COLOR white]%s MB[/COLOR]' % ( self.recommendedVideo)
			self.currentVideo1=xbmcgui.ControlTextBox(leftside+BorderWidth,firstrow+235,currentwidth,20,font=Font,textColor=TxtColor)
			self.addControl(self.currentVideo1)
			self.currentVideo1.setText(current1)
			self.recommendedVideo1=xbmcgui.ControlTextBox(leftside+BorderWidth+currentwidth,firstrow+235,currentwidth,20,font=Font,textColor=TxtColor)
			self.addControl(self.recommendedVideo1)
			self.recommendedVideo1.setText(recommended1)
			
			header = '[COLOR white]CURL Timeout/CURL Mala brzina[/COLOR]'
			self.Header3=xbmcgui.ControlLabel(rightside+BorderWidth, firstrow+5, (W/2)-(BorderWidth*2), 20, header, font='font13', textColor=TxtColor, alignment=0x00000002)
			self.addControl(self.Header3)
			msg3 = "[COLOR white]CURL Timeout[/COLOR] [COLOR lime]je vrijeme u sekundama, potrebno da se prekine veza sa serverom - kad nema odgovora.[/COLOR] [COLOR white]CURL Mala brzina[/COLOR] [COLOR lime]je vrijeme u sekundama potrebno za utvrdivanje brzine veze. Za sporiju vezu postavite na[/COLOR] [COLOR white]20[/COLOR][COLOR lime].[/COLOR]"
			self.Support3=xbmcgui.ControlTextBox(rightside+int(BorderWidth*3.5), firstrow+30+BorderWidth, (W/2)-(BorderWidth*4), 150, font='font12', textColor=TxtColor)
			self.addControl(self.Support3)
			self.Support3.setText(msg3)
			try: self.CURLTimeout=xbmcgui.ControlSlider(rightside+int(BorderWidth*3.5),firstrow+210,(W/2)-(BorderWidth*5),20, textureback=sliderfocus, texture=slidernibnofocus, texturefocus=slidernibfocus, orientation=xbmcgui.HORIZONTAL)
			except: self.CURLTimeout=xbmcgui.ControlSlider(rightside+int(BorderWidth*3.5),firstrow+210,(W/2)-(BorderWidth*5),20, textureback=sliderfocus, texture=slidernibnofocus, texturefocus=slidernibfocus)
			self.addControl(self.CURLTimeout)
			self.curlmin = 0; self.curlmax = 20
			self.recommendedCurl = 10; self.currentCurl = self.recommendedCurl
			curlpos = wiz.percentage(self.currentCurl, self.curlmax)
			self.CURLTimeout.setPercent(curlpos)
			current2 = '[COLOR lime]Trenutno:[/COLOR] [COLOR white]%ss[/COLOR]' % (self.currentCurl)
			recommended2 = '[COLOR lime]Preporuceno:[/COLOR] [COLOR white]%ss[/COLOR]' % (self.recommendedCurl)
			self.currentCurl2=xbmcgui.ControlTextBox(rightside+(BorderWidth*3),firstrow+235,currentwidth,20,font=Font,textColor=TxtColor)
			self.addControl(self.currentCurl2)
			self.currentCurl2.setText(current2)
			self.recommendedCurl2=xbmcgui.ControlTextBox(rightside+(BorderWidth*3)+currentwidth,firstrow+235,currentwidth,20,font=Font,textColor=TxtColor)
			self.addControl(self.recommendedCurl2)
			self.recommendedCurl2.setText(recommended2)
			
			header = '[COLOR white]Faktor ucitavanja predmemorije[/COLOR]'
			self.Header4=xbmcgui.ControlLabel(leftside, secondrow+5, (W/2)-(BorderWidth*2), 20, header, font='font13', textColor=TxtColor, alignment=0x00000002)
			self.addControl(self.Header4)
			msg3 = "[COLOR lime]Vrijednost ove postavke je mnozitelj default-nog ogranicenja. Ako Kodi ucitava BlueRay datoteku na 36 Mbit/s, vrijednost od 2 ce trebati 72 Mbit/s propusnosti mreze.[/COLOR] [COLOR white]Napomena[/COLOR][COLOR lime]: Za razliku od RAM postavke, ovu postavku mozete sigurno povecati na zeljenu visinu i Kodi se nece srusiti.[/COLOR]"
			self.Support3=xbmcgui.ControlTextBox(leftside+int(BorderWidth*1.5), secondrow+30+BorderWidth, (W/2)-(BorderWidth*4), 150, font='font12', textColor=TxtColor)
			self.addControl(self.Support3)
			self.Support3.setText(msg3)
			try: self.readBufferFactor=xbmcgui.ControlSlider(leftside+int(BorderWidth*1.5), secondrow+210,(W/2)-(BorderWidth*5),20, textureback=sliderfocus, texture=slidernibnofocus, texturefocus=slidernibfocus, orientation=xbmcgui.HORIZONTAL)
			except: self.readBufferFactor=xbmcgui.ControlSlider(leftside+int(BorderWidth*1.5), secondrow+210,(W/2)-(BorderWidth*5),20, textureback=sliderfocus, texture=slidernibnofocus, texturefocus=slidernibfocus)
			self.addControl(self.readBufferFactor)
			self.readmin = 0; self.readmax = 10
			self.recommendedRead = 5; self.currentRead = self.recommendedRead
			readpos = wiz.percentage(self.currentRead, self.readmax)
			self.readBufferFactor.setPercent(readpos)
			current3 = '[COLOR lime]Trenutno:[/COLOR] [COLOR white]%s[/COLOR]' % ( self.currentRead)
			recommended3 = '[COLOR lime]Preporuceno:[/COLOR] [COLOR white]%s[/COLOR]' % (self.recommendedRead)
			self.currentRead3=xbmcgui.ControlTextBox(leftside+BorderWidth,secondrow+235,currentwidth,20,font=Font,textColor=TxtColor)
			self.addControl(self.currentRead3)
			self.currentRead3.setText(current3)
			self.recommendedRead3=xbmcgui.ControlTextBox(leftside+BorderWidth+currentwidth,secondrow+235,currentwidth,20,font=Font,textColor=TxtColor)
			self.addControl(self.recommendedRead3)
			self.recommendedRead3.setText(recommended3)
			
			header = '[COLOR white]Nacin rada predmemorije[/COLOR]'
			self.Header4=xbmcgui.ControlLabel(rightside+BorderWidth, secondrow+5, (W/2)-(BorderWidth*2), 20, header, font='font13', textColor=TxtColor, alignment=0x00000002)
			self.addControl(self.Header4)
			msg4 = "[COLOR lime]Ova postavka prisiljava Kodi da koristi predmemoriju za sav video, lokalnu mrezu, internet i Hard disk. Zadana vrijednost je[/COLOR] [COLOR white]0[/COLOR] [COLOR lime]i predmemorija ce se koristiti za videozapise koji se ucitavaju putem interneta.[/COLOR]"
			self.Support4=xbmcgui.ControlTextBox(rightside+int(BorderWidth*3.5), secondrow+30+BorderWidth, (W/2)-(BorderWidth*4), 110, font='font12', textColor=TxtColor)
			self.addControl(self.Support4)
			self.Support4.setText(msg4)
			B1 = secondrow+130+BorderWidth; B2 = B1+30; B3 = B2+30; B4 = B3+30;
			self.Button0 = xbmcgui.ControlRadioButton(rightside+(BorderWidth*3), B1, (W/2)-(BorderWidth*4), 30, '[COLOR white]Predmemorija svih internetskih sustava[/COLOR]', font='font10', focusTexture=radiobgfocus, noFocusTexture=radiobgnofocus, focusOnTexture=radiofocus, noFocusOnTexture=radiofocus, focusOffTexture=radionofocus, noFocusOffTexture=radionofocus)
			self.Button1 = xbmcgui.ControlRadioButton(rightside+(BorderWidth*3), B2, (W/2)-(BorderWidth*4), 30, '[COLOR white]Predmemorija svih sustava[/COLOR]', font='font10', focusTexture=radiobgfocus, noFocusTexture=radiobgnofocus, focusOnTexture=radiofocus, noFocusOnTexture=radiofocus, focusOffTexture=radionofocus, noFocusOffTexture=radionofocus)
			self.Button2 = xbmcgui.ControlRadioButton(rightside+(BorderWidth*3), B3, (W/2)-(BorderWidth*4), 30, '[COLOR white]Samo predmemorija internetskih sustava[/COLOR]', font='font10', focusTexture=radiobgfocus, noFocusTexture=radiobgnofocus, focusOnTexture=radiofocus, noFocusOnTexture=radiofocus, focusOffTexture=radionofocus, noFocusOffTexture=radionofocus)
			self.Button3 = xbmcgui.ControlRadioButton(rightside+(BorderWidth*3), B4, (W/2)-(BorderWidth*4), 30, '[COLOR white]Bez predmemorije[/COLOR]', font='font10', focusTexture=radiobgfocus, noFocusTexture=radiobgnofocus, focusOnTexture=radiofocus, noFocusOnTexture=radiofocus, focusOffTexture=radionofocus, noFocusOffTexture=radionofocus)
			self.addControl(self.Button0)
			self.addControl(self.Button1)
			self.addControl(self.Button2)
			self.addControl(self.Button3)
			self.Button0.setSelected(False)
			self.Button1.setSelected(False)
			self.Button2.setSelected(True)
			self.Button3.setSelected(False)
			
			self.buttonWrite=xbmcgui.ControlButton(leftside,T+H-40-BorderWidth,(W/2)-(BorderWidth*2),35,"Napravi datoteku",textColor="0xFFFFFFFF",focusedColor="0xFF04fc05",alignment=2,focusTexture=buttonfocus,noFocusTexture=buttonnofocus)
			self.buttonCancel=xbmcgui.ControlButton(rightside+BorderWidth*2,T+H-40-BorderWidth,(W/2)-(BorderWidth*2),35,"Odustani",textColor="0xFFFFFFFF",focusedColor="0xFF04fc05",alignment=2,focusTexture=buttonfocus,noFocusTexture=buttonnofocus)
			self.addControl(self.buttonWrite); self.addControl(self.buttonCancel)
			
			self.buttonWrite.controlLeft(self.buttonCancel); self.buttonWrite.controlRight(self.buttonCancel); self.buttonWrite.controlUp(self.Button3); self.buttonWrite.controlDown(self.videoCacheSize)
			self.buttonCancel.controlLeft(self.buttonWrite); self.buttonCancel.controlRight(self.buttonWrite); self.buttonCancel.controlUp(self.Button3); self.buttonCancel.controlDown(self.videoCacheSize)
			self.videoCacheSize.controlUp(self.buttonWrite); self.videoCacheSize.controlDown(self.CURLTimeout)
			self.CURLTimeout.controlUp(self.videoCacheSize); self.CURLTimeout.controlDown(self.readBufferFactor)
			self.readBufferFactor.controlUp(self.CURLTimeout); self.readBufferFactor.controlDown(self.Button0)
			self.Button0.controlUp(self.CURLTimeout); self.Button0.controlDown(self.Button1); self.Button0.controlLeft(self.readBufferFactor); self.Button0.controlRight(self.readBufferFactor);
			self.Button1.controlUp(self.Button0); self.Button1.controlDown(self.Button2); self.Button1.controlLeft(self.readBufferFactor); self.Button1.controlRight(self.readBufferFactor);
			self.Button2.controlUp(self.Button1); self.Button2.controlDown(self.Button3); self.Button2.controlLeft(self.readBufferFactor); self.Button2.controlRight(self.readBufferFactor);
			self.Button3.controlUp(self.Button2); self.Button3.controlDown(self.buttonWrite); self.Button3.controlLeft(self.readBufferFactor); self.Button3.controlRight(self.readBufferFactor);
			self.setFocus(self.videoCacheSize)
			
		def doExit(self):
			self.CloseWindow()
			
		def updateCurrent(self, control):
			if control == self.videoCacheSize:
				self.currentVideo = (self.videomax)*self.videoCacheSize.getPercent()/100
				current = '[COLOR lime]Trenutno:[/COLOR] [COLOR white]%s MB[/COLOR]' % (int(self.currentVideo))
				self.currentVideo1.setText(current)
				
			elif control == self.CURLTimeout:
				self.currentCurl = (self.curlmax)*self.CURLTimeout.getPercent()/100
				current = '[COLOR lime]Trenutno:[/COLOR] [COLOR white]%ss[/COLOR]' % (int(self.currentCurl))
				self.currentCurl2.setText(current)
				
			elif control == self.readBufferFactor:
				self.currentRead = (self.readmax)*self.readBufferFactor.getPercent()/100
				current = '[COLOR lime]Trenutno:[/COLOR] [COLOR white]%s[/COLOR]' % (int(self.currentRead))
				self.currentRead3.setText(current)
				
			elif control in [self.Button0, self.Button1, self.Button2, self.Button3]:
				self.Button0.setSelected(False)
				self.Button1.setSelected(False)
				self.Button2.setSelected(False)
				self.Button3.setSelected(False)
				control.setSelected(True)

		def doWrite(self):
			#self.currentVideo = int((self.videomax-20)*self.videoCacheSize.getPercent()/100+20)*1024*1024
			#self.currentCurl = int((self.curlmax)*self.CURLTimeout.getPercent()/100)
			#self.currentRead = int((self.readmax)*self.readBufferFactor.getPercent()/100)
			if   self.Button0.isSelected(): buffermode = 0
			elif self.Button1.isSelected(): buffermode = 1
			elif self.Button2.isSelected(): buffermode = 2
			elif self.Button3.isSelected(): buffermode = 3
			if os.path.exists(ADVANCED):
				choice = DIALOG.yesno(ADDONTITLE, "[COLOR lime]Trenutno je aktivan[/COLOR] [COLOR white]AdvancedSettings.xml[/COLOR][COLOR lime], zelite li ukloniti i nastaviti?[/COLOR]"  , yeslabel="[B][COLOR white]Nastavi[/COLOR][/B]", nolabel="[B][COLOR white]Odustani[/COLOR][/B]")
				if choice == 0: return
				try: os.remove(ADVANCED)
				except: f = open(ADVANCED, 'w'); f.close()
			if KODIV < 17:
				with open(ADVANCED, 'w+') as f:
					f.write('<advancedsettings>\n')
					f.write('	<network>\n')
					f.write('		<buffermode>%s</buffermode>\n' % buffermode)
					f.write('		<cachemembuffersize>%s</cachemembuffersize>\n' % int(self.currentVideo*1024*1024))
					f.write('		<readbufferfactor>%s</readbufferfactor>\n' % self.currentRead)
					f.write('		<curlclienttimeout>%s</curlclienttimeout>\n' % self.currentCurl)
					f.write('		<curllowspeedtime>%s</curllowspeedtime>\n' % self.currentCurl)
					f.write('	</network>\n')
					f.write('</advancedsettings>\n')
				f.close()
			else:
				with open(ADVANCED, 'w+') as f:
					f.write('<advancedsettings>\n')
					f.write('	<cache>\n')
					f.write('		<buffermode>%s</buffermode>\n' % buffermode)
					f.write('		<memorysize>%s</memorysize>\n' % int(self.currentVideo*1024*1024))
					f.write('		<readfactor>%s</readfactor>\n' % self.currentRead)
					f.write('	</cache>\n')
					f.write('	<network>\n')
					f.write('		<curlclienttimeout>%s</curlclienttimeout>\n' % self.currentCurl)
					f.write('		<curllowspeedtime>%s</curllowspeedtime>\n' % self.currentCurl)
					f.write('	</network>\n')
					f.write('</advancedsettings>\n')
				f.close()
				wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]AdvancedSettings.xml have been written[/COLOR]' % COLOR2)
			self.CloseWindow()
			
		def onControl(self, control):
			if   control==self.buttonWrite: self.doWrite()
			elif control==self.buttonCancel:  self.doExit()

		def onAction(self, action):
			try: F=self.getFocus()
			except: F=False
			if   F      == self.videoCacheSize:   self.updateCurrent(self.videoCacheSize)
			elif F      == self.CURLTimeout:      self.updateCurrent(self.CURLTimeout)
			elif F      == self.readBufferFactor: self.updateCurrent(self.readBufferFactor)
			elif F      in [self.Button0, self.Button1, self.Button2, self.Button3] and action in [ACTION_MOUSE_LEFT_CLICK, ACTION_SELECT_ITEM]: self.updateCurrent(F)
			elif action == ACTION_PREVIOUS_MENU:  self.doExit()
			elif action == ACTION_NAV_BACK:       self.doExit()
			
		def CloseWindow(self): self.close()

	maxW=1280; maxH=720; W=int(900); H=int(650); L=int((maxW-W)/2); T=int((maxH-H)/2); 
	TempWindow=MyWindow(L=L,T=T,W=W,H=H,TxtColor=TxtColor,Font=Font,BorderWidth=BorderWidth); 
	TempWindow.doModal() 
	del TempWindow
##########################################
#  `7MM"""YMM MMP""MM""YMM   .g8"""bgd   #
#    MM    `7 P'   MM   `7 .dP'     `M   #
#    MM   d        MM      dM'       `   #
#    MM""MM        MM      MM            #
#    MM   Y        MM      MM.    `7MMF' #
#    MM            MM      `Mb.     MM   #
#  .JMML.        .JMML.      `"bmmmdPY   #
########################################## 
def autoConfig2(msg='', TxtColor='0xFFFFFFFF', Font='font10', BorderWidth=10):
	class MyWindow(xbmcgui.WindowDialog):
		scr={};
		def __init__(self,msg='',L=0,T=0,W=1280,H=720,TxtColor='0xFFFFFFFF',Font='font10',BorderWidth=10):
			buttonfocus, buttonnofocus = artwork('button')
			self.BG=xbmcgui.ControlImage(L+BorderWidth,T+BorderWidth,W-(BorderWidth*2),H-(BorderWidth*2), FANART, aspectRatio=0)
			self.addControl(self.BG)
			top = T+BorderWidth
			leftside = L+BorderWidth
			rightside = L+(W/2)-(BorderWidth*2)
			
			header = '[COLOR lime]Brzo konfiguriranje naprednih postavki[/COLOR]'
			self.Header=xbmcgui.ControlLabel(L, top, W, 30, header, font='font13', textColor=TxtColor, alignment=0x00000002)
			self.addControl(self.Header)
			top += 30+BorderWidth
			
			#####Video Cache Size####
			freeMemory = int(float(wiz.getInfo('System.Memory(free)')[:-2])*.33)
			recMemory = int(float(wiz.getInfo('System.Memory(free)')[:-2])*.23)

			self.videomin = 0; self.videomax = freeMemory if freeMemory < 2000 else 2000
			self.recommendedVideo = recMemory if recMemory < 500 else 500; self.currentVideo = self.recommendedVideo
			current1 = '[COLOR lime]Velicina predmomorije videa:[/COLOR]=[COLOR white]%s MB[/COLOR]' % (self.currentVideo)
			recommended1 = '[COLOR lime]Velicina predmemorije videozapisa:[/COLOR] [COLOR white]%s MB[/COLOR]' % (self.recommendedVideo)
			
			####CURL Timeout/CURL Low Speed####
			self.curlmin = 0; self.curlmax = 20
			self.recommendedCurl = 10; self.currentCurl = self.recommendedCurl
			curlpos = wiz.percentage(self.currentCurl, self.curlmax)
			recommended2 = '[COLOR lime]CURL pauza/CURL niska brzina:[/COLOR] [COLOR white]%ss[/COLOR]' % (self.recommendedCurl)
			
			########Read Buffer Factor#####
			self.readmin = 0; self.readmax = 10
			self.recommendedRead = 5; self.currentRead = self.recommendedRead
			readpos = wiz.percentage(self.currentRead, self.readmax)
			recommended3 = '[COLOR lime]Ocitavanje buffera[/COLOR] [COLOR white]%s[/COLOR]' % (self.recommendedRead)
			
			######Buffer Mode#####
			recommended4 = '[COLOR lime]Buffer Mode:[/COLOR] [COLOR white]2[/COLOR]' 

			
			####BOX##
			msgbox='[COLOR lime]Postavke ce se upisati u advancesettings.xml[/COLOR]\r\n\r\n%s\r\n%s\r\n%s\r\n%s' %(recommended4, recommended1, recommended3, recommended2)
			self.box=xbmcgui.ControlTextBox(L+25,T+50,W,H, font='font14')
			self.addControl(self.box)
			self.box.setText(msgbox)
			
			####Buttons###
			
			
			
			self.buttonWrite=xbmcgui.ControlButton(leftside,T+H-40-BorderWidth,(W/2)-(BorderWidth*2),35,"Napravi datoteku",textColor="0xFFFFFFFF",focusedColor="0xFF04fc05",alignment=2,focusTexture=buttonfocus,noFocusTexture=buttonnofocus)
			self.buttonCancel=xbmcgui.ControlButton(rightside+BorderWidth*2,T+H-40-BorderWidth,(W/2)-(BorderWidth*2),35,"Odustani",textColor="0xFFFFFFFF",focusedColor="0xFF04fc05",alignment=2,focusTexture=buttonfocus,noFocusTexture=buttonnofocus)
			
			self.addControl(self.buttonWrite); self.addControl(self.buttonCancel)
			self.setFocus(self.buttonCancel)
			
			self.buttonWrite.controlLeft(self.buttonCancel); self.buttonWrite.controlRight(self.buttonCancel); self.buttonCancel.controlLeft(self.buttonWrite); self.buttonCancel.controlRight(self.buttonWrite)
			

			
		def doExit(self):
			self.CloseWindow()
			
		def updateCurrent(self, control):
			if control == self.videoCacheSize:
				self.currentVideo = (self.videomax)*self.videoCacheSize.getPercent()/100
				current = '[COLOR lime]Trenutno:[/COLOR] [COLOR white]%s MB[/COLOR]' % (int(self.currentVideo))
				self.currentVideo1.setText(current)
				
			elif control == self.CURLTimeout:
				self.currentCurl = (self.curlmax)*self.CURLTimeout.getPercent()/100
				current = '[COLOR lime]Trenutno:[/COLOR] [COLOR white]%ss[/COLOR]' % (int(self.currentCurl))
				self.currentCurl2.setText(current)
				
			elif control == self.readBufferFactor:
				self.currentRead = (self.readmax)*self.readBufferFactor.getPercent()/100
				current = '[COLOR lime]Trenutno:[/COLOR] [COLOR white]%s[/COLOR]' % (int(self.currentRead))
				self.currentRead3.setText(current)
				

		def doWrite(self):

			buffermode = 2

			if os.path.exists(ADVANCED):
				choice = DIALOG.yesno(ADDONTITLE, "[COLOR lime]Trenutno je aktivan[/COLOR] [COLOR white]AdvancedSettings.xml[/COLOR][COLOR lime], zelite li ukloniti i nastaviti?[/COLOR]" , yeslabel="[B][COLOR white]Nastavi[/COLOR][/B]", nolabel="[B][COLOR white]Odustani[/COLOR][/B]")
				if choice == 0: return
				try: os.remove(ADVANCED)
				except: f = open(ADVANCED, 'w'); f.close()
			if KODIV < 17:
				with open(ADVANCED, 'w+') as f:
					f.write('<advancedsettings>\n')
					f.write('	<network>\n')
					f.write('		<buffermode>%s</buffermode>\n' % buffermode)
					f.write('		<cachemembuffersize>%s</cachemembuffersize>\n' % int(self.currentVideo*1024*1024))
					f.write('		<readbufferfactor>%s</readbufferfactor>\n' % self.currentRead)
					f.write('		<curlclienttimeout>%s</curlclienttimeout>\n' % self.currentCurl)
					f.write('		<curllowspeedtime>%s</curllowspeedtime>\n' % self.currentCurl)
					f.write('	</network>\n')
					f.write('</advancedsettings>\n')
				f.close()
			else:
				with open(ADVANCED, 'w+') as f:
					f.write('<advancedsettings>\n')
					f.write('	<cache>\n')
					f.write('		<buffermode>%s</buffermode>\n' % buffermode)
					f.write('		<memorysize>%s</memorysize>\n' % int(self.currentVideo*1024*1024))
					f.write('		<readfactor>%s</readfactor>\n' % self.currentRead)
					f.write('	</cache>\n')
					f.write('	<network>\n')
					f.write('		<curlclienttimeout>%s</curlclienttimeout>\n' % self.currentCurl)
					f.write('		<curllowspeedtime>%s</curllowspeedtime>\n' % self.currentCurl)
					f.write('	</network>\n')
					f.write('</advancedsettings>\n')
				f.close()
				wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]AdvancedSettings.xml have been written[/COLOR]' % COLOR2)
			self.CloseWindow()
			
		def onControl(self, control):
			if   control==self.buttonWrite: self.doWrite()
			elif control==self.buttonCancel:  self.doExit()

		def onAction(self, action):
			try: F=self.getFocus()
			except: F=False
			if action == ACTION_PREVIOUS_MENU:  self.doExit()
			elif action == ACTION_NAV_BACK:       self.doExit()
			
		def CloseWindow(self): self.close()

	maxW=1280; maxH=720; W=int(700); H=int(350); L=int((maxW-W)/2); T=int((maxH-H)/2); 
	TempWindow=MyWindow(L=L,T=T,W=W,H=H,TxtColor=TxtColor,Font=Font,BorderWidth=BorderWidth); 
	TempWindow.doModal() 
	del TempWindow

##########################
### Converted to XML
##########################

def contact(msg=""):
	class MyWindow(xbmcgui.WindowXMLDialog):
		def __init__(self, *args, **kwargs):
			self.title = THEME3 % kwargs["title"]
			self.image = kwargs["image"]
			self.fanart = kwargs["fanart"]
			self.msg = THEME2 % kwargs["msg"]

		def onInit(self):
			self.fanartimage = 101
			self.titlebox = 102
			self.imagecontrol = 103
			self.textbox = 104
			self.scrollcontrol = 105
			self.showdialog()

		def showdialog(self):
			self.getControl(self.imagecontrol).setImage(self.image)
			self.getControl(self.fanartimage).setImage(self.fanart)
			self.getControl(self.fanartimage).setColorDiffuse('9FFFFFFF')
			self.getControl(self.textbox).setText(self.msg)
			self.getControl(self.titlebox).setLabel(self.title)
			self.setFocusId(self.scrollcontrol)
			
		def onAction(self,action):
			if   action == ACTION_PREVIOUS_MENU: self.close()
			elif action == ACTION_NAV_BACK: self.close()

	cw = MyWindow( "Contact.xml" , ADDON.getAddonInfo('path'), 'DefaultSkin', title=ADDONTITLE, fanart=CONTACTFANART, image=CONTACTICON, msg=msg)
	cw.doModal()
	del cw

def apkInstaller(apk):
	class APKInstaller(xbmcgui.WindowXMLDialog):
		def __init__(self,*args,**kwargs):
			self.shut=kwargs['close_time']
			xbmc.executebuiltin("Skin.Reset(AnimeWindowXMLDialogClose)")
			xbmc.executebuiltin("Skin.SetBool(AnimeWindowXMLDialogClose)")

		def onClick(self,controlID): self.CloseWindow()

		def onAction(self,action):
			if action in [ACTION_PREVIOUS_MENU, ACTION_BACKSPACE, ACTION_NAV_BACK, ACTION_SELECT_ITEM, ACTION_MOUSE_LEFT_CLICK, ACTION_MOUSE_LONG_CLICK]: self.CloseWindow()

		def CloseWindow(self):
			xbmc.executebuiltin("Skin.Reset(AnimeWindowXMLDialogClose)")
			xbmc.sleep(400)
			self.close()
	
	xbmc.executebuiltin('Skin.SetString(apkinstaller, Now that %s has been downloaded[CR]Click install on the next window!)' % apk)
	popup = APKInstaller('APK.xml', ADDON.getAddonInfo('path'), 'DefaultSkin', close_time=34)
	popup.doModal()
	del popup

def speedTest(img):
	class speedTest(xbmcgui.WindowXMLDialog):
		def __init__(self,*args,**kwargs):
			self.imgfile    = kwargs['img']
		
		def onInit(self):
			self.imagespeed = 101
			self.button     = 201
			self.showdialog()
			
		def showdialog(self):
			self.setFocus(self.getControl(self.button))
			self.getControl(self.imagespeed).setImage(self.imgfile)

		def onClick(self,controlID): self.CloseWindow()

		def onAction(self,action):
			if action in [ACTION_PREVIOUS_MENU, ACTION_BACKSPACE, ACTION_NAV_BACK, ACTION_SELECT_ITEM, ACTION_MOUSE_LEFT_CLICK, ACTION_MOUSE_LONG_CLICK]: self.CloseWindow()

		def CloseWindow(self):
			self.close()
	
	popup = speedTest('SpeedTest.xml', ADDON.getAddonInfo('path'), 'DefaultSkin', img=img)
	popup.doModal()
	del popup
	
def Preview(url):
	class YTvid(xbmcgui.WindowXMLDialog):
		def __init__(self,*args,**kwargs):
			self.url    = kwargs['url']
		
		def onInit(self):
			self.button    = 101
			self.Obutton    = 102
			self.showdialog()
			
		def showdialog(self):
			self.setFocus(self.getControl(self.Obutton))
			if wiz.getCond('System.HasAddon(plugin.video.youtube)') == 1:
				url = 'plugin://plugin.video.youtube/play/?video_id=%s' % self.url
				xbmc.Player().play(url, windowed=False)
				xbmc.sleep(2000)
			if xbmc.Player().isPlayingVideo() == 0:
				yt.PlayVideoB(self.url)

		def onClick(self,controlID):
			if controlId == self.Obutton:
				self.close()		
			else: self.CloseWindow()

		def onAction(self,action):
			if action in [ACTION_PREVIOUS_MENU, ACTION_BACKSPACE, ACTION_NAV_BACK, ACTION_SELECT_ITEM, ACTION_MOUSE_LEFT_CLICK, ACTION_MOUSE_LONG_CLICK]: self.CloseWindow(); xbmc.Player().stop()

		def CloseWindow(self):
			self.close()
	
	YTv = YTvid('Preview.xml', ADDON.getAddonInfo('path'), 'DefaultSkin', url=url)
	YTv.doModal()
	del YTv

def firstRunSettings():
	class firstRun(xbmcgui.WindowXMLDialog):
		def __init__(self,*args,**kwargs):
			self.whitelistcurrent = kwargs['current']
		
		def onInit(self):
			self.title      = 101
			self.okbutton   = 201
			self.trakt      = 301
			self.debrid     = 302
			self.login      = 303
			self.alluc      = 314
			self.profiles   = 305
			self.advanced   = 306
			self.favourites = 307
			self.superfav   = 308
			self.repo       = 309
			self.whitelist  = 310
			self.cache      = 311
			self.showdialog()
			self.controllist     = [self.trakt, self.debrid, self.login, 
									self.profiles, self.advanced, 
									self.favourites, self.superfav, self.repo, 
									self.whitelist, self.cache,  self.alluc]
			self.controlsettings = ['keeptrakt', 'keepdebrid', 'keeplogin',
									'keepprofiles', 'keepadvanced',
									'keepfavourites', 'keeprepos', 'keepsuper', 
									'keepwhitelist', 'clearcache', 'keepalluc']
									
			for item in self.controllist:
				if wiz.getS(self.controlsettings[self.controllist.index(item)]) == 'true':
					self.getControl(item).setSelected(True)

		def showdialog(self):
			self.getControl(self.title).setLabel(ADDONTITLE)
			self.setFocus(self.getControl(self.okbutton))
			
		def onClick(self, controlId):
			if controlId == self.okbutton:
				self.close()

				for item in self.controllist:
					at = self.controllist.index(item)
					if self.getControl(item).isSelected(): wiz.setS(self.controlsettings[at], 'true')
					else: wiz.setS(self.controlsettings[at], 'false')
						
				if self.getControl(self.whitelist).isSelected() and not self.whitelistcurrent == 'true':
					wiz.whiteList('edit')

	fr = firstRun( "FirstRunSaveData.xml" , ADDON.getAddonInfo('path'), 'DefaultSkin', current=wiz.getS('keepwhitelist'))
	fr.doModal()
	del fr

def firstRun():
	class MyWindow(xbmcgui.WindowXMLDialog):
		def __init__(self, *args, **kwargs):
			self.title = THEME3 % ADDONTITLE
			self.msg   = "Trenutno nije instaliran %s.\n\nOdabrati 'INSTALIRAJ' za instalaciju %s ili 'ODUSTANI' za prekidanje instalacije.\n\nHvala na odabiru %s." % (ADDONTITLE,BUILDERNAME, ADDONTITLE)
			self.msg   = THEME2 % self.msg

		def onInit(self):
			self.image     = 101
			self.titlebox  = 102
			self.textbox   = 103
			self.buildmenu = 201
			self.ignore    = 202
			self.showdialog()

		def showdialog(self):
			self.getControl(self.image).setImage(FANART)
			self.getControl(self.image).setColorDiffuse('9FFFFFFF')
			self.getControl(self.textbox).setText(self.msg)
			self.getControl(self.titlebox).setLabel(self.title)
			self.setFocusId(self.buildmenu)
		
		def doBuildMenu(self):
			wiz.log("[Check Updates] [User Selected: Open Build Menu] [Next Check: %s]" % str(NEXTCHECK), xbmc.LOGNOTICE)
			wiz.setS('lastbuildcheck', str(NEXTCHECK))
			self.close()
			url = 'plugin://%s/?mode=builds' % ADDON_ID
			xbmc.executebuiltin('ActivateWindow(10025, "%s", return)' % url)
		
		def doIgnore(self):
			self.close()
			wiz.log("[First Run] [User Selected: Ignore Build Menu] [Next Check: %s]" % str(NEXTCHECK), xbmc.LOGNOTICE)
			wiz.setS('lastbuildcheck', str(NEXTCHECK))
		
		def onAction(self,action):
			if   action == ACTION_PREVIOUS_MENU: self.doIgnore()
			elif action == ACTION_NAV_BACK: self.doIgnore()

		def onClick(self, controlId):
			if (controlId == self.buildmenu): self.doBuildMenu()
			else: self.doIgnore()
	
	fr = MyWindow( "FirstRunBuild.xml" , ADDON.getAddonInfo('path'), 'DefaultSkin')
	fr.doModal()
	del fr

def notification(msg='', test=False):
	class MyWindow(xbmcgui.WindowXMLDialog):
		def __init__(self, *args, **kwargs):
			self.test = kwargs['test']
			self.message =  THEME2 % kwargs['msg']
		
		def onInit(self):
			self.image       = 101
			self.titlebox    = 102
			self.titleimage  = 103
			self.textbox     = 104
			self.scroller    = 105
			self.dismiss     = 201
			self.remindme    = 202
			self.showdialog()

		def showdialog(self):
			self.testimage = os.path.join(ART, 'text.png')
			self.getControl(self.image).setImage(BACKGROUND)
			self.getControl(self.image).setColorDiffuse('9FFFFFFF')
			self.getControl(self.textbox).setText(self.message)
			self.setFocusId(self.remindme)
			if HEADERTYPE == 'Text':
				self.getControl(self.titlebox).setLabel(THEME3 % HEADERMESSAGE)
			else:
				self.getControl(self.titleimage).setImage(HEADERIMAGE)

		def doRemindMeLater(self):
			if not test == True:
				wiz.setS("notedismiss","false")
			wiz.log("[Notification] NotifyID %s Remind Me Later" % wiz.getS('noteid'), xbmc.LOGNOTICE)
			self.close()

		def doDismiss(self):
			if not test == True:
				wiz.setS("notedismiss","true")
			wiz.log("[Notification] NotifyID %s Dismissed" % wiz.getS('noteid'), xbmc.LOGNOTICE)
			self.close()

		def onAction(self,action):
			if   action == ACTION_PREVIOUS_MENU: self.doRemindMeLater()
			elif action == ACTION_NAV_BACK: self.doRemindMeLater()

		def onClick(self, controlId):
			if (controlId == self.dismiss): self.doDismiss()
			else: self.doRemindMeLater()
			
	xbmc.executebuiltin('Skin.SetString(headertexttype, %s)' % 'true' if HEADERTYPE == 'Text' else 'false')
	xbmc.executebuiltin('Skin.SetString(headerimagetype, %s)' % 'true' if HEADERTYPE == 'Image' else 'false')
	notify = MyWindow( "Notifications.xml" , ADDON.getAddonInfo('path'), 'DefaultSkin', msg=msg, test=test)
	notify.doModal()
	del notify

def updateWindow(name='Testing Window', current='1.0', new='1.1', icon=ICON, fanart=FANART):
	class MyWindow(xbmcgui.WindowXMLDialog):
		def __init__(self, *args, **kwargs):
			self.name = THEME3 % kwargs['name']
			self.current = kwargs['current']
			self.new = kwargs['new']
			self.icon = kwargs['icon']
			self.fanart = kwargs['fanart']
			self.msgupdate  = "[COLOR lime]Dostupna nadogranja za build:[COLOR] [COLOR white]\n%s\n\n[/COLOR] [COLOR lime]Trenutna verzija:[/COLOR] [COLOR white]%s[/COLOR]\n[COLOR lime]Dostupna verzija:[/COLOR] [COLOR white]%s[/COLOR]\n\n[COLOR white]**Preporuka**: Svjeza instalacija[/COLOR]" % (self.name, self.current, self.new)
			self.msgcurrent = "Running latest version of installed build:\n[COLOR %s]%s[/COLOR]\n\nCurrent Version: v[COLOR %s]%s[/COLOR]\nLatest Version: v[COLOR %s]%s[/COLOR]\n\n[COLOR %s]*Recommended: Fresh install[/COLOR]" % (COLOR1, self.name, COLOR1, self.current, COLOR1, self.new, COLOR1)
		
		def onInit(self):
			self.imagefanart = 101
			self.header      = 102
			self.textbox     = 103
			self.imageicon   = 104
			self.fresh       = 201
			self.normal      = 202
			self.ignore      = 203
			self.showdialog()

		def showdialog(self):
			self.getControl(self.header).setLabel(self.name)
			self.getControl(self.textbox).setText(THEME2 % self.msgupdate if current < new else self.msgcurrent)
			self.getControl(self.imagefanart).setImage(self.fanart)
			self.getControl(self.imagefanart).setColorDiffuse('2FFFFFFF')
			self.getControl(self.imageicon).setImage(self.icon)
			self.setFocusId(self.fresh)

		def doFreshInstall(self):
			wiz.log("[Check Updates] [Installed Version: %s] [Current Version: %s] [User Selected: Fresh Install build]" % (BUILDVERSION, LATESTVERSION), xbmc.LOGNOTICE)
			wiz.log("[Check Updates] [Next Check: %s]" % str(NEXTCHECK), xbmc.LOGNOTICE)
			wiz.setS('lastbuildcheck', str(NEXTCHECK))
			self.close()
			url = 'plugin://%s/?mode=install&name=%s&url=fresh' % (ADDON_ID, urllib.quote_plus(BUILDNAME))
			xbmc.executebuiltin('RunPlugin(%s)' % url)

		def doNormalInstall(self):
			wiz.log("[Check Updates] [Installed Version: %s] [Current Version: %s] [User Selected: Normal Install build]" % (BUILDVERSION, LATESTVERSION), xbmc.LOGNOTICE)
			wiz.log("[Check Updates] [Next Check: %s]" % str(NEXTCHECK), xbmc.LOGNOTICE)
			wiz.setS('lastbuildcheck', str(NEXTCHECK))
			self.close()
			url = 'plugin://%s/?mode=install&name=%s&url=normal' % (ADDON_ID, urllib.quote_plus(BUILDNAME))
			xbmc.executebuiltin('RunPlugin(%s)' % url)

		def doIgnore(self):
			wiz.log("[Check Updates] [Installed Version: %s] [Current Version: %s] [User Selected: Ignore 3 Days]" % (BUILDVERSION, LATESTVERSION), xbmc.LOGNOTICE)
			wiz.log("[Check Updates] [Next Check: %s]" % str(THREEDAYS), xbmc.LOGNOTICE)
			wiz.setS('lastbuildcheck', str(THREEDAYS))
			self.close()

		def onAction(self,action):
			if   action == ACTION_PREVIOUS_MENU: self.doIgnore()
			elif action == ACTION_NAV_BACK: self.doIgnore()

		def onClick(self, controlId):
			if   (controlId == self.fresh): self.doFreshInstall()
			elif (controlId == self.normal): self.doNormalInstall()
			else: self.doIgnore()

	update = MyWindow( "BuildUpdate.xml" , ADDON.getAddonInfo('path'), 'DefaultSkin', name=name, current=current, new=new, icon=icon, fanart=fanart)
	update.doModal()
	del update