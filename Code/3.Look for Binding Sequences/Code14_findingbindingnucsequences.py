# This code is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode.

import os
from collections import namedtuple

#given a list of sequences that were found to bind to the target bacteria from experimental data
# this code finds these sequences in the library

#namedtuple for binding sequences
BindingSequence = namedtuple('BindingSequence', ['name', 'nucleotide_sequence', 'amino_acid_sequence'])

#processing binding sequence file
def read_binding_sequences(filename):
    with open(filename, 'r') as file:
        lines = file.read().splitlines()

    binding_sequences = []
    for i in range(0, len(lines), 2):
        if '\t' in lines[i]:
            parts = lines[i].split('\t')
            name = parts[0].strip()
            nucleotide_sequence = parts[1].strip()
            aa_sequence = lines[i + 1].strip() if (i + 1) < len(lines) else ""
            binding_sequences.append(BindingSequence(name, nucleotide_sequence, aa_sequence))

    return binding_sequences

#function to find the binding sequences
def remove_whitespaces_and_search_sequences(input_filename, binding_sequences, output_filename=None):
    directory, basename = os.path.split(input_filename)
    if output_filename is None:
        output_filename = os.path.join(directory, 'processed_' + basename)

    with open(input_filename, 'r') as file:
        content = file.read()

    sequences = content.split('>')

    matching_sequences = {binding.name: [] for binding in binding_sequences}
    not_found_sequences = {binding.name for binding in binding_sequences}

    for seq in sequences:
        if seq:
            parts = seq.split('\n', 1)
            sequence_name = parts[0].strip()
            sequence = ''.join(parts[1].split())

            for binding in binding_sequences:
                if binding.nucleotide_sequence in sequence:
                    matching_sequences[binding.name].append(sequence_name)
                    not_found_sequences.discard(binding.name)

    with open(output_filename, 'w') as file:
        file.write("Binding Sequences Not Found:\n")
        for name in not_found_sequences:
            file.write(name + '\n')
        file.write("\nFound Sequences:\n")
        for binding_name, sequence_names in matching_sequences.items():
            for sequence_name in sequence_names:
                file.write(f"{sequence_name}, {binding_name}\n")

    return matching_sequences

#replace with your own file path
binding_sequences = read_binding_sequences('/Users/chenlab/Desktop/blastcodetesting/bindingsequences.txt')

# display the binding sequences
for binding in binding_sequences:
    print(f"Name: {binding.name}, Nucleotide Sequence: {binding.nucleotide_sequence}, "
          f"Amino Acid Sequence: {binding.amino_acid_sequence}")

#replace with your own file path
target_file_path = '/Users/chenlab/Desktop/blastcodetesting/18_member.txt'
output_file_path = '/Users/chenlab/Desktop/blastcodetesting/processedog18.txt'

found_sequences = remove_whitespaces_and_search_sequences(target_file_path, binding_sequences, output_file_path)
