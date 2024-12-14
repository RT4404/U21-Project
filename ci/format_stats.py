#!/usr/bin/env python3
import os
import re
import csv
import argparse

# Function to collect the data
def collect_data(log_folder, target_metric):
    collected_data = []

    # Ensure the folder exists
    if not os.path.exists(log_folder):
        print(f"Error: Folder {log_folder} does not exist.")
        return collected_data

    # Common string patterns that accompany metrics
    # Metrics from individual cores e.g. PERF: core0: icache reads=8850
    core_pattern = re.compile(rf"PERF: core(\d+):.*{target_metric}=(\S+)")

    # Overall metrics (not tied to individual cores) e.g. PERF: memory latency=65 cycles
    normal_pattern = re.compile(rf"PERF: .*{target_metric}=(\S+)")

    # Iterate through the folders for the desired results in log_folder
    for root, _, files in os.walk(log_folder):
        # Go through all the files
        for file in files:
            filepath = os.path.join(root, file)
            file_metrics = {"file": file}
            # Go line by line in the log file
            with open(filepath, 'r') as f:
                # Collect data line by line that matches target_metric
                for line in f:
                    # Match for core metrics
                    core_match = core_pattern.search(line)
                    if core_match:
                        core_id, value = core_match.groups()
                        file_metrics[f"core{core_id}_{target_metric}"] = value

                    # Match for non-core metrics
                    normal_match = normal_pattern.search(line)
                    if normal_match:
                        value = normal_match.group(1)
                        file_metrics[f"{target_metric}"] = value

            # Gather all the collected data into the array
            collected_data.append(file_metrics)

    return collected_data

# Function to create CSV file
def save_to_csv(collected_data, output_file):
    # Collect all unique column names
    columns = set()
    for data in collected_data:
        columns.update(data.keys())

    # Ensure 'file' is the first column, followed by the rest in sorted order
    columns = ['file'] + sorted(col for col in columns if col != 'file')

    # Write data to CSV
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        writer.writerows(collected_data)

    print(f"Metrics saved to {output_file}")


# Main
def main():
    parser = argparse.ArgumentParser(description="Extract metrics from log files across multiple folders and save them into a single CSV.")
    parser.add_argument("log_folders", nargs='+', help="Paths to the folders containing log files. You can specify multiple folders.")
    parser.add_argument("target_metric", help="The target metric to extract (e.g., IPC).")
    args = parser.parse_args()

    # Ensure the output folder exists
    output_folder = "CSV_results"
    os.makedirs(output_folder, exist_ok=True)

    # Generate the output file name dynamically
    combined_folders = "_".join([os.path.basename(os.path.normpath(folder)) for folder in args.log_folders])
    output_file = os.path.join(output_folder, f"{combined_folders}_{args.target_metric}_metrics.csv")

    # Collect data from all provided folders
    all_collected_data = []
    for log_folder in args.log_folders:
        collected_data = collect_data(log_folder, args.target_metric)
        all_collected_data.extend(collected_data)

    # Save all the data to a single CSV file
    save_to_csv(all_collected_data, output_file)


if __name__ == "__main__":
    main()
