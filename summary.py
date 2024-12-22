from glob import glob
from json import load, dump

FOLDER = "cf_on_luogu"

all_obj = {}

for file in glob(f"{FOLDER}/*"):
    obj = load(open(file, "r"))
    all_obj.update({pro['pid']:pro for pro in obj})

dump(all_obj, open("problems.json", "w"))