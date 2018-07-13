import datetime, glob, os
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec
import pytz


lista = sorted(glob.glob("data/*.txt"))

fig = plt.figure(figsize=(14, 8))
gs = gridspec.GridSpec(3, 1,
                       #width_ratios=[1],
                       height_ratios=[3, 1, 1]
                       )


ax1 = fig.add_subplot(gs[0])
ax3 = fig.add_subplot(gs[1])
ax2 = fig.add_subplot(gs[2])

plt.tight_layout()
plt.ion()

H_per_day = 24
MIN_per_hour = 60
MEAS_per_min = 6
pst = pytz.timezone('Europe/Rome')

x = np.zeros(H_per_day * MIN_per_hour * MEAS_per_min)
x += H_per_day * MIN_per_hour * MEAS_per_min
tot_power = np.zeros(H_per_day * MIN_per_hour * MEAS_per_min)
tot_power -= 100
cnt=0
spgramma = np.empty((360,1001,))
spgramma[:] = np.nan


for l in lista:
    if l[-6:-4]=="00":
        x = np.zeros(H_per_day * MIN_per_hour * MEAS_per_min)
        x += H_per_day * MIN_per_hour * MEAS_per_min
        tot_power = np.zeros(H_per_day * MIN_per_hour * MEAS_per_min)
        tot_power -= 100 
        cnt=0
        spgramma = np.empty((360,1001,))
        spgramma[:] = np.nan
        print "\n\nStarting new day...\n"

    with open(l) as f:
        data=f.readlines()
    print "Generating images for file: ",l
    for d in data:
        
        dati = d.split(" ")
        t = datetime.datetime.utcfromtimestamp(float(dati[0]))-datetime.timedelta(24107)#+datetime.timedelta(0, 3600*2)
        t=pytz.UTC.localize(t)
        t=t.astimezone(pst)
        day = datetime.datetime(t.year,t.month,t.day)
        t=t.replace(tzinfo=None)
        x[cnt] = (t-day).seconds/10 
        tot_power[cnt] = float(dati[-1])
        spettro = np.array(dati[1:-1])
        last, spgramma = spgramma[0], spgramma[1:] 
        if np.mean(spettro.astype(np.float))<-100:
            spettro = np.empty(1001)
            spettro[:] = np.nan
            spgramma = np.concatenate((spgramma,[spettro]),axis=0)
        else:
            spgramma = np.concatenate((spgramma,[spettro.astype(np.float)]),axis=0)
        
        #print spgramma,len(spgramma)
        ax1.cla()
        #if len(spgramma)>1:
        ax1.imshow(spgramma, interpolation='none', aspect='auto', extent=[10,1010,60,0])
        ax1.set_ylabel("Time (minutes)")
        ax1.set_xlabel('MHz')
        ax1.set_title("Spectrogram")

        ax3.cla()
        ax3.plot(dati[1:-1])
        ax3.set_ylim([-100,0])
        title = datetime.datetime.strftime(t,"%Y/%m/%d %H:%M:%S")#+"  -  Timestamp:"+str(float(dati[0]))+"  -  Total Power: "+str(float(dati[-1]))
        ax3.set_title(title)
        title = datetime.datetime.strftime(t,"%Y%m%d_%H%M%S")
        ax3.grid(True)
        ax3.set_xlabel('MHz')
        ax3.set_ylabel("dBm")

        ax2.cla()
        ax2.plot(x[:cnt],tot_power[:cnt])
        ax2.set_ylim([-20,-10])
        ax2.set_xlim([0,H_per_day * MIN_per_hour * MEAS_per_min])
        ax2.set_title("Total Power")
        ax2.set_ylabel("dBm")
        ax2.grid(True)
        ax2.set_xlabel("Day Time")
        ax2.set_xticks([0,1080,2160,3240,4320,5400,6480,7560,8640])
        ax2.set_xticklabels(["0","3","6","9","12","15","18","21","24"])
        plt.tight_layout()
        
        if not os.path.isdir("data/img/"+title[:8]):
            os.makedirs("data/img/"+title[:8])
        fig.savefig("data/img/"+title[:8]+"/"+title+".png")
        cnt = cnt + 1

print "\nExecution terminated!\n"

        
