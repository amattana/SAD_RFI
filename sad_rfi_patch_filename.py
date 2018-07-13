import os,glob

print "\n\nThis software will patch the filenames of SAD RFI Data from DDMMYYYY to YYYYMMDD"
a=glob.glob("].txt")
print "\n\nReading directory..."

for f in a:
    print "Changing file: ",f," to "+f[:4]+f[8:12]+f[6:8]+f[4:6]+f[12:]+ "...",
    os.system("mv "+f+" "+f[:4]+f[8:12]+f[6:8]+f[4:6]+f[12:])
    print "done!"

print "\nExecution terminated."


