# This code is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode.

#extract sequences
remove_count = 0
sequences_to_remove = set()
with open('/Users/chenlab/Desktop/blastcodetesting/exact_matches/exact_matches18.txt', 'r') as file:
    for line in file:
        seq = line.split(',')[1]
        print(seq)
        sequences_to_remove.add(seq)

#process the top3blastresutls file
print("brea")
output = []
with open('/Users/chenlab/Desktop/blastcodetesting/updates18membertop3blastresults.txt', 'r') as file:
    lines = file.readlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("Query:"):
            #remove prefix from top3blastresults
            seq = line.split('m64083_211102_082253/')[1] #18
            print(seq)
            #seq = line.split('m64083_220302_073838/')[1].split('/')[0] #43
            #seq = line.split('m64083_220722_080851/')[1].split('/')[0] #200
            # If the sequence is in the list to be removed, skip its block
            if seq in sequences_to_remove:
                remove_count = remove_count + 1
                print(seq)
                i += 1
                while i < len(lines) and not lines[i].startswith("Query:"):
                    i += 1
            else:
                output.append(line)
                i += 1
        else:
            output.append(line)
            i += 1

#write the unrepeated results to a new file
with open('/Users/chenlab/Desktop/blastcodetesting/nomatches_18membertop3blastresults.txt', 'w') as file:
    file.writelines(output)
print(remove_count)
