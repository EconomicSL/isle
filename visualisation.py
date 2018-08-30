# file to visualise agent-level data per timestep

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# read in data for each agent for each timestep
    # read in insurancefirm data
rfile = open("data/insurance_firms_cash.dat","r")
insurance_firms_cash = [eval(k) for k in rfile]
rfile.close()
    # read in reinsurancefirm data
rfile = open("data/reinsurance_firms_cash.dat","r")
reinsurance_firms_cash = [eval(k) for k in rfile]
rfile.close()

insurance_firms_cash = np.array(insurance_firms_cash)
reinsurance_firms_cash = np.array(reinsurance_firms_cash)

# shape (runs, steps)

# let's look at only the first run
first_run_insurance = insurance_firms_cash[0][:]
first_run_reinsurance = reinsurance_firms_cash[0][:]

class InsuranceFirmAnimation(object):
    '''class takes in a run of insurance data and produces animations '''
    def __init__(self, data):
        self.data = data
        self.fig, self.ax = plt.subplots()
        self.stream = self.data_stream()
        self.ani = animation.FuncAnimation(self.fig, self.update, repeat=False, interval=40,
                                           init_func=self.setup_plot)

    def setup_plot(self):
        """Initial drawing of the plots."""
        casharr,idarr = next(self.stream)
        self.pie = self.ax.pie(casharr, labels=idarr,autopct='%1.0f%%')
        return self.pie,

    def data_stream(self):
        for timestep in self.data:
            casharr = []
            idarr = []
            for (cash, id, operational) in timestep:
                if operational:
                    casharr.append(cash)
                    idarr.append(id)
            yield casharr,idarr

    def update(self, i):
        self.ax.clear()
        self.ax.axis('equal')
        casharr,idarr = next(self.stream)
        self.pie = self.ax.pie(casharr, labels=idarr,autopct='%1.0f%%')
        self.ax.set_title("Timestep : {:,.0f} | Total cash : {:,.0f}".format(i,sum(casharr)))
        return self.pie,

    def save(self,filename):
        self.ani.save(filename, writer='ffmpeg', dpi=80)

    def show(self):
        plt.show()
        
anim1 = InsuranceFirmAnimation(first_run_insurance)
anim2 = InsuranceFirmAnimation(first_run_reinsurance)
#anim1.save("insurance.mp4")
#anim2.save("reinsurance.mp4")
plt.show()