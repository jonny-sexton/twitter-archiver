from datetime import *
import os.path

start_date = date(2015,1,1)
end_date = date(2015,2,19)
day_count = (end_date - start_date).days + 1

currentDir = "/home/pi/data/"

for single_date in (start_date + timedelta(n) for n in range(day_count)):
    print(single_date)

    file = currentDir + str(single_date.year) + "/" + str(single_date.month) + "/" + str(single_date) + ".txt"

    if os.path.isfile(file):
        print("EXISTS!")
    else:
        with open(file, "a") as f:
            f.close()
        print("File Created.")
