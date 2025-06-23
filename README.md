# autogrammetry

Software used by my device for data acquisition for 3D reconstruction with photogrammetry.

## Dependencies

Package 'PyExifTool' included in requirements.txt requires the CLI package 'exiftool'. Install instructions can be found on https://pypi.org/project/PyExifTool:

"For PyExifTool to function, exiftool command-line tool must exist on the system. If exiftool is not on the PATH, you can specify the full pathname to it by using ExifTool(executable=<full path>).

PyExifTool requires a minimum version of 12.15 (which was the first production version of exiftool featuring the options to allow exit status checks used in conjuction with -echo3 and -echo4 parameters).

To check your exiftool version:

exiftool -ver
Windows/Mac
Windows/Mac users can download the latest version of exiftool:

https://exiftool.org
Linux
Most current Linux distributions have a package which will install exiftool. Unfortunately, some do not have the minimum required version, in which case you will have to build from source.

Ubuntu

sudo apt install libimage-exiftool-perl
CentOS/RHEL

yum install perl-Image-ExifTool"