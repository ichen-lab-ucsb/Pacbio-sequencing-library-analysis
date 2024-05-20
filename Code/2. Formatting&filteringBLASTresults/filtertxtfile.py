# This code is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode.

seen_alignments = set()
#input file is the blast reqults in the 
with open("/Users/chenlab/Desktop/blastcodetesting/formatblastp_mostusedrefseq_results.txt", "r") as input_file, open("/Users/chenlab/Desktop/blastcodetesting/filteredblastp_mostusedrefseq_results.txt", "w") as output_file:
    for line in input_file:
        parts = line.strip().split("\t")
        query_id, subject_id, evalue = parts[0], parts[1], parts[2]
        alignment_info = (query_id, subject_id, evalue)
        if alignment_info not in seen_alignments:
            seen_alignments.add(alignment_info)
            output_file.write(line)


