// This code is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.
// To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode.
//  PlasmidDatabase.cpp
//  PacBioPlasmidingPlay
//
//  Created by Beatrice Mihalache on 5/9/23.
//

#include "PlasmidDatabase.h"
#include "Plasmid.h"

#include <fstream>
#include <iostream>
#include <string>

using namespace std;

//constructor
PlasmidDatabase::PlasmidDatabase()
{
}

//destructor
PlasmidDatabase::~PlasmidDatabase()
{
    vector<Plasmid*>::iterator it = m_plasmid_database.begin();
    while(it != m_plasmid_database.end()){
        delete *it;
        it = m_plasmid_database.erase(it);
    }
}

//function takes a file and extracts the sequence name and actual sequence for processing
bool PlasmidDatabase::load(const string& filename)
{
    ifstream infile(filename); //loads file
    if( ! infile){
        cerr << "Error" << endl;
        return false;
        //happens when loading a file that does not exist
    }
    
    string plasmid_name;
    string next_plasmid_name;
    string line;
    string sequence = "";
    //string pre_glycine_linker_sequence;
    //string post_glycine_linker_sequence;
    getline(infile, next_plasmid_name);
    while(getline(infile, sequence)){
        //get(infile, sequence, '>');
        plasmid_name = next_plasmid_name;
        while(getline(infile, line) && line[0] != '>'){
            sequence += line;
        }
        next_plasmid_name = line;
        Plasmid* plasmid = new Plasmid(plasmid_name, sequence);
        m_plasmid_database.insert(m_plasmid_database.begin() + m_plasmid_count, plasmid);
        m_plasmid_count++;
        plasmid->check_target_sequence();
        
        sequence = "";
    }
    
    return true;
}

//function prints database
void PlasmidDatabase::print_database(){
    vector<Plasmid*>::iterator it = m_plasmid_database.begin();
    while(it != m_plasmid_database.end()){
        (*it)->print_plasmid();
        it++;
    }
}

//function returns number of protein sequences in the database (valid ones)
int PlasmidDatabase::return_plasmid_count(){
    return m_plasmid_count;
}

/*
 //used as a check
void PlasmidDatabase::print_first_fifty_for_plasmids(){
    vector<Plasmid*>::iterator it = m_plasmid_database.begin();
    string fifty;
    while(it != m_plasmid_database.end()){
        fifty = (*it)->first_fifty();
        cout << fifty << endl;
        it++;
    }
}*/

//sequences marked as not valid are deleted
void PlasmidDatabase::delete_faulty(){
    vector<Plasmid*>::iterator it = m_plasmid_database.begin();
    while(it != m_plasmid_database.end()){
        if( (*it)->get_faulty() == 1 ){
            //cout << "deleting " << (*it)->get_name() << endl;
            delete (*it);
            m_plasmid_count--;
            it = m_plasmid_database.erase(it);
        }
        else{
            it++;
        }
    }
}

//converting DNA sequence to amino acid sequence
void PlasmidDatabase::database_dna_to_amino(){
    vector<Plasmid*>::iterator it = m_plasmid_database.begin();
    while(it != m_plasmid_database.end()){
        cout << (*it)->get_name() << endl;
        (*it)->dna_to_amino();
        it++;
    }
}

//prints contents of database to a file
bool PlasmidDatabase::print_to_text(const std::string& filename1, const std::string& filename2){
    ofstream outputFile(filename1); //loads file
    ofstream oFile(filename2);
    if( !outputFile.is_open() && !oFile.is_open() ){
        cerr << "Error" << endl;
        return false;
        //happens when loading a file that does not exist
    }
    else{
        vector <Plasmid*>::iterator it = m_plasmid_database.begin();
        while(it != m_plasmid_database.end()){
            outputFile << (*it)->get_name() << std::endl;
            outputFile << (*it)->get_amino_acid_sequence() << std::endl;
            if((*it)->get_sequence_length() > 1000 && (*it)->get_sequence_length() < 10000){
                oFile << (*it)->get_name() << std::endl;
                oFile << (*it)->get_amino_acid_sequence() << std::endl;
            }
            it++;
            
        }
        outputFile.close();
        oFile.close();
        return true;
    }
}

