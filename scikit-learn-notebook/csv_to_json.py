import copy
import json

json_data = {}
all_jsons = []
csv_file = "csv_files\\wikipedia_history_suspects_II_world_war.csv"
json_file = "json_files\\wikipedia_history_suspects_II_world_war.json"

file = open(csv_file, 'r')
line = file.readline()

keys = line.strip().split(",")
line = file.readline()
while line:
    line = line.strip().split(',')
    for index, key in enumerate(keys):
        try:
            json_data[key] = int(line[index])
        except:
            if 'True' in line[index]:
                json_data[key] = bool(":)")
            else:
                json_data[key] = bool("")
    all_jsons.append(copy.deepcopy(json_data))
    line = file.readline()

all_jsons = json.dumps(all_jsons)
out_file = open(json_file, 'w')
out_file.write(str(all_jsons))
