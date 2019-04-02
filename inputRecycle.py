import os

# delete all files in /input
input_files = [f for f in os.listdir("input/")]
for f in input_files:
    os.remove(os.path.join("input/", f))
