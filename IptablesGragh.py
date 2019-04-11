import re
import os
import datetime
import sys
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
                try:
                    dpt = re.search('DPT=(.*)', line_split[1]).group(1).split(" ")[0].strip()
                except:
                    print("debug: ")
                    print(sys.exc_info())

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
    try:
        transfer_title = "IP: " + ip + "\nTotal Time: " + str(time[-1]).rstrip('0').rstrip('.') + \
                         " sec | Total Transferred: " + unit_convert(total_transfer) + "Bytes"
        if time[-1] == 0:
            bandwidth_title = "IP: " + ip + "\nTotal Time: " + str(time[-1]).rstrip('0').rstrip('.') + \
                              " sec | Bandwidth: ~" + unit_convert_bw(total_bandwidth) + "bps"
        elif time[-1] < 0:
            bandwidth_title = "IP: " + ip + "\nTotal Time: " + str(time[-1]).rstrip('0').rstrip('.') + \
                              " sec | Bandwidth: ~" + unit_convert_bw(-(total_bandwidth / time[-1])) + "bps"
        else:
            bandwidth_title = "IP: " + ip + "\nTotal Time: " + str(time[-1]).rstrip('0').rstrip('.') + \
                              " sec | Bandwidth: ~" + unit_convert_bw(total_bandwidth / time[-1]) + "bps"
    except:
        print(sys.exc_info())
        return

    show_transfer(time, transfer, transfer_title,  filename)
    show_bandwidth(time, bandwidth, bandwidth_title, filename)


def show_transfer(time, transfer, transfer_title, filename):
    # Figure width is doubled (2*6.4) to display nicely 2 subplots side by side.
    fig, (ax) = plt.subplots(nrows=1, figsize=(12, 6))

    plt.title("Sender: " + transfer_title)

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


def show_bandwidth(time, bandwidth, bandwidth_title, filename):
    fig, (ax) = plt.subplots(nrows=1, figsize=(12, 6))

    plt.title("Sender: " + bandwidth_title)

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


def unit_convert(value):
    if 1024 < value < 1048576:
        return '~' + str(round(value/1024)).rstrip('0').rstrip('.') + ' K'
    elif 1048576 < value < 1073741824:
        return '~' + str(round(value/1048576)).rstrip('0').rstrip('.') + ' M'
    elif 1073741824 < value:
        return '~' + str(round(value/1073741824)).rstrip('0').rstrip('.') + ' G'
    else:
        return str(value).rstrip('0').rstrip('.') + ' '


def unit_convert_bw(value):
    if 1024 < value < 1048576:
        return str(round(value / 1024)).rstrip('0').rstrip('.') + ' K'
    elif 1048576 < value < 1073741824:
        return str(round(value / 1048576)).rstrip('0').rstrip('.') + ' M'
    elif 1073741824 < value:
        return str(round(value / 1073741824)).rstrip('0').rstrip('.') + ' G'
    else:
        return str(value).rstrip('0').rstrip('.') + ' '


def emptyfile(filename):
    f = open("iptables_output/" + filename, "w+")
    f.close()


def multifiles(ip):
    for filename in os.listdir("iptables_input"):
        with open(os.path.join("iptables_input", filename), "r") as file:
            run(file, ip)


def singlefile(ip):
    file = open(os.path.join("iptables_input", "iptables.log"), "r")
    run(file, ip)


if __name__ == "__main__":
    output = "iptables_output/"
    if not os.path.exists(output):
        os.makedirs(output)
    multifiles("192.168.8.70")
