import re
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter


def run(file):
    time = []
    transfer = []
    bandwidth = []
    # bug file separator
    filename = file.name.split("\\")[1]
    for line in file:
        if "sec" in line:
            if "sender" in line:
                line_split = line.split("/sec")
                t = re.search('](.*)sec', line_split[0]).group(1).strip().split("-")[1].replace(" ", "") + "sec"
                trans = re.search('sec(.*)Bytes', line_split[0]).group(1).strip().replace(" ", "") + "Bytes"
                bw = re.search('Bytes(.*)bits', line_split[0]).group(1).strip().replace(" ", "") + "bits/sec"
                transfer_sender = "Total Time: " + t + " | Total Transferred: "+trans
                bandwidth_sender = "Total Time: " + t + " | Bandwidth: ~" + bw
            elif "receiver" in line:
                line_split = line.split("/sec")
                t = re.search('](.*)sec', line_split[0]).group(1).strip().split("-")[1].replace(" ", "") + "sec"
                trans = re.search('sec(.*)Bytes', line_split[0]).group(1).strip().replace(" ", "") + "Bytes"
                bw = re.search('Bytes(.*)bits', line_split[0]).group(1).strip().replace(" ", "") + "bits/sec"
                transfer_receiver = "Total Time: " + t + " | Total Transferred: " + trans
                bandwidth_receiver = "Total Time: " + t + " | Bandwidth: ~" + bw
            elif "SUM" in line:
                print("iPerf3 several connections")
                emptyfile("multi_conn_" + filename)
                return
            else:
                # get time, transfer and bandwidth
                line_split = line.split("/sec")

                t = float(re.search('](.*)sec', line_split[0]).group(1).strip().split("-")[1].replace(" ", ""))
                # print(t)

                trans = unit_convert(re.search('sec(.*)Bytes', line_split[0]).group(1).strip().replace(" ", ""))
                # print(trans)

                bw = unit_convert(re.search('Bytes(.*)bits', line_split[0]).group(1).strip().replace(" ", ""))
                # print(bw)

                time.append(t)
                transfer.append(trans)
                bandwidth.append(bw)

        if "error" in line:
            print("iPerf3 error")
            emptyfile("error_" + filename)
            return
        if "interrupt" in line:
            print("iPerf3 interrupted")
            emptyfile("interrupted_" + filename)
            return

    # if the iPerf is not completed
    try:
        transfer_sender
        transfer_receiver
        bandwidth_sender
        bandwidth_receiver
    except NameError:
        print("not finished")
        emptyfile("not_finished_" + filename)
        return

    show_transfer(time, transfer, transfer_sender, transfer_receiver, filename)
    show_bandwidth(time, bandwidth, bandwidth_sender, bandwidth_receiver, filename)


def show_transfer(time, transfer, transfer_sender, transfer_receiver, filename):
    # Figure width is doubled (2*6.4) to display nicely 2 subplots side by side.
    fig, (ax) = plt.subplots(nrows=1, figsize=(12, 6))

    plt.title("Sender: " + transfer_sender + "\n Receiver: " + transfer_receiver)

    formatter = EngFormatter(places=1, sep="\N{THIN SPACE}")
    ax.plot(time, transfer)

    ax.yaxis.set_major_formatter(formatter)
    ax.set_ylim(bottom=0)  # y label start at 0
    ax.set_xlabel('time [sec]')
    ax.set_ylabel('transfer [Byte]')

    plt.tight_layout()
    # plt.show()

    fig.savefig('iPerf_output/'+filename+'_QT.pdf')

    plt.close()


def show_bandwidth(time, bandwidth, bandwidth_sender, bandwidth_receiver, filename):
    fig, (ax) = plt.subplots(nrows=1, figsize=(12, 6))

    plt.title("Sender: " + bandwidth_sender + "\n Receiver: " + bandwidth_receiver)

    formatter = EngFormatter(places=1, sep="\N{THIN SPACE}")

    ax.plot(time, bandwidth)

    ax.yaxis.set_major_formatter(formatter)
    ax.set_ylim(bottom=0)  # y label start at 0
    ax.set_xlabel('time [sec]')
    ax.set_ylabel('bandwidth [bps]')
    plt.tight_layout()
    # plt.show()

    fig.savefig('iPerf_output/'+filename+'_BW.pdf')

    plt.close()


def unit_convert(value):
    if "K" in value:
        value = value[:-1]
        value = float(value+"e+3")
    elif "M" in value:
        value = value[:-1]
        value = float(value+"e+6")
    elif "G" in value:
        value = value[:-1]
        value = float(value+"e+9")
    else:
        value = float(value)
    return value


def emptyfile(filename):
    f = open("iPerf_output/" + filename, "w+")
    f.close()


def multifiles():
    for filename in os.listdir("iPerf_input"):
        with open(os.path.join("iPerf_input", filename), "r") as file:
            run(file)


def singlefile():
    file = open(os.path.join("iPerf_input", "normal"), "r")
    run(file)


