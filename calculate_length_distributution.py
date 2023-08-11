import sys
import os
import csv

def classified_sequence_length_distribution(filename):
    # A dictionary to hold the length distribution
    length_distribution = {}
    
    with open(filename, "r") as file:
        for line in file:
            fields = line.strip().split('\\t')
            
            # Check if the sequence is classified
            if fields[0] == 'C':
                length = int(fields[3])  # Corrected this line to fetch length from the fourth column
                
                # Update the distribution dictionary
                if length in length_distribution:
                    length_distribution[length] += 1
                else:
                    length_distribution[length] = 1
    
    return length_distribution

def main():
    # Dictionary to hold all distributions
    all_distributions = {}
    
    # Get all filenames from command line arguments
    filenames = sys.argv[1:]
    
    for filename in filenames:
        sample_name = os.path.basename(filename).split('.')[0]
        distribution = classified_sequence_length_distribution(filename)
        all_distributions[sample_name] = distribution

    # Getting all unique lengths
    all_lengths = set()
    for distribution in all_distributions.values():
        all_lengths.update(distribution.keys())
    all_lengths = sorted(all_lengths)
    
    # Writing to CSV
    with open('output_distribution.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        headers = ['Length'] + list(all_distributions.keys())
        csvwriter.writerow(headers)
        
        for length in all_lengths:
            row = [length]
            for sample in headers[1:]:
                row.append(all_distributions[sample].get(length, 0))
            csvwriter.writerow(row)
    
if __name__ == "__main__":
    main()
