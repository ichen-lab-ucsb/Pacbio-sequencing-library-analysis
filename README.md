# Pacbio sequencing library analysis
This is a pipeline for evaluating the efficiency and diversity of protein libraries given DNA sequences. Currently this pipeline is specific to analyzing the g3p protein of bacteriophages which binds to gram-negative bacteria. This tool creates a force-directed clustered visualization to depict the diversity of the library. 

## License
This project is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License. To view a copy of this license, visit [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode).


## Usage:
Follow flow chart for steps of process. With modifications, this code can be generalized to evaluate other types of libraries as well. For all codes, the input file must be changed. Following the flow chart, the output file for the previous code is the input file for the current code for most of the scripts. 

<img width="488" alt="Screen Shot 2024-05-20 at 2 40 22 PM" src="https://github.com/ichen-lab-ucsb/Pacbio-sequencing-library-analysis/assets/52757011/dc0f31eb-99fb-4301-956e-439fc6718c60">

**Flow chart key:**
* Files are numbered 1,2,3…
     * Currently files are omitted until the larger project this is a part of is published.
* Code numbered Code13_, Code14_, …
* Color key:
    * Yellow: .fasta file
    * Green: .txt file
    * Purple: local database for BLAST
    * Red: .png for graph

**Additional notes on steps:**
**Steps 2 & 3:** For BLAST related things, follow the following tutorials:
* For installing: https://www.ncbi.nlm.nih.gov/books/NBK569861/
* For creating local database: https://www.ncbi.nlm.nih.gov/books/NBK569841/
* To perform BLAST sequence alignment: https://www.ncbi.nlm.nih.gov/books/NBK569856/
* To get the BLAST output file in the format used in organizing the data better (folder 2. Organizing results), run the following command:
   blastp -query /Users/…/fastafile.fasta -db /Users/…/database/database -outfmt "6 qseqid sseqid evalue" -out blast_results.txt
BLASTP 2.14.1+ Reference: Stephen F. Altschul, Thomas L. Madden, Alejandro A.
Schaffer, Jinghui Zhang, Zheng Zhang, Webb Miller, and David J.
Lipman (1997), "Gapped BLAST and PSI-BLAST: a new generation of
protein database search programs", Nucleic Acids Res. 25:3389-3402.
Reference for composition-based statistics: Alejandro A. Schaffer,
L. Aravind, Thomas L. Madden, Sergei Shavirin, John L. Spouge, Yuri
I. Wolf, Eugene V. Koonin, and Stephen F. Altschul (2001),
"Improving the accuracy of PSI-BLAST protein database searches with
composition-based statistics and other refinements", Nucleic Acids
Res. 29:2994-3005.
**Step 4:** Used a computing node with 36 CPUs to cut down processing time. 
**Step 6:** Various versions of sampling the data are presented in the repository i.e. sampling for one specific binder versus a list of many binders.



## Reporting bugs:
Please report any bugs to Beatrice Mihalache (beatricemiha@g.ucla.edu).

When reporting bugs please include full output printed in the terminal when running the code.

