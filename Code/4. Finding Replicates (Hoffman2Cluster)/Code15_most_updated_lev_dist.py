# This code is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode.

import Levenshtein
from multiprocessing import Pool, cpu_count
import time

start_time = time.time()

#function to parse fasta file
def parse_fasta(file_path):
    with open(file_path, "r") as file:
        identifier = None
        sequence = []

        for line in file:
            if line.startswith(">"):
                if identifier:
                    yield identifier, ''.join(sequence)
                identifier, sequence = line.rstrip()[1:], []
            else:
                sequence.append(line.strip())

        if identifier:
            yield identifier, ''.join(sequence)

#levenshtein distance calculator where 1.0 is exactly the same
def calculate_similarity(pair):
    sequence1, sequence2, name1, name2 = pair
    distance = Levenshtein.distance(sequence1, sequence2)
    max_length = max(len(sequence1), len(sequence2))
    return 1 - distance / max_length, name1.split('/', 1)[1], name2.split('/', 1)[1]

#pairing sequences for analysis
def generate_pairs(sequences, sequence_names):
    num_sequences = len(sequences)
    for i in range(num_sequences):
        for j in range(i + 1, num_sequences):
            yield sequences[i], sequences[j], sequence_names[i], sequence_names[j]

def main():
    #change to your file path
    fasta_file = "/Users/chenlab/Desktop/blastcodetesting/levinsteindistancetest.fasta"

    sequences = []
    sequence_names = []

    for record_id, sequence in parse_fasta(fasta_file):
        sequence_names.append(record_id)
        sequences.append(sequence)
    
    #uses as many CPUs as available
    with Pool(processes=cpu_count()) as pool:
        counter = 0
        #with open("/u/scratch/b/bmihalac/levinsteindistanceforhoffman/18member_similarity_results.txt", "w") as output_file:
        with open("/Users/chenlab/Desktop/blastcodetesting/similarity_results.txt", "w") as output_file:    
            for similarity, seq_name1, seq_name2 in pool.imap_unordered(calculate_similarity, generate_pairs(sequences, sequence_names)):
                output_file.write(f"{seq_name1},{seq_name2},{similarity:.4f}\n")
                counter += 1
                if counter % 1000 == 0:
                    print(f"Processed {counter} pairs")

    print("Similarity results have been written to 'similarity_results.txt'")

if __name__ == "__main__":
    main()

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Total time taken: {elapsed_time:.2f} seconds")
