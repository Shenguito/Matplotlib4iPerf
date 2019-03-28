import re
import os
import matplotlib.pyplot as plt


def run(file):
    time = []
    transfer = []
    bandwidth = []
    filename = file.name.split("\\")[1]
    for line in file:
        if "sec" in line:
            if "sender" in line:
                line_split = line.split("/sec")
                t = re.search('](.*)sec', line_split[0]).group(1).strip().split("-")[1].replace(" ", "") + "sec"
                trans = re.search('sec(.*)Bytes', line_split[0]).group(1).strip().replace(" ", "") + "Bytes"
                bw = re.search('Bytes(.*)bits', line_split[0]).group(1).strip().replace(" ", "") + "bits/sec"
                transfer_sender = "Time: " + t + " | Transferred: "+trans
                bandwidth_sender = "Time: " + t + " | Bandwidth: ~" + bw
            elif "receiver" in line:
                line_split = line.split("/sec")
                t = re.search('](.*)sec', line_split[0]).group(1).strip().split("-")[1].replace(" ", "") + "sec"
                trans = re.search('sec(.*)Bytes', line_split[0]).group(1).strip().replace(" ", "") + "Bytes"
                bw = re.search('Bytes(.*)bits', line_split[0]).group(1).strip().replace(" ", "") + "bits/sec"
                transfer_receiver = "Time: " + t + " | Transferred: " + trans
                bandwidth_receiver = "Time: " + t + " | Bandwidth: ~" + bw
            else:
                # get time, transfer and bandwidth
                line_split = line.split("/sec")

                t = unit_convert(re.search('](.*)sec', line_split[0]).group(1).strip().split("-")[1].replace(" ", ""))
                # print(t)

                trans = unit_convert(re.search('sec(.*)Bytes', line_split[0]).group(1).strip().replace(" ", ""))
                # print(trans)

                bw = unit_convert(re.search('Bytes(.*)bits', line_split[0]).group(1).strip().replace(" ", ""))
                # print(bw)

                time.append(t)
                transfer.append(trans)
                bandwidth.append(bw)

    # if the iPerf is not completed
    try:
        transfer_sender
    except NameError:
        transfer_sender = "not finished"
    try:
        transfer_receiver
    except NameError:
        transfer_receiver = "not finished"
    try:
        bandwidth_sender
    except NameError:
        bandwidth_sender = "not finished"
    try:
        bandwidth_receiver
    except NameError:
        bandwidth_receiver = "not finished"

    show_transfer(time, transfer, transfer_sender, transfer_receiver, filename)
    show_bandwidth(time, bandwidth, bandwidth_sender, bandwidth_receiver, filename)


def show_transfer(time, transfer, transfer_sender, transfer_receiver, filename):
    fig = plt.figure()

    plt.plot(time, transfer)
    plt.title("Sender: "+transfer_sender+"\n Receiver: "+transfer_receiver)
    plt.xlabel('time')
    plt.ylabel('transfer(Bytes)')
    plt.tight_layout()
    # plt.show()

    fig.savefig('output/'+filename+'_QT.png')


def show_bandwidth(time, bandwidth, bandwidth_sender, bandwidth_receiver, filename):
    fig = plt.figure()

    plt.plot(time, bandwidth)
    plt.title("Sender: "+bandwidth_sender+"\n Receiver: "+bandwidth_receiver)
    plt.xlabel('time')
    plt.ylabel('bandwidth(bit/sec)')
    plt.tight_layout()
    # plt.show()

    fig.savefig('output/'+filename+'_BW.png')


def unit_convert(value):
    if "K" in value:
        value = value[:-1]
        value = float(value) * 1024
    elif "M" in value:
        value = value[:-1]
        value = float(value) * 1024 * 1024
    elif "G" in value:
        value = value[:-1]
        value = float(value) * 1024 * 1024 * 1024
    else:
        value = float(value)
    return value


def multifiles():
    for filename in os.listdir("input"):
        with open(os.path.join("input", filename), "r") as file:
            run(file)


def singlefile():
    file = open("input/1gb_bw1mb", "r")
    run(file)


if __name__ == "__main__":
    multifiles()
