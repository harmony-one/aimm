import csv

input_file_name = '1000_output.csv'
output_file_name = '1000_output_deduplicated.csv'

with open(input_file_name, mode='r', newline='') as infile, open(output_file_name, mode='w', newline='') as outfile:
    reader = csv.reader(infile, delimiter='|')
    writer = csv.writer(outfile, delimiter='|')
    
    header = next(reader)
    writer.writerow(header)
    
    line_number = 0
    
    for row in reader:
        if line_number % 2 == 0:
            writer.writerow(row)
        line_number += 1

print("Saved in '{}'.".format(output_file_name))
