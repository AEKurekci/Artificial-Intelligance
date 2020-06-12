import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

csv_directory = "csv_files\\"
output_directory = "graphics\\"
file_name = "wikipedia_history_suspects_I_world_war"
csv_file = csv_directory + file_name + ".csv"

wiki = pd.read_csv(csv_file, sep=',', encoding='windows-1254')
print(wiki.head(10))
print(wiki.isnull().sum())

sns_plot = sns.countplot(wiki['class_suspect'])
sns_plot.figure.savefig(output_directory + file_name + "_count_plot.png")

true_count = 0
false_count = 0
for i in wiki['class_suspect'].values:
    if i:
        true_count += 1
    else:
        false_count += 1

sizes = [true_count, false_count]
labels = 'True', 'False'
explode = (0.1, 0)
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
ax1.axis('equal')

plt.savefig(output_directory + file_name + "_pie_plot.png")


