# A simple parser for raw name diminutives
# Parses and saves to the desired output

from pathlib import Path

in_f = open("cenas.txt", "r")

out_f = open("raw_names_dim.txt", "w")
for line in in_f:
    line = line.replace("\n", "")
    line = line.replace(",", "")
    line = line.replace("/", " ")
    contents = line.split(' ')
    
    to_remove = []
    
    contents = [x for x in contents if x != ""]
    for cnt in contents:
        if cnt[0].islower() or not cnt[0].isalpha():
            to_remove.append(cnt)
            
    contents = [x for x in contents if x not in to_remove]
    if len(contents) < 2:
        continue
    out_f.write(",".join(contents) + "\n")
    # print(contents)