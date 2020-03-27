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

import zipfile, xbmcaddon, xbmc, uservar, sys, os, time

import wizard as wiz
KODIV          = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
if KODIV > 17:
	import zfile as zipfile #FTG mod for Kodi 18
else:
	import zipfile

ADDON_ID       = uservar.ADDON_ID
ADDONTITLE     = uservar.ADDONTITLE
COLOR1         = uservar.COLOR1
COLOR2         = uservar.COLOR2
ADDON          = wiz.addonId(ADDON_ID)
HOME           = xbmc.translatePath('special://home/')
USERDATA       = os.path.join(HOME,      'userdata')
GUISETTINGS    = os.path.join(USERDATA,  'guisettings.xml')
KEEPFAVS       = wiz.getS('keepfavourites')
KEEPSOURCES    = wiz.getS('keepsources')
KEEPPROFILES   = wiz.getS('keepprofiles')
KEEPADVANCED   = wiz.getS('keepadvanced')
KEEPSUPER      = wiz.getS('keepsuper')
KEEPREPOS      = wiz.getS('keeprepos')
KEEPWHITELIST  = wiz.getS('keepwhitelist')
KODIV          = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
LOGFILES       = ['xbmc.log', 'xbmc.old.log', 'kodi.log', 'kodi.old.log', 'spmc.log', 'spmc.old.log', 'tvmc.log', 'tvmc.old.log', 'Thumbs.db', '.gitignore', '.DS_Store']
bad_files      = ['onechannelcache.db', 'saltscache.db', 'saltscache.db-shm', 'saltscache.db-wal', 'saltshd.lite.db', 'saltshd.lite.db-shm', 'saltshd.lite.db-wal', 'queue.db', 'commoncache.db', 'access.log', 'trakt.db', 'video_cache.db']

def all(_in, _out, dp=None, ignore=None, title=None):
	if dp: return allWithProgress(_in, _out, dp, ignore, title)
	else: return allNoProgress(_in, _out, ignore)

def allNoProgress(_in, _out, ignore):
	try:
		zin = zipfile.ZipFile(_in, 'r')
		zin.extractall(_out)
	except Exception, e:
		print str(e)
		return False
	return True

def allWithProgress(_in, _out, dp, ignore, title):
	count = 0; errors = 0; error = ''; update = 0; size = 0; excludes = []
	try:
		zin = zipfile.ZipFile(_in,  'r')
	except Exception, e:
		errors += 1; error += '%s\n' % e
		wiz.log('Error Checking Zip: %s' % str(e), xbmc.LOGERROR)
		return update, errors, error
	
	whitelist = wiz.whiteList('read')
	for item in whitelist:
		try: name, id, fold = item
		except: pass
		excludes.append(fold)
		if fold.startswith('pvr'):
			wiz.setS('pvrclient', id)
	
	nFiles = float(len(zin.namelist()))
	zipsize = wiz.convertSize(sum([item.file_size for item in zin.infolist()]))

	zipit = str(_in).replace('\\', '/').split('/')
	title = title if not title == None else zipit[-1].replace('.zip', '')

	for item in zin.infolist():
		count += 1; prog = int(count / nFiles * 100); size += item.file_size
		file = str(item.filename).split('/')
		skip = False
		line1  = ''
		line2  = '[COLOR lime]Datoteka:[/COLOR] [COLOR white]%s/%s[/COLOR] ' % (count, int(nFiles))
		line2 += '[COLOR lime]Velicina:[/COLOR] [COLOR white]%s/%s[/COLOR]' % (wiz.convertSize(size), zipsize)
		line3  = '[COLOR white]Vas[/COLOR] [COLOR lime]Balkan Green[/COLOR]'
		if item.filename == 'userdata/sources.xml' and KEEPSOURCES == 'true': skip = True
		elif item.filename == 'userdata/favourites.xml' and KEEPFAVS == 'true': skip = True
		elif item.filename == 'userdata/profiles.xml' and KEEPPROFILES == 'true': skip = True
		elif item.filename == 'userdata/advancedsettings.xml' and KEEPADVANCED == 'true': skip = True
		elif file[0] == 'addons' and file[1] in excludes: skip = True
		elif file[0] == 'userdata' and file[1] == 'addon_data' and file[2] in excludes: skip = True
		elif file[-1] in LOGFILES: skip = True
		elif file[-1] in bad_files: skip = True
		elif file[-1].endswith('.csv'): skip = True
		elif not str(item.filename).find('plugin.program.super.favourites') == -1 and KEEPSUPER == 'true': skip = True
		elif not str(item.filename).find(ADDON_ID) == -1 and ignore == None: skip = True
		if skip == True: wiz.log("Skipping: %s" % item.filename, xbmc.LOGNOTICE)
		else:
			try:
				zin.extract(item, _out)
			except Exception, e:
				errormsg  = "[COLOR lime]Datoteka:[/COLOR] [COLOR white]%s[/COLOR]\n" % (file[-1])
				errormsg += "[COLOR lime]Mapa:[/COLOR] [COLOR white]%s[/COLOR]\n" % ((item.filename).replace(file[-1],''))
				errormsg += "[COLOR lime]Greska:[/COLOR] [COLOR white]%s[/COLOR]\n\n" % (str(e).replace('\\\\','\\').replace("'%s'" % item.filename, ''))
				errors += 1; error += errormsg
				wiz.log('Error Extracting: %s(%s)' % (item.filename, str(e)), xbmc.LOGERROR)
				pass
		dp.update(prog, line1, line2, line3)
		if dp.iscanceled(): break
	if dp.iscanceled(): 
		dp.close()
		wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Extract Cancelled[/COLOR]" % COLOR2)
		sys.exit()
	return prog, errors, error