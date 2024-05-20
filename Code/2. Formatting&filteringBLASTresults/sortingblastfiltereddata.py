# This code is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode.

def main():
    data = {}
    filtereddata = {}

    with open("/Users/chenlab/Desktop/blastcodetesting/filteredblast_leastusedrefseq.txt", "r") as input_file:
        for line in input_file:
            query, subject, e_value = line.strip().split("\t")
            e_value = float(e_value)

            if query not in data:
                data[query] = []

            data[query].append({"subject": subject, "e_value": e_value})

    num_queries = len(data)  # Count the number of query sequences
    total_min_e_values = []  # Store minimum E-values for computing average later

    for query, results in data.items():
        sorted_results = sorted(results, key=lambda x: x["e_value"])
        filtered_results = []

        for result in sorted_results:
            if len(filtered_results) < 6 or result["e_value"] < 1e-10:
                if len(filtered_results) < 6:
                    filtered_results.append(result)

        if filtered_results:
            filtereddata[query] = filtered_results
            total_min_e_values.append(filtered_results[0]["e_value"])  # Store the minimum E-value for average
    
    with open("/Users/chenlab/Desktop/blastcodetesting/leastusedreftop3blastresults.txt", "w") as output_file:
        for query, results in filtereddata.items():
            output_file.write(f"Query: {query}\n")
            for result in results:
                subject = result["subject"]
                e_value = result["e_value"]
                output_file.write(f"Subject: {subject}\tE-value: {e_value}\n")
            output_file.write("\n")

    # Calculate statistics
    print(total_min_e_values)
    average_min_e_value = sum(total_min_e_values) / len(total_min_e_values)
    min_min_e_value = min(total_min_e_values)
    max_min_e_value = max(total_min_e_values)

    print(f"Number of query sequences: {num_queries}")
    print(f"Average minimum E-value: {average_min_e_value:.2e}")
    print(f"Minimum minimum E-value: {min_min_e_value:.2e}")
    print(f"Maximum minimum E-value: {max_min_e_value:.2e}")

    smaller_min_e_values = []
    for e_value in total_min_e_values:
        if(e_value < 0.1):
            smaller_min_e_values.append(e_value)

    average_min_e_value = sum(smaller_min_e_values) / len(smaller_min_e_values)
    min_min_e_value = min(smaller_min_e_values)
    max_min_e_value = max(smaller_min_e_values)

    num_elements = len(smaller_min_e_values)
    print(f"Number of query sequences w e-value less than 0.1: {num_elements}")
    print(f"Average minimum E-value: {average_min_e_value:.2e}")
    print(f"Minimum minimum E-value: {min_min_e_value:.2e}")
    print(f"Maximum minimum E-value: {max_min_e_value:.2e}")




    #print(data)

if __name__ == "__main__":
    main()
