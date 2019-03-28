import os

# delete all files in /input
input_files = [f for f in os.listdir("input/")]
for f in input_files:
    os.remove(os.path.join("input/", f))

# delete all png files in /output
output_files = [f for f in os.listdir("output/") if f.endswith(".png")]
for f in output_files:
    os.remove(os.path.join("output/", f))
