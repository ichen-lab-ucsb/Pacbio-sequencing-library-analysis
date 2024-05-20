# This code is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode.

import numpy as np
def main():
    data = {}
    
    with open("/Users/chenlab/Desktop/blastcodetesting/filtered43_e_PA_binder.txt", "r") as input_file:
        for line in input_file:
            query, subject, e_value = line.strip().split("\t")
            e_value = float(e_value)
            
            # Check if the query is already in data with a higher e-value
            if query not in data or data[query]["e_value"] > e_value:
                data[query] = {"subject": subject, "e_value": e_value}

    # Now, data contains only the lowest e-value for each unique query sequence
    # Convert data dictionary to a list of its values for sorting and statistics
    unique_results = list(data.values())
    
    # Sort the results based on e-value in increasing order
    sorted_results = sorted(unique_results, key=lambda x: x["e_value"])

    e_values = [result["e_value"] for result in sorted_results]  # Extract all e-values for statistics

    def calculate_median(values):
        sorted_values = sorted(values)
        length = len(sorted_values)
        if length % 2 == 1:  # If odd
            # The median is the middle number
            return sorted_values[length // 2]
        else:  # If even
            # The median is the average of the two middle numbers
            return (sorted_values[length // 2 - 1] + sorted_values[length // 2]) / 2


    '''
    with open("/Users/chenlab/Desktop/blastcodetesting/43PA-bindertophits.txt", "w") as output_file:
        for query, result in data.items():
            output_file.write(f"Query: {query}\tSubject: {result['subject']}\tE-value: {result['e_value']}\n")
    '''
    with open("/Users/chenlab/Desktop/blastcodetesting/18PA-bindertophits.txt", "w") as output_file:
        for result in sorted_results:  # Iterate over sorted results based on e-value
            # Find the query corresponding to each sorted result
            query = [key for key, value in data.items() if value == result][0]
            # Write sorted results to the file
            output_file.write(f"Query: {query}\tSubject: {result['subject']}\tE-value: {result['e_value']}\n")

    # Calculate statistics
    average_e_value = sum(e_values) / len(e_values)
    min_e_value = min(e_values)
    max_e_value = max(e_values)
    median_e_value = calculate_median(e_values)


    print(f"Total number of unique query sequences: {len(sorted_results)}")
    print(f"Average E-value: {average_e_value:.2e}")
    print(f"Minimum E-value: {min_e_value:.2e}")
    print(f"Maximum E-value: {max_e_value:.2e}")
    print(f"Median E-value: {median_e_value:.2e}")

    # Filtering for e-values less than 0.1
    smaller_e_values = [e_value for e_value in e_values if e_value < 0.1]
    if smaller_e_values:
        average_min_e_value = sum(smaller_e_values) / len(smaller_e_values)
        min_min_e_value = min(smaller_e_values)
        max_min_e_value = max(smaller_e_values)
        median_e_value = calculate_median(smaller_e_values)

        print(f"Number of query sequences with e-value less than 0.1: {len(smaller_e_values)}")
        print(f"Average E-value for sequences with e-value < 0.1: {average_min_e_value:.2e}")
        print(f"Minimum E-value for sequences with e-value < 0.1: {min_min_e_value:.2e}")
        print(f"Maximum E-value for sequences with e-value < 0.1: {max_min_e_value:.2e}")
        print(f"Median E-value for sequences with e-value < 0.1:: {median_e_value:.2e}")
    else:
        print("No query sequences with e-value less than 0.1.")

    # Calculate quartiles
    Q1 = np.percentile(e_values, 25)
    # Filter for Q1
    q1_results = [result for result in sorted_results if result["e_value"] <= Q1]

    # Write Q1 results to a new file
    with open("/Users/chenlab/Desktop/blastcodetesting/43PA-BinderQ1.txt", "w") as output_file:
        for result in q1_results:
            # Find the query corresponding to each sorted result
            query = [key for key, value in data.items() if value == result][0]
            output_file.write(f"Query: {query}\tSubject: {result['subject']}\tE-value: {result['e_value']}\n")

    print(f"First Quartile (Q1) E-value: {Q1:.2e}")
    print(f"Total number of unique query sequences in Q1: {len(q1_results)}")


if __name__ == "__main__":
    main()
