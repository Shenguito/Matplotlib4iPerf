import re
import os
import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter


def run(file, ip):
    time = []
    start_time = ""
    transfer = []
    total_transfer = 0
    bandwidth = []
    total_bandwidth = 0
    # bug file separator
    filename = file.name.split("\\")[1]
    for line in file:
        # outgoing
        if "IN=wlan0 OUT=eth0" in line:
            # defined source ip
            if "SRC="+ip in line:
                line_split = line.split("[spyke - log]")
                dst = re.search('DST=(.*)', line_split[1]).group(1).split(" ")[0].strip()
                dpt = re.search('DPT=(.*)', line_split[1]).group(1).split(" ")[0].strip()
                len = re.search('LEN=(.*)', line_split[1]).group(1).split(" ")[0].strip()
                # print("dst: " + dst)
                # print("dpt: " + dpt)
                # print("len: " + len)
                dateline = line_split[0].split("kernel:")[0].strip().replace("  ", " ").split(" ")
                date = dateline[0] + " " + dateline[1]
                # print("date: " + date)
                # print("time: " + getHour(dateline[2]).strftime("%H:%M:%S"))
                # print('[%s]' % ', '.join(map(str, dateline)))

                if time:
                    # print("time exists")
                    sub_time = getHour(dateline[2]) - start_time
                    # print(sub_time.total_seconds())
                    time.append(sub_time.total_seconds())
                else:
                    # print("time not exists")
                    time.append(0)
                    start_time = getHour(dateline[2])
                total_transfer += float(len)
                total_bandwidth += float(len)*8
                transfer.append(float(len))
                bandwidth.append(float(len)*8)

    transfer_sender = "Total Time: " + str(time[-1]).rstrip('0').rstrip('.') + " sec | Total Transferred: " + str(total_transfer).rstrip('0').rstrip('.') + " Bytes"
    bandwidth_sender = "Total Time: " + str(time[-1]).rstrip('0').rstrip('.') + " sec | Bandwidth: ~" + str(total_bandwidth/time[-1]).rstrip('0').rstrip('.') + " bps"

    show_transfer(time, transfer, transfer_sender,  filename)
    show_bandwidth(time, bandwidth, bandwidth_sender, filename)


def show_transfer(time, transfer, transfer_sender, filename):
    # Figure width is doubled (2*6.4) to display nicely 2 subplots side by side.
    fig, (ax) = plt.subplots(nrows=1, figsize=(12, 6))

    plt.title("Sender: " + transfer_sender)

    formatter = EngFormatter(places=1, sep="\N{THIN SPACE}")
    ax.plot(time, transfer)

    ax.yaxis.set_major_formatter(formatter)
    ax.set_ylim(bottom=0)  # y label start at 0
    ax.set_xlabel('time [sec]')
    ax.set_ylabel('transfer [Byte]')

    plt.tight_layout()
    # plt.show()

    fig.savefig('iptables_output/'+filename+'_QT.pdf')

    plt.close()


def show_bandwidth(time, bandwidth, bandwidth_sender, filename):
    fig, (ax) = plt.subplots(nrows=1, figsize=(12, 6))

    plt.title("Sender: " + bandwidth_sender)

    formatter = EngFormatter(places=1, sep="\N{THIN SPACE}")

    ax.plot(time, bandwidth)

    ax.yaxis.set_major_formatter(formatter)
    ax.set_ylim(bottom=0)  # y label start at 0
    ax.set_xlabel('time [sec]')
    ax.set_ylabel('bandwidth [bps]')
    plt.tight_layout()
    # plt.show()

    fig.savefig('iptables_output/'+filename+'_BW.pdf')

    plt.close()


def getHour(hour):
    return datetime.datetime.strptime(hour, '%H:%M:%S')


def emptyfile(filename):
    f = open("iptables_output/" + filename, "w+")
    f.close()


def multifiles():
    for filename in os.listdir("iptables_input"):
        with open(os.path.join("iptables_input", filename), "r") as file:
            run(file, "192.168.8.70")


def singlefile():
    file = open(os.path.join("iptables_input", "iptables.log"), "r")
    run(file, "192.168.8.70")


if __name__ == "__main__":
    multifiles()