def show_filetransfer(filetransfer, transfer_sender, transfer_receiver):
    # Figure width is doubled (2*6.4) to display nicely 2 subplots side by side.
    fig, (ax) = plt.subplots(nrows=1, figsize=(12, 6))

    plt.title("Sender: " + transfer_sender + "\n Receiver: " + transfer_receiver)

    formatter = EngFormatter(places=1, sep="\N{THIN SPACE}")

    for value in filetransfer:
        if len(value) == 3:
            ax.plot(value[0], value[1], label=value[2])

    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    ax.yaxis.set_major_formatter(formatter)
    ax.set_ylim(bottom=0)  # y label start at 0
    ax.set_xlabel('time [sec]')
    ax.set_ylabel('transfer [Byte]')

    plt.tight_layout()
    # plt.show()

    fig.savefig('iPerf_output/multiplots_QT.pdf')

    plt.close()


def show_filebandwidth(filebandwidth, bandwidth_sender, bandwidth_receiver):
    fig, (ax) = plt.subplots(nrows=1, figsize=(12, 6))

    plt.title("Sender: " + bandwidth_sender + "\n Receiver: " + bandwidth_receiver)

    formatter = EngFormatter(places=1, sep="\N{THIN SPACE}")

    for value in filebandwidth:
        if len(value) == 3:
            ax.plot(value[0], value[1], label=value[2])

    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    ax.yaxis.set_major_formatter(formatter)
    ax.set_ylim(bottom=0)  # y label start at 0
    ax.set_xlabel('time [sec]')
    ax.set_ylabel('bandwidth [bps]')
    plt.tight_layout()
    # plt.show()

    fig.savefig('iPerf_output/multiplots_BW.pdf')

    plt.close()


def allfiles():
    transfer = []
    bandwidth = []
    for filename in os.listdir("iPerf_input"):
        with open(os.path.join("iPerf_input", filename), "r") as file:
            filename = file.name.split("\\")[1]
            filetime = []
            filetransfer = []
            filebandwidth = []
            for line in file:
                if "sec" in line:
                    if "sender" in line:
                        # get total value of sender at the end
                        line_split = line.split("/sec")
                        t = re.search('](.*)sec', line_split[0]).group(1).strip().split("-")[1].replace(" ", "") + "sec"
                        trans = re.search('sec(.*)Bytes', line_split[0]).group(1).strip().replace(" ", "") + "Bytes"
                        bw = re.search('Bytes(.*)bits', line_split[0]).group(1).strip().replace(" ", "") + "bits/sec"
                        transfer_sender = "Total Time: " + t + " "
                        #transfer_sender = "Total Time: " + t + " | Total Transferred: " + trans
                        bandwidth_sender = "Total Time: " + t + " "
                        #bandwidth_sender = "Total Time: " + t + " | Bandwidth: ~" + bw
                    elif "receiver" in line:
                        # get total value of receiver at the end
                        line_split = line.split("/sec")
                        t = re.search('](.*)sec', line_split[0]).group(1).strip().split("-")[1].replace(" ", "") + "sec"
                        trans = re.search('sec(.*)Bytes', line_split[0]).group(1).strip().replace(" ", "") + "Bytes"
                        bw = re.search('Bytes(.*)bits', line_split[0]).group(1).strip().replace(" ", "") + "bits/sec"
                        #transfer_receiver = "Total Time: " + t + " | Total Transferred: " + trans
                        transfer_receiver = "Total Time: " + t + " "
                        #bandwidth_receiver = "Total Time: " + t + " | Bandwidth: ~" + bw
                        bandwidth_receiver = "Total Time: " + t + " "
                    elif "SUM" in line:
                        print("iPerf3 several connections")
                        emptyfile("multi_conn_" + filename)
                        return
                    else:
                        # get values of time, transfer and bandwidth
                        line_split = line.split("/sec")

                        t = float(re.search('](.*)sec', line_split[0]).group(1).strip().split("-")[1].replace(" ", ""))
                        #print(t)

                        trans = unit_convert(re.search('sec(.*)Bytes', line_split[0]).group(1).strip().replace(" ", ""))
                        #print(trans)

                        bw = unit_convert(re.search('Bytes(.*)bits', line_split[0]).group(1).strip().replace(" ", ""))
                        #print(bw)

                        filetime.append(t)
                        filetransfer.append(trans)
                        filebandwidth.append(bw)

                if "error" in line:
                    print("iPerf3 error")
                    emptyfile("error_" + filename)
                    return
                if "interrupt" in line:
                    print("iPerf3 interrupted")
                    emptyfile("interrupted_" + filename)
                    return

            #time.append(filetime)
            transfer.append([filetime, filetransfer, filename])
            bandwidth.append([filetime, filebandwidth, filename])

    # if the iPerf is not completed
    try:
        transfer_sender
        transfer_receiver
        bandwidth_sender
        bandwidth_receiver
    except NameError:
        print("not finished")
        emptyfile("not_finished_" + filename)
        return

    show_filetransfer(transfer, transfer_sender, transfer_receiver)
    show_filebandwidth(bandwidth, bandwidth_sender, bandwidth_receiver)


if __name__ == "__main__":
    output = "iPerf_output/"
    if not os.path.exists(output):
        os.makedirs(output)
    allfiles()
