import matplotlib.pyplot as plt
import re
import os


def run(file):
    transfer_sender, bandwidth_sender, transfer_receiver, bandwidth_receiver = ""
    time = []
    transfer = []
    bandwidth = []

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
                t = re.search('](.*)sec', line_split[0]).group(1).strip().split("-")[1].replace(" ", "")
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

    show_transfer(time, transfer, transfer_sender, transfer_receiver)
    show_bandwidth(time, bandwidth, bandwidth_sender, bandwidth_receiver)


def show_transfer(time, transfer, transfer_sender, transfer_receiver):

    plt.plot(time, transfer)
    plt.title("Sender: "+transfer_sender+"\n Receiver: "+transfer_receiver)
    plt.xlabel('time')
    plt.ylabel('transfer(Bytes)')

    plt.show()


def show_bandwidth(time, bandwidth, bandwidth_sender, bandwidth_receiver):

    plt.plot(time, bandwidth)
    plt.title("Sender: "+bandwidth_sender+"\n Receiver: "+bandwidth_receiver)
    plt.xlabel('time')
    plt.ylabel('bandwidth(bit/sec)')

    plt.show()


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


def multifile():
    for filename in os.listdir("input"):
        with open(os.path.join("input", filename), "r") as file:
            run(file)


def singlefile():
    file = open("input/1gb_bw1mb", "r")
    run(file)


if __name__ == "__main__":
    multifile()
