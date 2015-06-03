__author__ = 'Matias'

filename = "C:\Users\matias\Desktop\churn.txt"

with open(filename, 'r') as infile:
    lines = infile.read().split(".\n")[:-1]

states = []

for line in lines:
    parts = line.split(",")
    state = parts[0]
    account_length = parts[1]
    area_code = parts[2]
    phone = parts[3]





print len(lines)
