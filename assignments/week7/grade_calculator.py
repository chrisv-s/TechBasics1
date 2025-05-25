
from sys import argv
import csv
import random

# I set these to global values so I can use rows, fieldnames in my main
rows = []
fieldnames = []

# Step 1
def read_csv(filename):
    global rows, fieldnames
    rows = []
    try:
        with open(filename, newline='') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames.copy()
            for row in reader:
                first_field = fieldnames[0]
                if not row.get(first_field, '').strip():
                    continue  # I want to skip the rows where there is no useful information
                rows.append(row)
    except FileNotFoundError: # exception handling if the csv file is not found
        print("The file was not found")
        rows, fieldnames = [], []
    except PermissionError:
        print("No permission to access the file")
        rows, fieldnames = [], []

# Step 2
def populate_scores():
    global rows
    for i in range(1, 14):
        if i == 6 or 1 <= i <= 5:
            continue # so I dont overwrite the scores from week 1-5
        col = f'week{i}'
        if col not in fieldnames:
            fieldnames.append(col) # append columns
        for row in rows:
            if col not in row or row[col].strip() == '':
                row[col] = str(random.randint(1, 3)) # random grade

# Step 3
def calculate_all():
    global rows, fieldnames

    if not rows:  # just a precautionary step
        print("No data to process.")
        return

    if 'Total Points' not in fieldnames: # add the two columns
        fieldnames.append('Total Points')
    if 'Average Points' not in fieldnames:
        fieldnames.append('Average Points')

    for row in rows:
        scores = []
        for i in range(1, 14):
            if i == 6:
                continue
            val = row.get(f'week{i}', '').strip()
            if val.isdigit():
                scores.append(int(val))

        total = calculate_total(scores)
        average = calculate_average(total)

        row['Total Points'] = str(total)
        row['Average Points'] = str(average)

    return rows, fieldnames

def calculate_total(scores):
    total = 0
    best_scores = scores[:12]
    best_10 = sorted(best_scores, reverse=True)[:10]
    total = sum(best_10)
    return total

def calculate_average(total):
    average = 0
    average = round(total / 12, 2)
    return average

def write_csv(filename):
    global rows, fieldnames
    try:
# in case there is a permission error
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"Data successfully written to {filename}")
    except PermissionError:
        print("No permission to write to the file.")

def print_analysis():
    global rows

    # I used a list comprehension to create two lists for each stream, source: https://realpython.com/list-comprehension-python/
    stream_a_students = [row for row in rows if row.get('Stream', '').strip().upper() == 'A']
    stream_b_students = [row for row in rows if row.get('Stream', '').strip().upper() == 'B']

    num_a = len(stream_a_students)
    num_b = len(stream_b_students)

    if num_a == 0 and num_b == 0: # just in case...
        print("No data found.")
        return

    print("\n📊 Weekly Average Scores by Stream (Total Points / #Students)")
    print("+--------+------------+------------+")
    print("| Week   | Stream A   | Stream B   |")
    print("+--------+------------+------------+")

    for i in range(1, 14):
        if i == 6:
            continue

        week_col = f'week{i}'

        total_a = sum(
            int(row[week_col]) for row in stream_a_students
            if row.get(week_col, '').isdigit()
        )
        total_b = sum(
            int(row[week_col]) for row in stream_b_students
            if row.get(week_col, '').isdigit()
        )

        avg_a = round(total_a / num_a, 2) if num_a > 0 else 0
        avg_b = round(total_b / num_b, 2) if num_b > 0 else 0

        print(f"| week{i:<2} |   {avg_a:>6.2f}   |   {avg_b:>6.2f}   |") # make print look nice

    print("+--------+------------+------------+\n")

if __name__ == "__main__":
    script, filename = argv

    print("Open file:", filename)

    read_csv(filename)

    populate_scores()
    calculate_all()

    user_name = "Chris"

    newname = filename.split(".")[0] + "_calculated_by_" + user_name + ".csv"
    write_csv(newname)
    print("New file written:", newname)

    print_analysis()


