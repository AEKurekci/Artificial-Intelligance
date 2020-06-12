import pandas as pd
import seaborn as sns

csv_directory = "csv_files\\"
output_directory = "graphics\\"
file_name = "wikipedia_history_suspects"
csv_file = csv_directory + file_name + ".csv"

wiki = pd.read_csv(csv_file, sep=',', encoding='windows-1254')
print(wiki.head(10))
print(wiki.isnull().sum())

sns_plot = sns.countplot(wiki['class_suspect'])
sns_plot.figure.savefig(output_directory + file_name + ".png")

