# This code is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode.

import random
from collections import defaultdict
#reading file with matches
def read_exact_matches(filename):
    repeats = defaultdict(int)  # initialize a defaultdict for counting

    with open(filename, 'r') as file:
        for line in file:
            seq = line.split(',')[0]
            # assuming 'full_seq' is the format you want to store in the dictionary, add these prefixes
            full_seq = 'm64083_211102_082253/' + seq  # For 18member
            #full_seq = 'm64083_220302_073838/' + seq  # For 43 member
            #full_seq = 'm64083_220722_080851/' + seq  # For 200 member
            repeats[full_seq] += 1  # Increment the count for this sequence
    return repeats

#reading file with blast results and finding the repeated sequences
def process_blast_results(blast_file, repeat_queries, output_file, percentage=0.05):
    with open(blast_file, 'r') as file:
        lines = file.readlines()

    total_queries = sum(1 for line in lines if line.startswith('Query:'))
    max_queries = int(total_queries * percentage)
    print(f"Number of repeat queries: {len(repeat_queries)}")
    print(f"Max queries: {max_queries}")

    # Convert dictionary keys to a set
    repeat_queries_set = set(repeats.keys())


    # Check if repeat sequences exist in blast_file
    found_repeats = set()
    for line in lines:
        if line.startswith('Query:'):
            query = line.split()[1]
            #full_query = 'm64083_211102_082253/' + seq  # For 18member
            if query in repeat_queries:
                found_repeats.add(query)
    print(f"Repeat queries found in file: {len(found_repeats)}")
    
    if len(found_repeats) > max_queries:
        selected_repeats = set(random.sample(found_repeats, max_queries))
    else:
        non_repeat_queries = repeat_queries_set - found_repeats
        selected_additional = set(random.sample(non_repeat_queries, max_queries - len(found_repeats)))
        selected_repeats = found_repeats.union(selected_additional)
        #print(selected_repeats)

    #will compute and print these statistics
    min_e_value = float('inf')
    max_e_value = 0
    avg_e_value = 0
    e_val_count = 0
    processed_queries = 0

    with open(output_file, 'w') as out_file:
        query_count = 0
        include = False
        for line in lines:
            if line.startswith('Query:'):
                query = line.split()[1]
                include = query in selected_repeats
                #print(f"Query: {query}, Include: {include}")  # Debugging print
                
                if include:
                    processed_queries += 1
                    prefix = f'!{repeats[query]}' if query in repeat_queries else ''
                    out_file.write(f'\nQuery: {prefix}{query}\n')
                query_count += 1
            elif include and line.startswith('Subject:'):
                e_value = float(line.split()[3])
                e_val_count += 1
                avg_e_value += e_value
                min_e_value = min(min_e_value, e_value)
                max_e_value = max(max_e_value, e_value)
                out_file.write(line)
    print(f"Avg E-value: {avg_e_value/e_val_count}")
    print(f"Minimum E-value: {min_e_value}")
    print(f"Maximum E-value: {max_e_value}")
    print(f"Total queries: {total_queries}")
    print(f"Processed queries: {processed_queries}")
    print(f"Percentage of data used: {(processed_queries / total_queries)*100:.2f}%")

#change to your path name
exact_matches_file = '/Users/chenlab/Desktop/blastcodetesting/exact_matches/exact_matches18.txt'
blast_results_file = '/Users/chenlab/Desktop/blastcodetesting/norepeats_18membertop3blastresults.txt'
output_file = '/Users/chenlab/Desktop/blastcodetesting/fdgtest/final18membergraphdata5percent.txt'

# process the files
repeats = read_exact_matches(exact_matches_file)
process_blast_results(blast_results_file, repeats, output_file)
