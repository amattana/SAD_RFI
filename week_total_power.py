import datetime, glob, os
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec
import pytz

wday = ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab", "Dom"]

lista = sorted(glob.glob("data/*.txt"))

ax = [[]]
ax = ax*7
dx = [[]]
dx = dx*7

gs = gridspec.GridSpec(7, 2, width_ratios=[1,10], height_ratios=[1, 1, 1, 1, 1, 1, 1])
fig = plt.figure(figsize=(9, 12), facecolor='w')

plt.ion()

for i in xrange(len(ax)):
    dx[i] = fig.add_subplot(gs[i*2])
    dx[i].plot(range(10),color='w')
    dx[i].set_axis_off()
    dx[i].annotate(wday[i],(1,4.5),fontsize=16)
    #dx[i].annotate("16/04/2017",(1,2.5),fontsize=10)

    ax[i] = fig.add_subplot(gs[i*2+1])
    ax[i].grid(True)
    ax[i].set_xticks([0,1080,2160,3240,4320,5400,6480,7560,8640])
    ax[i].set_xticklabels(["0","3","6","9","12","15","18","21","24"])
    ax[i].set_xlim([0,8640])
    ax[i].set_ylim([-25,-5])

ax[0].set_title("Weekly Total Power (dBm/hours)")
plt.tight_layout()

H_per_day = 24
MIN_per_hour = 60
MEAS_per_min = 6
pst = pytz.timezone('Europe/Rome')

x = np.zeros(H_per_day * MIN_per_hour * MEAS_per_min)
x += H_per_day * MIN_per_hour * MEAS_per_min
tot_power = np.zeros(H_per_day * MIN_per_hour * MEAS_per_min)
tot_power -= 100
cnt=0

for l in lista:
    if l[-6:-4]=="00":
        x = np.zeros(H_per_day * MIN_per_hour * MEAS_per_min)
        x += H_per_day * MIN_per_hour * MEAS_per_min
        tot_power = np.zeros(H_per_day * MIN_per_hour * MEAS_per_min)
        tot_power -= 100 
        cnt=0
        print "Starting new day..."

    with open(l) as f:
        data=f.readlines()
    #print "Generating images for file: ",l
    for d in data:
        
        dati = d.split(" ")
        t = datetime.datetime.utcfromtimestamp(float(dati[0]))-datetime.timedelta(24107)#+datetime.timedelta(0, 3600*2)
        t=pytz.UTC.localize(t)
        t=t.astimezone(pst)
        day = datetime.datetime(t.year,t.month,t.day)
        t=t.replace(tzinfo=None)
        x[cnt] = (t-day).seconds/10 
        if float(dati[-1])>-50:
            tot_power[cnt] = float(dati[-1])
        else:
            tot_power[cnt] = None

        cnt = cnt + 1

    if l[-6:-4]=="23":
        weekday = t.weekday()

        dx[weekday].cla()
        dx[weekday].plot(range(10),color='w')
        dx[weekday].set_axis_off()
        dx[weekday].annotate(wday[weekday],(1,4.5),fontsize=16) 
        dx[weekday].annotate(datetime.datetime.strftime(t,"%d/%m/%Y"),(1,2.5),fontsize=10)

        ax[weekday].cla()
        ax[weekday].plot(x[:cnt],tot_power[:cnt])
        ax[weekday].grid(True)
        ax[weekday].set_xticks([0,1080,2160,3240,4320,5400,6480,7560,8640])
        ax[weekday].set_xticklabels(["0","3","6","9","12","15","18","21","24"])
        ax[weekday].set_xlim([0,8640])
        ax[weekday].set_ylim([-25,-5])

        if weekday == 6:        
            ax[0].set_title("Weekly Total Power (dBm/hours)")
            plt.tight_layout()
            weeknumber="%02d"%(day.isocalendar()[1])
            if not os.path.isdir("data/weekly"):
                os.makedirs("data/weekly")
            fig.savefig("data/weekly/SAD_RFI_2018_WEEK-"+weeknumber+".png")
            print "\n\nSaved week image: "+"data/weekly/SAD_RFI_2018_WEEK-"+weeknumber+".png\n"

            for i in xrange(len(ax)):
                dx[i].cla()
                dx[i].plot(range(10),color='w')
                dx[i].set_axis_off()
                dx[i].annotate(wday[i],(1,4.5),fontsize=16)

                ax[i].cla()
                ax[i].grid(True)
                ax[i].set_xticks([0,1080,2160,3240,4320,5400,6480,7560,8640])
                ax[i].set_xticklabels(["0","3","6","9","12","15","18","21","24"])
                ax[i].set_xlim([0,8640])
                ax[i].set_ylim([-25,-5])


ax[0].set_title("Weekly Total Power (dBm/hours)")
plt.tight_layout()
weeknumber="%02d"%(day.isocalendar()[1])
if not os.path.isdir("data/weekly"):
    os.makedirs("data/weekly")
fig.savefig("data/weekly/SAD_RFI_2018_WEEK-"+weeknumber+".png")
print "\n\nSaved week image: "+"data/weekly/SAD_RFI_2018_WEEK-"+weeknumber+".png\n"
    

print "\nExecution terminated!\n"

        
