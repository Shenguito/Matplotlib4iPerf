import os

# delete all png files in /output
output_files = [f for f in os.listdir("output/") if f.endswith(".png")]
for f in output_files:
    os.remove(os.path.join("output/", f))
