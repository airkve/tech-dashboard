#! python3
# TechHub.py - Hub made to improve the daily work of the support guy.
# Author: Richard Jimenez
# 2016/08/28

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.simpledialog as td
import datetime
import psutil
import time
import socket
import winsound


class TechHud():
    """docstring for TechHub."""

    def __init__(self, master):
        """Docstring for Init."""
        self.host = '8.8.8.8'
        self.port = 53
        self.timeout = 1
        self.master = master
        master.title("TechHud")
        master.minsize(width=800, height=640)
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        self.mainFrame = ttk.Frame(master)
        self.mainFrame.pack(side='top', fill='both', expand=True)

        self.ThClock()
        self.compStats()
        self.workTime()
        self.internet()
        self.monSrv()
        self.netDisc()
        master.after(1000, self.refresh)

    def ThClock(self):
        """Docstring ThClock."""
        # Clock frame
        self.clockFrame = ttk.LabelFrame(self.mainFrame, text='Date and Time')
        self.clockFrame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        self.varTime = tk.StringVar()
        # Time label
        self.timeLabel = ttk.Label(self.clockFrame, textvariable=self.varTime,
                                   font='curier 20 bold')
        self.timeLabel.grid(row=0, column=0, padx=5, pady=5)
        self.varDate = tk.StringVar()
        # Date label
        self.dateLabel = ttk.Label(self.clockFrame, textvariable=self.varDate)
        self.dateLabel.grid(row=1, column=0, padx=5, pady=5)

    def compStats(self):
        """Docstring of compStats."""
        # Status bars frame
        self.statsFrame = ttk.LabelFrame(self.mainFrame, text='Computer Stats')
        self.statsFrame.grid(row=0, column=1, padx=5, pady=5)
        # CPU meter
        tk.Label(self.statsFrame, text='CPU',
                 font='curier 7').grid(row=0, column=0, sticky='W', padx=5)
        self.statBarCpu = ttk.Progressbar(self.statsFrame, orient='horizontal',
                                          length=100, mode='determinate')
        self.statBarCpu.grid(row=1, column=0, padx=5, pady=1)
        self.statBarCpu['value'] = 0
        self.statBarCpu['maximum'] = 10
        # Ram meter
        tk.Label(self.statsFrame, text='RAM',
                 font='curier 7').grid(row=2, column=0, sticky='W', padx=5)
        self.statBarRam = ttk.Progressbar(self.statsFrame, orient='horizontal',
                                          length=100, mode='determinate')
        self.statBarRam.grid(row=3, column=0, padx=5, pady=1)
        self.statBarRam['value'] = 0
        self.statBarRam['maximum'] = 100
        # HDD meter
        tk.Label(self.statsFrame, text='HDD',
                 font='curier 7').grid(row=4, column=0, sticky='W', padx=5)
        self.statBarHDD = ttk.Progressbar(self.statsFrame, orient='horizontal',
                                          length=100, mode='determinate')
        self.statBarHDD.grid(row=5, column=0, padx=5, pady=1)
        self.statBarHDD['value'] = 0
        self.statBarHDD['maximum'] = 100
        self.endHdd = psutil.disk_io_counters()

    def workTime(self):
        """Docstring of workTime."""
        self.wtFrame = ttk.LabelFrame(self.mainFrame, text='Work log')
        self.wtFrame.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)
        tk.Label(self.wtFrame, text='Worked time:',
                 font='currier 7').grid(row=0, column=0, sticky='nsew')
        self.varWt = tk.StringVar()
        self.varWt.set('00:00')
        self.wtLabel = ttk.Label(self.wtFrame, textvariable=self.varWt,
                                 font='curier 20 bold')
        self.wtLabel.grid(row=1, column=0, sticky='N', padx=5)
        tk.Label(self.wtFrame, text='Cost per hour:',
                 font='currier 7').grid(row=2, column=0, sticky='nsew')

    def internet(self):
        """Docstring for internet."""
        # Conectivity frame
        self.intFrame = ttk.LabelFrame(self.mainFrame, text='Conectivity')
        self.intFrame.grid(row=0, column=3, sticky='nsew', padx=5, pady=5)
        # Internet activity button
        self.varInter = tk.StringVar()
        self.varInter.set('------')
        self.intBtn = tk.Label(self.intFrame, textvariable=self.varInter)
        self.intBtn.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        self.intBtn['fg'] = 'white'
        self.intBtn['bg'] = 'grey'
        self.srvMon1 = tk.Button(self.intFrame, text='Server 1',
                                 command=self.setSrv1)
        self.srvMon1.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        self.srvMon1['bg'] = 'grey'
        self.srvMon2 = tk.Button(self.intFrame, text='Server 2')
        self.srvMon2.grid(row=2, column=0, sticky='nsew', padx=5, pady=5)
        self.srvMon2['bg'] = 'grey'

    def setSrv1(self):
        self.server = td.askstring('Change input', 'Enter server name/IP:')
        self.srvMon1['text'] = self.server
        self.srvMon1['bg'] = 'green'
        return self.server

    def monSrv(self):
        pass

    def netDisc(self):
        pass

    def refresh(self):
        # Time
        self.varTime.set(datetime.datetime.now().strftime("%I:%M:%S %p"))
        self.varDate.set(datetime.datetime.now().strftime("%A, %m/%Y"))
        # Status bars
        self.mem = psutil.virtual_memory()
        self.startHdd = psutil.disk_io_counters()
        self.media = self.endHdd[1] - self.startHdd[1]
        self.statBarCpu['value'] = int(psutil.cpu_percent())
        self.statBarRam['value'] = int(self.mem[2])
        self.statBarHDD['value'] = abs(self.media)
        # Internet probe
        try:
            socket.setdefaulttimeout(self.timeout)
            socket.socket(socket.AF_INET,
                          socket.SOCK_STREAM).connect((self.host, self.port))
            self.intBtn['bg'] = 'green'
            self.varInter.set('Online')
        except Exception as ex:
            self.intBtn['bg'] = 'red'
            self.varInter.set('Offline')
            winsound.Beep(440, 250)
        # Server probe
        # if self.server:
        #     try:
        #         socket.setdefaulttimeout(self.timeout)
        #         socket.socket(socket.AF_INET,
        #                        socket.SOCK_STREAM).connect((self.server))
        #         self.srvMon1['bg'] = 'green'
        #     except Exception as ex:
        #         self.srvMon1['bg'] = 'red'
        #         winsound.Beep(440, 250)
        # Loop
        self.master.after(1000, self.refresh)
        self.endHdd = psutil.disk_io_counters()

def main():
    window = tk.Tk()
    app = TechHud(window)
    window.mainloop()

if __name__ == '__main__':
    main()
