import sys, os

path = sys.argv[1].strip()

file_location = []
for file in os.listdir(path):
    if file.endswith(".txt"):
        file_location.append(os.path.join(path,file))

for file in file_location:
    os.system(f"python3 tspd.py \"{file}\"")

