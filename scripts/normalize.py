import csv
import sys

reader = csv.DictReader(sys.stdin)
writer = csv.DictWriter(sys.stdout,
                        fieldnames=reader.fieldnames)
writer.writeheader()

for row in reader:
    writer.writerow({k: v.lower().strip() for k, v in row.items()})
