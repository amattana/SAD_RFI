import datetime, glob, os,sys
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec
import pytz

wday = ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab", "Dom"]
b_start = 400
b_stop  = 416
bw = b_stop - b_start
bw_step = bw/10.
ytick = np.array(range(11))*bw_step
yticklab = [str(int(j+b_start)) for j in ytick]

lista = sorted(glob.glob("data/*.txt"))

gs = gridspec.GridSpec(2, 1, height_ratios=[8,1])
fig = plt.figure(figsize=(12, 8), facecolor='w')

ax1 = fig.add_subplot(gs[1])
ax2 = fig.add_subplot(gs[0])

plt.ion()

H_per_day = 24
MIN_per_hour = 60
MEAS_per_min = 6
pst = pytz.timezone('Europe/Rome')

tot_power = np.zeros(H_per_day * MIN_per_hour * MEAS_per_min)
tot_power[:] = np.nan
cnt=0

#spgramma = np.empty((360*24,1001,))
spgramma = np.empty((360*24,bw,))
spgramma[:] = np.nan

for l in lista:
    if l[-6:-4]=="00":
        tot_power = np.zeros(H_per_day * MIN_per_hour * MEAS_per_min)
        tot_power[:] = np.nan
        cnt=0
        spgramma = np.empty((360*24,bw,))
        #spgramma = np.empty((360*24,1001,))
        spgramma[:] = np.nan

    with open(l) as f:
        data=f.readlines()
    sys.stdout.write("\rProcessing date %s/%s/%s, file # %s " % (l[-13:-11],l[-11:-9],l[-9:-7],l[-6:-4]))
    sys.stdout.flush()
    for d in data:
        
        dati = d.split(" ")
        t = datetime.datetime.utcfromtimestamp(float(dati[0]))-datetime.timedelta(24107)#+datetime.timedelta(0, 3600*2)
        t=pytz.UTC.localize(t)
        t=t.astimezone(pst)
        day = datetime.datetime(t.year,t.month,t.day)
        t=t.replace(tzinfo=None)
        if float(dati[-1])>-50:
            tot_power[(t-day).seconds/10] = float(dati[-1])
        else:
            tot_power[(t-day).seconds/10] = None

        #spettro = np.array(dati[1:-1])
        spettro = np.array(dati[1+b_start:1+b_stop])
        #last, spgramma = spgramma[0], spgramma[1:]
        if np.mean(spettro.astype(np.float))<-100:
            #spettro = np.empty(1001)
            spettro = np.empty(bw)
            spettro[:] = np.nan
            spgramma = np.concatenate((spgramma,[spettro]),axis=0)
        else:
            spgramma[(t-day).seconds/10] = spettro.astype(np.float)

        cnt = cnt + 1

    if l[-6:-4]=="23":
        weekday = t.weekday()

        for i in xrange(len(spgramma)):
            if (np.isnan(spgramma[i][0]) and not i==0 and not i+1>=len(spgramma)):
                if not np.isnan(spgramma[i+1][0]):
                    spgramma[i] = spgramma[i-1]

        ax1.cla()
        ax1.plot(xrange(len(tot_power)),tot_power)
        ax1.grid(True)
        ax1.set_ylabel("dBm")
        ax1.set_xticks([0,1080,2160,3240,4320,5400,6480,7560,8640])
        ax1.set_xticklabels(["0","3","6","9","12","15","18","21","24"])
        ax1.set_ylim([-25,-5])
        ax1.set_xlim([0,len(tot_power)])
        ax1.set_yticklabels(["-25","-20","-15","-10","-5"], fontsize=10)
        ax1.set_title("Total Power", fontsize=12)

        ax2.cla()
        #ax2.imshow(np.transpose(spgramma), interpolation='none', aspect='auto', extent=[0,24,1000,0])
        ax2.imshow(np.transpose(spgramma), interpolation='none', aspect='auto', extent=[0,24,bw,0])
        #ax2.set_yticks([0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
        #ax2.set_yticklabels(["0", "100", "200", "300", "400", "500", "600", "700", "800", "900", "1000"])
        ax2.set_yticks(ytick)
        ax2.set_yticklabels(yticklab)
        ax2.set_xticks([0, 3, 6, 9, 12, 15, 18, 21, 24])
        ax2.set_xticklabels(["0", "3", "6", "9", "12", "15", "18", "21", "24"])
        ax1.set_xlabel("Time (hour)",fontsize=10)
        ax2.set_ylabel('MHz')
        ax2.set_title("Spectrogram of "+datetime.datetime.strftime(t,"%Y-%m-%d"))
        plt.tight_layout()

        if not os.path.isdir("data/daily_band_"+str(b_start)+"-"+str(b_stop)):
            os.makedirs("data/daily_band_"+str(b_start)+"-"+str(b_stop))
        fig.savefig("data/daily_band_"+str(b_start)+"-"+str(b_stop)+"/SAD_RFI_band_"+str(b_start)+"-"+str(b_stop)+"_"+datetime.datetime.strftime(t,"%Y-%m-%d")+".png")
        sys.stdout.write("\rSaved daily image: " + "data/daily_band_"+str(b_start)+"-"+str(b_stop)+"/SAD_RFI_band_"+str(b_start)+"-"+str(b_stop)+"_"+datetime.datetime.strftime(t,"%Y-%m-%d")+".png\n")
        sys.stdout.flush()

ax1.cla()
ax1.plot(xrange(len(tot_power)),tot_power)
ax1.grid(True)
ax1.set_ylabel("dBm")
ax1.set_xticks([0,1080,2160,3240,4320,5400,6480,7560,8640])
ax1.set_xticklabels(["0","3","6","9","12","15","18","21","24"])
ax1.set_ylim([-25,-5])
ax1.set_xlim([0,len(tot_power)])
ax1.set_yticklabels(["-25","-20","-15","-10","-5"], fontsize=10)
ax1.set_title("Total Power", fontsize=12)

ax2.cla()
#ax2.imshow(np.transpose(spgramma), interpolation='none', aspect='auto', extent=[0,24,1000,0])
#ax2.set_yticks([0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
#ax2.set_yticklabels(["0", "100", "200", "300", "400", "500", "600", "700", "800", "900", "1000"])
ax2.imshow(np.transpose(spgramma), interpolation='none', aspect='auto', extent=[0,24,bw,0])
ax2.set_yticks(ytick)
ax2.set_yticklabels(yticklab)
ax2.set_xticks([0, 3, 6, 9, 12, 15, 18, 21, 24])
ax2.set_xticklabels(["0", "3", "6", "9", "12", "15", "18", "21", "24"])
ax1.set_xlabel("Time (hour)",fontsize=10)
ax2.set_ylabel('MHz')
ax2.set_title("Spectrogram of "+datetime.datetime.strftime(t,"%Y-%m-%d"))
plt.tight_layout()

if not os.path.isdir("data/daily_band_" + str(b_start) + "-" + str(b_stop)):
    os.makedirs("data/daily_band_" + str(b_start) + "-" + str(b_stop))
fig.savefig("data/daily_band_" + str(b_start) + "-" + str(b_stop) + "/SAD_RFI_band_" + str(b_start) + "-" + str(b_stop) + "_" + datetime.datetime.strftime(t, "%Y-%m-%d") + ".png")
sys.stdout.write("\rSaved daily image: " + "data/daily_band_" + str(b_start) + "-" + str(b_stop) + "/SAD_RFI_band_" + str(b_start) + "-" + str(b_stop) + "_" + datetime.datetime.strftime(t, "%Y-%m-%d") + ".png\n")
sys.stdout.flush()

print "\nExecution terminated!\n"

        
