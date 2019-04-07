import os

# delete all png files in /iptables_output
output_files = [f for f in os.listdir("iptables_output/")]  # if f.endswith(".png")
for f in output_files:
    os.remove(os.path.join("iptables_output/", f))

# delete all png files in /iPerf_output
output_files = [f for f in os.listdir("iPerf_output/")]  # if f.endswith(".png")
for f in output_files:
    os.remove(os.path.join("iPerf_output/", f))
