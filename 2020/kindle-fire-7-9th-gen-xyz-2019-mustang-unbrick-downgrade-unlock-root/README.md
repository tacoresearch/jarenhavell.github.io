# Kindle Fire 7 – 9th Gen (2019, mustang): xyz Root, TWRP, install Lineage 14.1

*January 1, 2020*

WARNING: THIS ARTICLE IS STILL IN PROCESS AS OF 1/1/2020.
WARNING: THIS PROJECT WAS ABANDONDED

XYZ from XDA developers was kind enough to put together a new root package / tutorial for the Kinde Fire 7 9th generation (2019 edition). All credit to [xyz](https://forum.xda-developers.com/search.php?searchid=461961171) of XDA Developers for making this all possible. Their post can be found on the [amazon fire fourms.](https://forum.xda-developers.com/amazon-fire/orig-development/fire-7-2019-mustang-unbrick-downgrade-t3944365)

The following article,  in combination with my video, will guide you through the process of unlocking your “$35” kindle fire and loading a different OS.

[Video – in process]

[Pictures]

picture –  short with tweezers – red dot to metal frame

- <https://forum.xda-developers.com/showpost.php?p=79683131&postcount=22>

[Tools]

- spare /empty USB drive
- USB cable for Kindle Fire
- computer that can boot from USB drive.
- tweezers if doing hardware unlock

Device: $35 Kindle Fire 7, 9th generation, released June 2019, nicknamed “[Mustang](https://forum.xda-developers.com/amazon-fire/help/fire-9th-gen-car-model-t4022621)” – For the [5th and 7th generation devices, see my previous post.](http://jarenhavell.com/2019/04/09/customromkindlefire7-2019/)

[Instructions – coming soon]

1. Read all instructions. Be warned thiat if you do the wrong thing, you could possibly delete all your data, break your kindle, cause a house fire, or make a small child cry, all of which coul d have been avoided if you just read the instructions. Still, proceed at your own risk.
2. Download DRBL and prepare a bootable USB disk
3. boot to linux (using USB disk, or your own linux machine)
4. download all the tools and things you will need, and unzip them.
5. On the kindle fire 7: Back up any data, **do a complete factory reset**, do **not** connect to wifi.
6. enable developer mode and USB debugging on kindle.
8. get kindle into bootrom mode

1. Hardware method:
   1. turn off. open device. unplug battery.
   2. Carefully remove metal can cover. go slow, do not pry against circuit board or else you might damage a trace / componant.
   3. with a small pair of metal tweezers, short the indicated pin to the metal frame, and then plug in the usb.
   4. run the script. (sudo ./bootrom-step.sh )
   5. Release the pin as directed.
   6. follow along

1. Software method: use mtk-su to do the thing. Careful: this will break your device… and then you fix it by installing a new OS.
   1. enable developer mode
   2. enable usb debug
   3. connect kindle to computer.
      1. On the kindle, pull down the menu, click the USB charging,  “tap for other USB options” and select PTP for “transfer photos”. Click Accept to allow permission for your computer.
   4. Open terminal on computer, navigate to the unzipped mtk-su folder.
      1. Transfer the executable to your tablet by typing:  sudo adb push arm/mtk-su /data/local/tmp”
      2. once successful, run these commands line by line.
         1. #do not copy paste.
         2. adb shell
         3. cd /data/local/temp
         4. ```
            cd /data/local/tmp

            ./mtk-su

            getenforce # Just to confirm it says Permissive

            echo 0 > /sys/block/mmcblk0boot0/force_ro

            dd if=/dev/zero of=/dev/block/mmcblk0boot0 bs=512 count=8
            ```

            #dont close this window. you will need it in a moment.
   5. open a new terminal window, and navigate to the unzipped amonet-mustang folder
      1. cd /Downloads/amonet-mustang
         1. run
            1. sudo ./bootrom-step.sh
   6. Back on the mustang” terminal run a reboot command
      1. type “reboot”.
      2. the tablet should restart, and the amonet script will begin to run.
         1. Click to continue, it will starytcopying  things. Should take about 4 minutes.
   8. Once the script finished, the kindle will restart into fastboot mode
      1. All you will see if the amazon logo. to verify that the dvice is in fastboot mode:
         1. type sudo fastboot devices
            1. it will list the device
   9. Now, back in the amonet window, start the fastboot process script to install twrp
      1. sudo ./fastboot\_step.sh
      2. the tablet will flash some text and do a few things. give it a minute or two
   10. the tablet will flash and appear to restart. let it do its thing untill the screen goes dark.
       1. tap the power button twice and TWRP will pop up.
       2. SUCCESS!
   11. TWRP (Team Win Recovery Project) is now installed and can be launched by holding down **VOL Down** (left most button from pwr) and **Power** when starting up the device.
   12. You may follow any apropriate guide for installing an applicable OS

Step 2:

Installing Lineage 14.1 on Kindle Fire 7 “mustang”  (9th gen)

1. read [instructions from Ggow on XDA](https://forum.xda-developers.com/amazon-fire/orig-development/rom-lineage-14-1-t3957329)
2. from TWRP:
   1. wipe > Format Data
   2. Swipe to reset
   3. copy the rom to the device (One does not simply copy things of course)
      1. copy the zips (Lineage / gapps / magisk)
   4. flash rom.zip
   5. flash .zip of apps
   6. reboot

Step 2.1 – Shave a few yacks.  
So, it seems that the TWRP version does not like the SD card slot on my device. I tried 2 sd cards and neither seemed to work in TWRP, even though the same cards seemed to work just fine later in the installation. So, to get around the SD card issue, we can just push the files using adb push like we did before right? yes, after getting permission from the linux overloads. We have to shave their yack for them.

This, of course, is only because you are usingdebian SID on DRB. For DRBL, We need to add a step to give you permission to connect to the device after TWRP is installed. When we were in FireOs, we simply slid down, clicked usb and changed the device to PTP mode. By default, TWRP supports MTP mode, which, of course doesn’t work “out of the box”.

This is what I did to get it working. I used this [article on askubuntu](http://Found this article https://askubuntu.com/questions/246913/insufficient-permissions-error-on-adb-push-command-on-12-04/349191) for the udev rules. Thanks to [vidarlo](https://askubuntu.com/users/653515/vidarlo) and [erjoalgo](https://askubuntu.com/users/19547/erjoalgo)

first, obtian the idVendor of the kindle.

plug the kindle in, with TWRP loaded, and mtp enabled (mount > enable MTP)

You can get the ID code from either of the following:

- sudo dmesg  
  Look for the amazon device

or

- lsusb  
  look for google Inc.

for me, the ID was **18d1**.

- Next, you need to give the”plugdev” group access to the device. You are going to create a file and then change some permissions then restart the services.
  - Create the file:

`sudo nano /etc/udev/rules.d/51-android.rules`

and type the following line:

```
SUBSYSTEM=="usb", ATTR{idVendor}=="18d1", MODE="0666", GROUP="plugdev"

```

**ctrl X** o exit, and  hit y to save.

Now assign read permissions on the files, reload udev and reload the adb daemon:

```
sudo chmod a+r /etc/udev/rules.d/51-android.rules

sudo udevadm control --reload-rules

adb kill-server

adb start-server

```

You may have to disconnect and connect again your device to the USB port.

——-

NOW you can copy the files using the adb push command, like we did before.

- navigate to where you downloaded the file, ie /Downloads/
- sudo adb push /path\_to\_lineage\_rom\_file.zip /data/local/tmp/lineage.zip
- after it finishes copying, use TWRP to install the image

After it finished installing, you can go back and do the same things for any other files, such as open gapps

Step 3-

[Downloads]

From your computer

- [DRBL](https://drbl.org/download/)

From linux pc/ or after booting up DRBL from flash drive:

- mtk-su (by XDA member [diplomatic](https://forum.xda-developers.com/search.php?searchid=461961153)), from <https://forum.xda-developers.com/android/development/amazing-temp-root-mediatek-armv8-t3922213>
- amonet-mustang.zip from [XDA post](https://forum.xda-developers.com/amazon-fire/orig-development/fire-7-2019-mustang-unbrick-downgrade-t3944365)
- finalize.zip from [XDA post](https://forum.xda-developers.com/amazon-fire/orig-development/fire-7-2019-mustang-unbrick-downgrade-t3944365)
- update-kindle-NS6312\_user\_1827\_0002517050244.bin: [https://fireos-tablet-src.s3.amazona…2517050244.bin](https://fireos-tablet-src.s3.amazonaws.com/Tr37jJbMSR96z5WBmVbW6uq32p/update-kindle-NS6312_user_1827_0002517050244.bin)
- Magisk-v19.3.zip: [https://github.com/topjohnwu/Magisk/…gisk-v19.3.zip](https://github.com/topjohnwu/Magisk/releases/download/v19.3/Magisk-v19.3.zip) or newer version from xda [topjohnwu](https://forum.xda-developers.com/apps/magisk/official-magisk-v7-universal-systemless-t3473445) on [Magisk github](https://github.com/topjohnwu/Magisk/releases)
- Optional
  - revert-stock-mustang.zip (to go back to stock) from [XDA post](https://forum.xda-developers.com/amazon-fire/orig-development/fire-7-2019-mustang-unbrick-downgrade-t3944365)
  - Lineage 14 (for Mustang: Kindle fire 7,  9th generation) <https://forum.xda-developers.com/amazon-fire/orig-development/rom-lineage-14-1-t3957329>
  - Open Google Apps <https://opengapps.org/>  (Select Arm , 7.1 , then select **stock**, or other as desired

[closing thoughts]

So, I completely missed the steps for providing a recovery back to stock kindle fire goodness.

You would need to eithre get the sd card mounted and copy files there, or push the files to a safe spot and flash the old kindle file, (as well as rooting it with magis)… I figured I should probably warn you there is no easy way to go back!
