import os

# delete all files in /iptables_input
input_files = [f for f in os.listdir("iptables_input/")]
for f in input_files:
    os.remove(os.path.join("iptables_input/", f))

'''
# delete all files in /iPerf_input
input_files = [f for f in os.listdir("iPerf_input/")]
for f in input_files:
    os.remove(os.path.join("iPerf_input/", f))
'''