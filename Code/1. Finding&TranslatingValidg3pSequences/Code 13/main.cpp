// This code is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.
// To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode.
//  main.cpp
//  PacBioSequencingPlay
//
//  Created by Beatrice Mihalache on 5/9/23.
//

#include <iostream>
#include <string>
#include "Plasmid.h"
#include "PlasmidDatabase.h"

using namespace std;

//change to your path names
const string SEQUENCE_DATAFILE = "43member.txt";
//const string SEQUENCE_DATAFILE = "18_member.txt";
//const string SEQUENCE_DATAFILE = "200member.txt";
const string DESIGN_SEQUENCE_DATAFILE = "200member_batch1_to_generate_oligos.txt";

const string OUTPUT_TXT_FILE = "output.txt";
const string OUTPUT_FASTA_FILE = "output.fasta";
const string SIZE_MATTERS_OUTPUT_TXT_FILE = "outputsize.txt";
const string SIZE_MATTERS_OUTPUT_FASTA_FILE = "outputsize.fasta";

int main() {
    PlasmidDatabase plasmid_database;
    bool pb = plasmid_database.load(SEQUENCE_DATAFILE);
    //PlasmidDatabase design_oligo_database;
   // bool ob = design_oligo_database.load(DESIGN_SEQUENCE_DATAFILE);
    cout << "There are " << plasmid_database.return_plasmid_count() << " plasmids in the database." << endl;
    //other methods
   // plasmid_database.print_longest_substring();
   // plasmid_database.print_longest_common_subsequence();
    //plasmid_database.print_dynamic_longest_common_subsequence();
    //plasmid_database.print_database();
    
    plasmid_database.delete_faulty();
    cout << "There are now " << plasmid_database.return_plasmid_count() << " plasmids in the database." << endl;
   // plasmid_database.print_first_fifty_for_plasmids();
    plasmid_database.database_dna_to_amino();
    
    cout << "this is the plasmid database: " << endl;
    plasmid_database.print_database();
    
    plasmid_database.print_to_text(OUTPUT_FASTA_FILE, SIZE_MATTERS_OUTPUT_FASTA_FILE);
}
