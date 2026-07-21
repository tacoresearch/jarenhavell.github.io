# Hey Linux, What wireless card do I have?

*February 17, 2018*

I was curious what wireless card I had in my Thinkpad T540p. I have Debian 9 installed on it.  
  
A quick search reveled an [ubuntu forum post](https://ubuntuforums.org/showthread.php?t=1422475) that provided some terminal commands for listing various hardware.

|  |  |
| --- | --- |
| List hardware: | lspci |

![](images/021718_2010_HeyLinuxWha1-6.png)

Adding a pipe (|) and grep command with “Wireless” as the filter yields the following

|  |  |
| --- | --- |
| To determine wireless card | lspci | grep Wireless |

Capitalization is important- w vs W

![](images/021718_2010_HeyLinuxWha2-6.png)

There we go.

![](images/021718_2010_HeyLinuxWha3-6.png)

My T540p has an Intel Wireless 7260

Ok, great… but I am curious what else my system has. Specifically, I would like to know some more specifics.

There is a tool called [lshw](https://ezix.org/project/wiki/HardwareLiSter) we can install that will reveal much more information.

|  |  |
| --- | --- |
| List hw | lshw |

Hmm looks like it needs to be installed.

![](images/021718_2010_HeyLinuxWha4-6.png)

|  |  |
| --- | --- |
| Install lshw | Sudo apt-get install lshw |

![](images/021718_2010_HeyLinuxWha5-6.png)

Try it again-

|  |  |
| --- | --- |
| List hardware | lshw |

Wow, information overload. And a note at the end saying I should run this as admin.

![](images/021718_2010_HeyLinuxWha6-5.png)

…

![](images/021718_2010_HeyLinuxWha7-6.png)

|  |  |
| --- | --- |
| List hardware as root user | Sudo lshw |

Jonny five just called: More Input! More input!

Interesting

![](images/021718_2010_HeyLinuxWha9-6.png)

Very interesting

![](images/021718_2010_HeyLinuxWha10-6.png)

Running a bad command yields a bevy of options, including a “-sanitize” command that removes sensitive information.

![](images/021718_2010_HeyLinuxWha11-6.png)

Useful for when posting online.

![](images/021718_2010_HeyLinuxWha12-5.png)

Apparently there is also a graphical version of this. We need to install the package

|  |  |
| --- | --- |
| Install list hardware graphical | Sudo apt-get install lshw-gtk |

![](images/021718_2010_HeyLinuxWha13-6.png)

|  |  |
| --- | --- |
| List hardware in graphical mode | lshw-gtk |

![](images/021718_2010_HeyLinuxWha14-6.png)

Let’s try it anyway: Execute!

Hmmm

Refresh button

![](images/021718_2010_HeyLinuxWha16-6.png)

Double click to start exploring

![](images/021718_2010_HeyLinuxWha17-6.png)

Way more information!

![](images/021718_2010_HeyLinuxWha18-6.png)
