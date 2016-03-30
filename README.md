# MunkiGenericIcons
Copies a generic icon to Munki items with no icons

## Rationale
Munki actually already has its own generic icon. If you go to **/Applications/Managed Software Center.app/Contents/Resources/WebResources/** on a Munki client, you'll see a **Generic.png** file that looks like a translucent yellow cube coming out of a cardboard box. When a user opens up Managed Software Center, MSC will check in with your Munki server to see for each item whether it has a corresponding icon or not. If it has no specified icon, MSC will use the Generic.png file.

For most people, that may be fine.

If you run `/usr/local/munki/managedsoftwareupdate -vvv`, you'll see a bunch of 404 errors when checking for icons that don't exist, though. Maybe you don't want those 404 errors. Or maybe you'd prefer to have your own "Generic" icon associated with certain items that wouldn't ordinarily have an icon (e.g., a nopkg or a custom .pkg).

Whatever your reasons, if you just want to make sure all your Munki items have corresponding icons, that's what Munki Generic Icons (MGI) is for.

## How to Install MGI
Download the files from this project to your Munki server and then copy the **MunkiGenericIcons.py** file to **/usr/local/mgi/** and make sure it's executable. For example:

`sudo mkdir -p /usr/local/mgi`

`sudo cp ~/Downloads/MunkiGenericIcons-master/MunkiGenericIcons.py /usr/local/mgi`

`sudo chmod +x /usr/local/mgi/MunkiGenericIcons.py`

## How to Use MGI
MGI is looking for an icon in your icons subfolder called **Generic.png**, so you have to have a generic icon ready to go. It should be square (50 x 50, or 70 x 70, or 220 x 220) and it should be a .png file. If your Munki repo is in /Users/Shared/munki_repo/, then your icon would be at /Users/Shared/munki_repo/icons/Generic.png.

MGI will not work as expected if you have an actual Munki item named *Generic* that needs its own icon. If that's the case, you'll have to modify the MGI script directly and change `generic_name="Generic.png"` line to reflect the icon you really want to be the generic icon (maybe call it *Generic1.png* or something).

When you run `/usr/local/mgi/MunkiGenericIcons.py`, the script will check for all the directories to exist (your Munki repository, the pkgsinfo and icons subdirectories), check that your generic icon exists, cycle through all the pkgsinfo files to check each one for an icon. If there isn't an icon, MGI will copy the Generic.png icon to be the previously missing icon.
