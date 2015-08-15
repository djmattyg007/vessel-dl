vessel-dl

This is a script to obtain direct download links for videos on Vessel so that
you can watch them in the video playback software of your choice, or save them
for viewing at a later date. You need an account on the Vessel website to make
use of this script.


Examples

Some examples of how to use the script:

vessel-dl --url https://www.vessel.com/videos/ABCDEFGH --username username

vessel-dl --url https://www.vessel.com/videos/IJKLMNOP --usertoken "LONG-STRING-OF-CHARACTERS"

vessel-dl --videoid 123456789 --usertoken "LONG-STRING-OF-CHARACTERS"

An example of the output of the script:

User Token: LONG-STRING-OF-CHARACTERS
Video ID: 123456789
mp4-216-250K: https://streams.vessel-static.com/98765432123456789/mp4-216-250K-12345654321.mp4?token=012ab345cd678ef&nva=20150815114442&v=2
mp4-360-500K: https://streams.vessel-static.com/98765432123456789/mp4-360-500K-12345654321.mp4?token=987fe654dc321ba&nva=20150815114442&v=2
mp4-480-1000K: https://streams.vessel-static.com/98765432123456789/mp4-480-1000K-12345654321.mp4?token=135ad792be468cf&nva=20150815114442&v=2
mp4-720-2400K: https://streams.vessel-static.com/98765432123456789/mp4-720-2400K-12345654321.mp4?token=2468abc1357def&nva=20150815114442&v=2
mp4-1080-4800K: https://streams.vessel-static.com/98765432123456789/mp4-1080-4800K-12345654321.mp4?token=0987abcdef1234&nva=20150815114442&v=2


Usage details

The script must autheticate you with the Vessel API. If you have previously
authenticated, you can pass the script your "User Token" with the --usertoken
flag. If you don't have a User Token, you can obtain one by authenticating (see
below). The script will print your User Token after successful authentication
so that you can use it for subsequent requests. I highly recommend saving your
User Token. It speeds up the script (one less HTTP request), and it more
closely mimics what is happening when watching videos in the browser.
Currently the User Token is not cached anywhere, so you must track it yourself.

If you don't have a User Token, you must authenticate with the API. This is
done by passing your Username to the script with the --username flag. You can
also provide your password with --password, but this is insecure as it can
result in your password being saved into your shell's command history file.
The script will prompt you for your password if you do not pass it on the
command line.

The other required part of the equation is the video ID. This is used to query
the API for the download URLs. If you know the video ID already, you can pass
it to the script with --videoid. If you don't know the video ID, just pass
the script the URL of the individual video page with --url. The script will
download the HTML and find the video ID automatically.


Packages

You can find packages for vessel-dl at the following locations:

- Arch User Repository: https://aur.archlinux.org/packages/vessel-dl/


Disclaimers

I take no responsibility for any actions that Vessel may take against your
account as a result of using this script.
This program is released into the public domain without any warranty.
