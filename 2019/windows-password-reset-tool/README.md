# Windows password reset tool

*March 11, 2019*

Windows password reset tool

This bootable USB tool allows you to reset the local administrator password on a windows system. It is easy to use and can be very helpful for that old computer that has been in the closet for 10 years.

[Video: https://www.youtube.com/watch?v=oq9iJWwH33c]

Offline Windows Password & Registry Editor, usb Bootdisk or CD. This is a free software project maintained by Petter Nordahl-Hagen. (*also called:**Ntpasswd*  
*and chntpw)*

**Downloads**

- Download the bootable ISO file [cd140201](http://pogostick.net/~pnh/ntpasswd/cd140201.zip) (ZIP) from Pogostick, or find the CD version from the  PogoStick Download page at <http://pogostick.net/~pnh/ntpasswd/>or <http://www.chntpw.com/download/>
- Download Rufus USB tool : <https://rufus.ie/>

**Bootable USB (or CD) instructions:**

You want to create a bootable USB drive.

1. 1. Download the Bootable “CD” \*version, as you will use Rufus to “burn” this cd iso to a usb flash drive.
   2. Extract the .zip file.The **.iso image** is inside the .zip.
      1. \*Even though there is a USB version, it is not the one you need. The USB version is for making the tool work on an existing bootable flash drive. you probably have a blank USB drive and just want to reset a password. **Use the CD Version.**
   3. Use Rufus  tool  to copy the .ISO to your USB drive. 
      1. Insert a spare, blank USB drive into your computer, and use RUFUS to turn it into a bootable disk.
         1. ***!!!!** This will erase everything on the usb drive. It is a good idea to unplug any external hard drives before you use this tool, as you do not want to accidentally pick the wrong drive.**!!!***
            1. ![Rufus 3.4.1430 (Portable) Drive Properties Device FD-SETUP [512 MB] 800t selection Password Reset Tool cdl 40201 .iso Partition scheme M8R v Show advanced drive properties Format Options Volume label chntpw 140201 File system FAT32 v Show advanced format options Status Target system BIOS (or UEFI-CSM) Cluster size 4096 bytes (Default) READY START Using image: Password Reset Tool cd140201 .iso CLOSE ](images/embedded-1.png)
               1. Click start and wait for it to finish before removing disk,

4. Insert the disk into the locked windows computer. Boot from the USB drive (may have to hit F1, F10, or F12, etc to get to the boot menu

5. Follow the prompts, [read the authors FAQ page](https://pogostick.net/~pnh/ntpasswd/) or watch my video above for instructions.
