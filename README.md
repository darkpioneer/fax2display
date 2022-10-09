# fax2display
Scripts for taking a fax from an asterisk server and sending it to a computer to display on a large screen

fax2display.py uses sftp to transfer a file across a remote dir on another computer, in my case a raspberry pi.
to display on the raspberry pi i used feh with the --reload option along with --full-screen and --slideshow-delay to 
refresh every n seconds.

# Requirements

You need python3 with pysftp and the libtiff-tools and poppler-utils packages.

## Usage

fax2display.py [Path to PDF]

## Gotchas

make sure you have sftp'd to the client machine from the asterisk user to add the machine to the known_hosts lists of the asterisk user

## Asterisk Config

[fax-display]
exten => s,1,Noop("Receiving FAX")
same => n,Answer()
same => n,Set(FAXDEST=/tmp/faxes)
same => n,Set(FAXNAME=${STRFTIME(,,%C%y%m%d%H%M)})
same => n,Set(FAXPATH=${FAXDEST}${FAXNAME})
same => n,ReceiveFax(${FAXPATH}.tif)
same => n,Noop(Converting tif to pdf)
same => n,Set(TIFF2PDF=${SHELL(tiff2pdf ${FAXPATH}.tif -o ${FAXPATH}.pdf)})
same => n,Noop(Sending fax to display)
same => n,Noop(PDF Path: ${FAXPATH}.pdf)
same => n,Set(FAX2DISPLAY=${SHELL(python3 -u /var/lib/asterisk/bin/fax2display.py ${FAXPATH}.pdf >> /tmp/log)})
same => n,Noop(Deleting old file)
same => n,Set(DELETE=${SHELL(rm ${FAXPATH}*)})
same => n,Wait(30)
same => n,Hangup()

# License

Released under the MIT license. See the LICENSE file.
