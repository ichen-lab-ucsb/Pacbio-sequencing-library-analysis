// This code is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.
// To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode.
//  PlasmidDatabase.h
//  PacBioSequencingPlay
//
//  Created by Beatrice Mihalache on 5/9/23.
//

#ifndef PlasmidDatabase_h
#define PlasmidDatabase_h

#include <string>
#include <unordered_set>
#include <vector>

class Plasmid;

class PlasmidDatabase
{
public:
    PlasmidDatabase();
    ~PlasmidDatabase();
    bool load(const std::string& filename);
    int return_plasmid_count();
    
    void print_first_fifty_for_plasmids();
    void delete_faulty(); // delete nonsense plasmid sequences i.e. too short, too long
    void print_database();
    
    void database_dna_to_amino();
    
    bool print_to_text(const std::string& filename1, const std::string& filename2);
    
private:
    //std::unordered_set<Plasmid*> m_plasmid_database;
    std::vector<Plasmid*> m_plasmid_database;
    std::vector<Plasmid*> m_oligo_database;
    int m_plasmid_count = 0;
};

#endif /* splitIntog3p_hpp */
