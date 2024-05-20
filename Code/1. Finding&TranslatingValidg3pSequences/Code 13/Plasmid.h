// This code is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.
// To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode.
//  Plasmid.hpp
//  PacBioSequencingPlay
//
//  Created by Beatrice Mihalache on 5/14/23.
//

#ifndef Plasmid_h
#define Plasmid_h

#include <stdio.h>
#include <string>
#include <iostream>
#include <unordered_map>
#include <map>
#include <algorithm>

//glycine linker
const std::string G3P_SEQUENCE = "GGCGGCGGCTGG";
//amino acids

const std::unordered_map<std::string, char> CODON_TABLE = {
    {"TTT", 'F'}, {"TTC", 'F'}, {"TTA", 'L'}, {"TTG", 'L'},
    {"CTT", 'L'}, {"CTC", 'L'}, {"CTA", 'L'}, {"CTG", 'L'},
    {"ATT", 'I'}, {"ATC", 'I'}, {"ATA", 'I'}, {"ATG", 'M'},
    {"GTT", 'V'}, {"GTC", 'V'}, {"GTA", 'V'}, {"GTG", 'V'},
    {"TCT", 'S'}, {"TCC", 'S'}, {"TCA", 'S'}, {"TCG", 'S'},
    {"CCT", 'P'}, {"CCC", 'P'}, {"CCA", 'P'}, {"CCG", 'P'},
    {"ACT", 'T'}, {"ACC", 'T'}, {"ACA", 'T'}, {"ACG", 'T'},
    {"GCT", 'A'}, {"GCC", 'A'}, {"GCA", 'A'}, {"GCG", 'A'},
    {"TAT", 'Y'}, {"TAC", 'Y'}, {"TAA", 'X'}, {"TAG", 'X'},
    {"CAT", 'H'}, {"CAC", 'H'}, {"CAA", 'Q'}, {"CAG", 'Q'},
    {"AAT", 'N'}, {"AAC", 'N'}, {"AAA", 'K'}, {"AAG", 'K'},
    {"GAT", 'D'}, {"GAC", 'D'}, {"GAA", 'E'}, {"GAG", 'E'},
    {"TGT", 'C'}, {"TGC", 'C'}, {"TGA", 'X'}, {"TGG", 'W'},
    {"CGT", 'R'}, {"CGC", 'R'}, {"CGA", 'R'}, {"CGG", 'R'},
    {"AGT", 'S'}, {"AGC", 'S'}, {"AGA", 'R'}, {"AGG", 'R'},
    {"GGT", 'G'}, {"GGC", 'G'}, {"GGA", 'G'}, {"GGG", 'G'}
};

//using this letter code for amino acids: https://www.hgmd.cf.ac.uk/docs/cd_amino.html


class Plasmid
{
public:
    Plasmid(const std::string& name, const std::string& sequence);
    //getter methods
    std::string get_name() const;
    std::string get_entire_sequence() const;
    int get_sequence_length();
    std::string get_amino_acid_sequence() const;
    
    void return_aa_count();
    void print_plasmid();
    bool return_base_count();
    void print_base_count();
    std::string longest_target_subsequence(const std::string& targetsequence, const std::string& sequence);
    
    bool check_target_sequence();
    bool shorten_to_g3pplusPAMA();
    void complement(std::string& sequence, std::string& newsequence, int i);
    bool reverse_and_complement_sequence();
    bool remove_PAMA();
    bool check_frame();
    std::string codon_to_aa(const std::string& codon);
    bool generate_aa();
    bool dna_to_amino();
    
    
    bool check_reverse_sequence(); //returns true if need to reverse, false if sequence is forward
    
    void reverse_sequence();
    
    static bool compare1(const Plasmid* a, const Plasmid* b) {
        return a->m_sequence.size() < b->m_sequence.size();
    }
    static bool compare2(const Plasmid* a, const Plasmid* b) {
        return a->m_g3p_sequence.size() < b->m_g3p_sequence.size();
    }
    
    bool target_sequences_g3p_PAMA();
    bool removing_PAMA();
    std::string get_g3p_sequence() const; 
    //get sequence g3p protein
    
    std::string first_fifty();
    int get_faulty();
    
    int levinstein_distance(std::string& target, std::string& sequence);
    
private:
    std::string m_name;
    std::string m_sequence;
    
    std::string m_has_sequence_error;
    //std::string m_protein_sequence = "";
    int m_sequence_length;
    std::unordered_map<char, int> m_aa_count = {
        {'A', 0}, {'C', 0}, {'D', 0}, {'E', 0}, {'F', 0},
        {'G', 0}, {'H', 0}, {'I', 0}, {'K', 0}, {'L', 0},
        {'M', 0}, {'N', 0}, {'P', 0}, {'Q', 0}, {'R', 0},
        {'S', 0}, {'T', 0}, {'V', 0}, {'W', 0}, {'X', 0},
        {'Y', 0}
    };
    std::map<char, int> m_base_count = {
        {'A', 0}, {'T', 0}, {'C', 0}, {'G', 0}
    };
    
    //PAMA
    std::string target_forward_PAMA = "CCGGCCATGGCT";
    
    //GlycineLinker + Age1
    std::string target_forward_downstream = "GGCGGCGGCACCGGTGGTGGT";
    std::string target_reverse_downstream = "ACCACCACCGGTGCCGCCGCC";
    
    bool forward = false;
    bool reverse = false;
    bool contains_target_downstream;
    std::size_t m_found = std::string::npos;
    
    
    std::string m_forward_downstream; //how much of target_downstream m_sequence contains
    std::string m_reverse_downstream;
    std::string m_downstream;
    int downstream_lev_distance;
    std::string lev_target_string;
    int reverses = 0; // 1 if reverse, 0 if forward
    
    std::string m_g3p_sequence_PAMA; //g3p with part of PAMA
    std::string m_g3p_sequence; //this is the part of the sequence we are interested in
    std::string m_amino_acid_sequence = "";
    
    std::string m_first_fifty_bases;
    
    int m_faulty = 0; // if string is faulty, will change to 1
};

#endif /* Plasmid_hpp */
