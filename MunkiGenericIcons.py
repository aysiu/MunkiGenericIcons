#!/usr/bin/python

######
## Created by aysiu (2016)
## Apache license
######

import os
import plistlib
from shutil import copyfile
import sys

# If you are hosting Munki on a Linux or Windows server, put your Munki path here. Otherwise, leave blank
MUNKI_ROOT_PATH=''

# Define the name of the generic icon to copy. In all likelihood, you won't have to change this value unless you have an item in your repositories called "Generic"
generic_name="Generic.png"

# Define likely subdirectories
pkgsinfo_sub="pkgsinfo"
icons_sub="icons"

def main():

   if not MUNKI_ROOT_PATH:
      # Find the path to the Munki repository
      munkiimport_prefs_location=os.path.join(os.getenv("HOME"), "Library/Preferences/com.googlecode.munki.munkiimport.plist")
      if os.path.exists(munkiimport_prefs_location):
         munkiimport_prefs=plistlib.readPlist(munkiimport_prefs_location)
         MUNKI_ROOT_PATH=munkiimport_prefs['repo_path']
      else:
         print "Cannot determine the Munki repo path. Be sure to run /usr/local/munki/munkiimport --configure to set the path for your user."
         sys.exit(1)
   if os.path.exists(MUNKI_ROOT_PATH):
      print "Munki repo path exists at %s. Set to proceed..." % MUNKI_ROOT_PATH
   else:
      print "Munki repo does not appear to exist at %s" % MUNKI_ROOT_PATH
      sys.exit(1)

   # Create full paths for subdirectories
   pkgsinfo_path=os.path.join(MUNKI_ROOT_PATH, pkgsinfo_sub)
   icons_path=os.path.join(MUNKI_ROOT_PATH, icons_sub)
   generic_path=os.path.join(icons_path, generic_name)

   if not os.path.exists(pkgsinfo_path):
      print "pkgsinfo folder does not exist in Munki repo"
      sys.exit(1)

   if not os.path.exists(icons_path):
      print "icons folder does not exist in Munki repo"
      sys.exit(1)
   else:
      if not os.access(icons_path, os.W_OK):
         print "The icons folder is not writable by your user."
         sys.exit(1)

   if not os.path.exists(generic_path):
      print "%s does not exist. Be sure to create a Generic.png and put it in your %s folder." % (generic_path, icons_path)
      sys.exit(1)

   # Set up a test variable
   any_missing='';

   # Walk through each of the pkgsinfo files
   for root, dirs, files in os.walk(pkgsinfo_path):
      for dir in dirs:
         # Skip directories starting with a period
         if dir.startswith("."):
            dirs.remove(dir)
         for file in files:
            # Skip files that start with a period
            if file.startswith("."):
               continue
            fullfile = os.path.join(root, file)
            plist = plistlib.readPlist(fullfile)
            plistname = plist['name'] + ".png"
            
            # See if the name already has an icon
            icon_check=os.path.join(icons_path, plistname)
            if not os.path.exists(icon_check):
               print "There is no icon for %s. Copying the generic one." % plistname
               copyfile(generic_path, icon_check)
               if not any_missing:
                  any_missing='Yes'
   if not any_missing:
      print "Congratulations! All your Munki items have icons already."

if __name__ == '__main__':
   main()
