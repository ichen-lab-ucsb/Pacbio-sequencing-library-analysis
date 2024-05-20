// This code is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.
// To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode.
//  Plasmid.cpp
//  PacBioSequencingPlay
//
//  Created by Beatrice Mihalache on 5/14/23.
//

#include "Plasmid.h"
#include <string>
#include <iostream>
#include <algorithm>
#include <vector>

using namespace std;

//constructor
Plasmid::Plasmid(const string& name, const string& sequence) : m_name(name), m_sequence(sequence)
{
    m_sequence_length = m_sequence.length();
    /*if(m_sequence_length < 1000 || m_sequence_length > 10000){
        m_faulty = 1;
        //this means that this sequence is too long or too short and should be removed from the sequence
    }*/
}

//returns the name of sequence
string Plasmid::get_name() const
{
    return m_name;
}

//returns the entire sequence
string Plasmid::get_entire_sequence() const
{
    return m_sequence;
}

//returns the sequence length
int Plasmid::get_sequence_length()
{
    return m_sequence_length;
}

//given a sequence, the longest subsequence is found
string Plasmid::longest_target_subsequence(const std::string& targetsequence, const std::string& sequence) {
    int len1 = sequence.length();
    int len2 = targetsequence.length();
    std::vector<std::vector<int>> dp(len1 + 1, std::vector<int>(len2 + 1, 0));
    int maxLen = 0;
    int endIndex = 0;
    
    for (int i = 1; i <= len1; ++i) {
        for (int j = 1; j <= len2; ++j) {
            if (sequence[i - 1] == targetsequence[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
                if (dp[i][j] > maxLen) {
                    maxLen = dp[i][j];
                    endIndex = i - 1;
                }
            }
        }
    }
    return sequence.substr(endIndex - maxLen + 1, maxLen);
}

//checking for the downstream sequence and figuring out if sequence was sequenced in forward or reverse
bool Plasmid::check_target_sequence(){
    //checks if forward or reverse target sequence is in
    m_found = m_sequence.find(target_forward_downstream);
    if (m_found != std::string::npos){
        forward = true;
        reverse = false;
        contains_target_downstream = true;
        return true;
    }
    m_found = m_sequence.find(target_reverse_downstream);
    if(m_found != std::string::npos){
        reverse = true;
        contains_target_downstream = true;
        return true;
    }
    m_faulty = 1;
    contains_target_downstream = false;
    return false;
}

//removes the downstream sequence and everything after
bool Plasmid::shorten_to_g3pplusPAMA(){
    if(m_found != std::string::npos){
        if(forward == true)
            m_g3p_sequence_PAMA = m_sequence.substr(0, m_found + target_forward_downstream.length());
        else if(reverse == true){
            //size_t length1 = m_sequence.length() - m_found - 1;
            //m_g3p_sequence_PAMA = m_sequence.substr(m_found, m_sequence.length() - m_found);  //if reverse want from sequence until the end
            m_g3p_sequence_PAMA = m_sequence.substr(m_found, m_sequence.length() - m_found);
        }
        return true;
    }
    return false;
}

//complement base function
void Plasmid::complement(string& sequence, string& newsequence, int i){
    if(sequence[i] == 'A')
        newsequence += 'T';
    if(sequence[i] == 'T')
        newsequence += 'A';
    if(sequence[i] == 'G')
        newsequence += 'C';
    if(sequence[i] == 'C')
        newsequence += 'G';
    else
        newsequence = newsequence;
}

//if the sequence is in reverse then it is normalized to be not reversed and complemented
bool Plasmid::reverse_and_complement_sequence(){
    //if contains_target_downstream is false then the sequence should be removed from the database...
    if(reverse == true){
        string complements = "";
        for(int i = 0; i < m_g3p_sequence_PAMA.length(); i++){
            complement(m_g3p_sequence_PAMA, complements, i);
        }
        string unreverse = "";
        for(int i = complements.length(); i >= 0; i--){
            unreverse += complements[i];
        }
        m_g3p_sequence_PAMA = unreverse;
        return true;
    }
    return false;
}

//this method removes the signal peptide PAMA
bool Plasmid::remove_PAMA(){
    //only need to check target_forward_PAMA because reverse_and_complement_sequence()
    //this method is called in check frame
    int length = 13; // PAMA is 12 nucleotides long
    int difference  = 0;
    string first_part;
    string substr_PAMA;
    while(length > 0){
        first_part = m_g3p_sequence_PAMA.substr(1,length-1);
        //first_part = m_g3p_sequence_PAMA.substr(0,length);
        substr_PAMA = target_forward_PAMA.substr(difference);
        if(first_part == substr_PAMA){
            if(length == 1){
                if(m_g3p_sequence_PAMA.length() % 3 == 0){
                    m_g3p_sequence = m_g3p_sequence_PAMA;
                    return false;
                }
            }
            m_g3p_sequence = m_g3p_sequence_PAMA.substr(length);
            return true;
        }
        length--;
        difference++;
    }
    m_g3p_sequence = m_g3p_sequence_PAMA;
    return false;
}

//checks if the sequence is in frame i.e. can be converted to amino acid sequence
bool Plasmid::check_frame(){
    int mod = m_g3p_sequence.length() % 3;
    if(mod == 0){
        return true;
    }
    else{
        m_g3p_sequence = m_g3p_sequence.substr(mod);
        return false;
    }
}

//now ready to convert to amino acid
//generate amino acid from codon
string Plasmid::codon_to_aa(const string& codon) {
    auto iter = CODON_TABLE.find(codon);
    if (iter != CODON_TABLE.end()) {
        //to count number of each amino acid
        char aa = iter->second;
        auto iter2 = m_aa_count.find(aa);
        if(iter2 != m_aa_count.end()){
            iter2->second++;
        }
        return std::string(1, iter->second); //returns string on length one with the letter in the map to add to string of amino acids in function generate_aa()
    } else {
        return "!"; // unknown amino acid
    }
}

//generate amino acid sequence from DNA sequence
bool Plasmid::generate_aa(){
    string codon;
   // cout << m_g3p_sequence.length() << endl;
    for (size_t i = 0; i < m_g3p_sequence.length() - 2; i += 3) {
        if (i + 2 < m_g3p_sequence.length()) {
            codon = m_g3p_sequence.substr(i, 3);
            string s = codon_to_aa(codon);
            if( s == "!" ){
                m_g3p_sequence.substr(1);
                i = 0;
            }
            else
                m_amino_acid_sequence += codon_to_aa(codon);
        } else {
            //handle the case when there are fewer than 3 characters left
            //cout << "format error" << endl;
        }
    }
    if(m_amino_acid_sequence.length() > 0){
        return true;
    }
    return false;
}

//returns the amino acid sequence
string Plasmid::get_amino_acid_sequence() const{
    return m_amino_acid_sequence;
}

//actually converts DNA sequence to amino acid sequence
bool Plasmid::dna_to_amino(){
    //check_target_sequence();
    if(m_found != std::string::npos){
        shorten_to_g3pplusPAMA();
        reverse_and_complement_sequence();
        remove_PAMA();
        check_frame();
        generate_aa();
        return true;
    }
    return false;
}

//prints out number of each amino acid
void Plasmid::return_aa_count(){
    auto iter = m_aa_count.begin();
    while(iter != m_aa_count.end()){
        cout << iter->first << ": " << iter->second << ", ";
        iter++;
    }
    cout << endl;
}

//counts the number of different bases
bool Plasmid::return_base_count(){
    for(int i = 0; i < m_sequence_length; i++){
        auto iter = m_base_count.find(m_sequence[i]);
        if(iter != m_base_count.end()){
            iter->second++;
        }
        else{
            cout << "Unidentified base pair" << endl;
        }
    }
    return true;
}

//prints base count
void Plasmid::print_base_count(){
    auto iter = m_base_count.begin();
    while(iter != m_base_count.end()){
        cout  << iter->first << ": " << iter->second << endl;
        iter++;
    }
}

//returns the valid or faulty status of sequence
int Plasmid::get_faulty(){
    return m_faulty;
}


//prints plasmid information
void Plasmid::print_plasmid()
{
    cout << "Name: " << m_name << endl;
    //cout << "Sequence: " << endl << m_sequence << endl;
    cout << "Sequence length: " << m_sequence_length << endl;
    dna_to_amino();
    if(m_found != std::string::npos){
        cout << "PAMA + g3p sequence: " << m_g3p_sequence_PAMA << endl;
        cout << "g3p sequence: " << m_g3p_sequence << endl;
        cout << "g3p sequence length: " << m_g3p_sequence.length() << endl;
        cout << "amino acid sequence " << m_amino_acid_sequence << endl;
    }
}

