# This code is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode.

import math

def process_evalues(input_file, output_file, min_evalue):
    # initialize variables to track new minimum and maximum E-values
    new_min_evalue = float('inf')  # Set to a very high value initially
    new_max_evalue = -1000  # Set to low value

    #process file
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if line.startswith('Subject:') and 'E-value:' in line:
                parts = line.split('E-value:')
                evalue = float(parts[1].strip())
                #substitute for most common (highest frequency) e-values in your data sets for normalization 
                #mceval = 1; # most common evalue according to graph slide 65 for 18 member
                #mceval = 1e-45; # most common evalue according to graph slide 66 for 43 member
                mceval = 1e-25; # most common evalue according to graph slide 67 for 200 member

                evalue = evalue/mceval
                evalue = math.log10(evalue)

                # Update new minimum and maximum E-values
                new_min_evalue = min(new_min_evalue, evalue)
                new_max_evalue = max(new_max_evalue, evalue)

                # Write the modified line
                outfile.write(f'{parts[0]}E-value: {evalue}\n')
            else:
                # Write other lines as is
                outfile.write(line)

    # return new minimum and maximum E-values
    return new_min_evalue, new_max_evalue

# replace with your actual file paths and minimum E-value
#input_file_path = '/Users/chenlab/Desktop/blastcodetesting/fdgtest/final200membergraphdata50percent.txt'
#output_file_path = '/Users/chenlab/Desktop/blastcodetesting/fdgtest/finalprocessedmc200graphdata50percent.txt'
input_file_path = '/Users/chenlab/Desktop/blastcodetesting/fdgtest/all_binders200membergraphdata50percent.txt'
output_file_path = '/Users/chenlab/Desktop/blastcodetesting/fdgtest/finalprocessedmcallbinders200graphdata50percent.txt'
min_evalue =3.95e-171

new_min, new_max = process_evalues(input_file_path, output_file_path, min_evalue)
print(f"New Minimum E-value: {new_min}")
print(f"New Maximum E-value: {new_max}")
