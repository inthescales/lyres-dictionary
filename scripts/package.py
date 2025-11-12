import os
import shutil

output_path = "./deploy"

if os.path.exists(output_path) and os.path.isdir(output_path):
    shutil.rmtree(output_path)

os.mkdir(output_path)

files = [
	"lyre.py",
	"requirements.txt",
	"creds.json"
]

directories = [
	"src",
	"data",
	"scripts"
]

print ("Copying files")

for file in files:
	shutil.copy(file, output_path + "/" + file)

print ("Copying directories")

for directory in directories:
	shutil.copytree(directory, output_path + "/" + directory)

print("Finished")
