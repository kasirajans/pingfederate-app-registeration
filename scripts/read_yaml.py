import os
import sys
import yaml
import json
import argparse
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
                    
def read_yaml_file(filepath):
    """Reads a YAML file and returns its contents."""
    logging.debug(f"Reading YAML file from: {filepath}")

    # Check if the file is empty
    if os.path.getsize(filepath) == 0:
        logging.warning(f"The file at {filepath} is empty. Skipping.")
        return None  # Return None if the file is empty

    try:
        with open(filepath, 'r') as file:
            data = yaml.safe_load(file)
            if data is None:
                raise ValueError(f"The YAML file at {filepath} is empty or invalid.")
            return data
    except yaml.YAMLError as e:
        logging.debug(f"YAML error while reading {filepath}: {e}")
        return None
    except Exception as e:
        logging.debug(f"Error reading YAML file: {e}")
        return None  # Return None on error

def build_json_structure(yaml_data, folder_hierarchy, global_ticket_numbers, yaml_path):
    """Build a structured JSON from the parsed YAML data."""
    json_output = []
    ticket_numbers_clients = set()  # Track TicketNo for clients in this file

    # Check if the data is a list of entries
    if isinstance(yaml_data, list):
        for entry in yaml_data:
            json_entry = entry if isinstance(entry, dict) else {}

            # Determine if this is a client or ATM entry based on the content of the entry
            if 'TicketNo' in json_entry:
                ticket_no = json_entry['TicketNo']

                # Ensure unique TicketNo across all files
                if ticket_no in global_ticket_numbers:
                    logging.warning(f"Duplicate TicketNo found across files: {ticket_no}. "
                          f"Skipping entry in file: {yaml_path}")
                    continue  # Skip duplicate TicketNo globally
                else:
                    global_ticket_numbers.add(ticket_no)
                    # If it has a name field, prefix with the folder hierarchy
                    if 'name' in json_entry:
                        json_entry['name'] = f"{folder_hierarchy}_{json_entry['name']}"
                    else:
                        # Use the folder hierarchy as the name if not already present
                        json_entry['name'] = f"{folder_hierarchy}"

            json_output.append(json_entry)

    return json_output

def find_yaml_files(base_path, yaml_file):
    """Search for all matching YAML files within the given base path and its subdirectories."""
    matching_files = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.lower() == yaml_file.lower():  # Case insensitive comparison
                matching_files.append(os.path.join(root, file))
    return matching_files

def main():
    parser = argparse.ArgumentParser(description='Process YAML file based on environment.')
    parser.add_argument('--env', required=True, help='The environment (e.g., US_Prod)')
    parser.add_argument('--file', required=True, help='The name of the YAML file')

    args = parser.parse_args()
    env = args.env
    yaml_file = args.file

    # Convert Env US_Prod to US/Prod and format for output filename
    env_path = env.replace("_", "/")
    
    
    
    # Construct the base path from the environment
    base_path = os.path.join(env_path)  # This should point to "US" or "EU"
    logging.debug(f"Searching for YAML file '{yaml_file}' in: {base_path}")

    # Find all YAML files matching the file name
    yaml_paths = find_yaml_files(base_path, yaml_file)

    if not yaml_paths:
        logging.debug(f"No files found: {yaml_file} in {base_path}")
        sys.exit(1)

    # Global set to track TicketNo across all files
    global_ticket_numbers = set()

    # Merge all matching YAML files
    merged_data = []
    for yaml_path in yaml_paths:
        logging.debug(f"Reading YAML file from: {yaml_path}")
        folder_hierarchy = os.path.relpath(os.path.dirname(yaml_path), base_path).replace("/", "_")
        yaml_data = read_yaml_file(yaml_path)

        if yaml_data is None:
            logging.debug(f"Skipping processing for empty or invalid file: {yaml_path}")
            continue

        structured_data = build_json_structure(yaml_data, folder_hierarchy, global_ticket_numbers, yaml_path)
        merged_data.extend(structured_data)

    # Write the merged structured data as JSON to the output file
    file_name = f"{env.lower()}_{yaml_file.split('.')[0].lower()}.json"

    # Get the current working directory
    current_directory = os.getcwd()
    logging.debug(f"Current Directory: {current_directory}")

    # Define the file name and path for the parent directory
    # parent_directory = os.path.join(current_directory, os.pardir)
    output_file = os.path.join(current_directory, file_name.replace("/", "_"))


    # with open(output_file, 'w') as f:
    # First serialization
    json_data = json.dumps(merged_data)
    # Second serialization (this is where the problem occurs)
    # output = json.dumps({"resources": json_data})

    print(json.dumps({"resources": json_data}))
    # print(json.dumps(json.dumps({"resources": merged_data})))
        # json.dump(serilized, f, indent=2)

    logging.debug(f"Structured data written to: {output_file}")

if __name__ == "__main__":
    main()