# This code is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode.

#this code is specifically for highlighting some of the binders that were not specifically
import random
from collections import defaultdict

def read_exact_matches(filename):
    repeats = defaultdict(int)
    with open(filename, 'r') as file:
        for line in file:
            seq = line.split(',')[0]
            #full_seq = 'm64083_211102_082253/' + seq  # For 18member
            #full_seq = 'm64083_220302_073838/' + seq  # For 43 member
            full_seq = 'm64083_220722_080851/' + seq  # For 200 member
            repeats[full_seq] += 1
    return repeats

def read_binder_q1(filename):
    binder_q1 = set()
    with open(filename, 'r') as file:
        for line in file:
            # Assuming the file format contains the query names in a specific part of each line
            query = line.split('\t')[0].split(': ')[1]  # Adjust based on the actual format
            binder_q1.add(query)
    return binder_q1

def read_found_sequences(filename, specific_binder):
    found_sequences = defaultdict(list)
    process_found = False
    with open(filename, 'r') as file:
        for line in file:
            if line.strip() == "Found Sequences:":
                process_found = True
                continue
            if process_found:
                parts = line.strip().split(', ')
                seq = parts[0]
                binder_name = parts[1]
                #print(binder_name)
                name_parts = binder_name.strip().split('-')
                binder_name = name_parts[0]
                #print(binder_name)
                found_sequences[binder_name].append(seq)
    return found_sequences[specific_binder]


def select_sequences_with_specific_binder(all_sequences, specific_binder_sequences, selected_repeats, percentage=0.1):
    if not any(seq in selected_repeats for seq in specific_binder_sequences):
        # If no specific binder sequences are selected, add at least one or up to 10%
        num_to_add = max(1, int(len(specific_binder_sequences) * percentage))
        additional_seqs = random.sample(specific_binder_sequences, num_to_add)
        selected_repeats.update(additional_seqs)
    return selected_repeats

def process_blast_results(blast_file, repeats, binder, output_file, specific_binder_sequence, percentage=0.50):
    with open(blast_file, 'r') as file:
        lines = file.readlines()

    all_queries = set()
    for line in lines:
        if line.startswith('Query:'):
            query = line.split()[1]
            all_queries.add(query)

    total_queries = sum(1 for line in lines if line.startswith('Query:'))
    max_queries = int(total_queries * percentage)
    repeat_queries_set = set(repeats.keys())
    found_repeats = set()

    for line in lines:
        if line.startswith('Query:'):
            query = line.split()[1]
            if query in repeat_queries_set:
                found_repeats.add(query)

    if len(found_repeats) > max_queries:
        selected_repeats = set(random.sample(found_repeats, max_queries))
    else:
        non_repeat_queries = all_queries - found_repeats
        additional_required = max_queries - len(found_repeats)
        selected_additional = set(random.sample(non_repeat_queries, additional_required))
        selected_repeats = found_repeats.union(selected_additional)
        selected_repeats = select_sequences_with_specific_binder(all_queries, specific_binder_sequence, selected_repeats)


    min_e_value = float('inf')
    max_e_value = 0
    avg_e_value = 0
    e_val_count = 0
    processed_queries = 0

    with open(output_file, 'w') as out_file:
        for line in lines:
            if line.startswith('Query:'):
                query = line.split()[1]
                include = query in selected_repeats
                
                if include:
                    processed_queries += 1
                    prefix = 'b&' if query in specific_binding_sequences else ''
                    prefix += f'!{repeats[query]}' if query in repeat_queries_set else ''
                    out_file.write(f'\nQuery: {prefix}{query}\n')
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

# File paths
exact_matches_file = '/Users/chenlab/Desktop/blastcodetesting/exact_matches/exact_matches200.txt'
blast_results_file = '/Users/chenlab/Desktop/blastcodetesting/norepeats_200membertop3blastresults.txt'
output_file = '/Users/chenlab/Desktop/blastcodetesting/fdgtest/binderAB200membergraphdata50percent.txt'
#binder_q1_file = '/Users/chenlab/Desktop/blastcodetesting/43PA-BinderQ1.txt' #for graphing the first quartile 
binder_file = "/Users/chenlab/Desktop/blastcodetesting/processedog200.txt"
specific_binder_sequence = "AB"

# Process the files
repeats = read_exact_matches(exact_matches_file)
specific_binding_sequences = read_found_sequences(binder_file, specific_binder_sequence)  
process_blast_results(blast_results_file, repeats, specific_binding_sequences, output_file, specific_binder_sequence) # Again, specify your binder name


