from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

file = open("data.txt", "r")
line = file.readline()
line = file.readline()
spend = []
income = []
while line:
    line = line.strip().split(',')
    income.append(line[0])
    spend.append(line[1])
    line = file.readline()

plt.scatter(income, spend, s=2, c='b', marker='o')
plt.show()
exit(0)
