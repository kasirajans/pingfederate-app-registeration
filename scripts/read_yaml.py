import os
import yaml
import json
import sys
import logging

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("processing.log"),
        logging.StreamHandler()
    ]
)

def load_yaml_file(filepath):
    """Helper function to load a YAML file"""
    logging.debug(f"Attempting to load YAML file: {filepath}")
    try:
        with open(filepath, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        logging.error(f"Failed to load YAML file: {filepath}, error: {e}")
        raise

def generate_pfname_only(data, relative_path, domain_name):
    """Generate 'pfname' based on the folder structure"""
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                if relative_path == '.':
                    relative_path = domain_name.lower()
                relative_path = relative_path.strip('_')

                # Append 'name' if it exists, or use relative_path alone
                if 'name' in item and item['name']:
                    item['pfname'] = f"{relative_path}_{item['name'].lower()}"
                else:
                    item['pfname'] = relative_path

                logging.debug(f"Generated pfname: {item['pfname']}")

    return data

def generate_description_from_appconfig(app_config):
    """Generate description from the appConfig.yaml contacts"""
    contacts = app_config.get('contacts', {})
    business_owner_email = contacts.get('business_owner_email_id', [''])[0]
    technical_owner_email = ",".join(contacts.get('technial_owner_email_id', []))
    team_pdl_email = contacts.get('team_pdl_email_id', [''])[0]
    return f"{business_owner_email}:{technical_owner_email}:{team_pdl_email}"

def generate_client_description(client, app_config):
    """Generate description for client based on appConfig.yaml"""
    contacts_description = generate_description_from_appconfig(app_config)
    ticket_no = client.get('TicketNo', '')
    internal_or_external = client.get('InternalOrExternal', '')
    is_partner = client.get('IsPartner', '')
    safe_name = client.get('SafeName', '')
    return f"{ticket_no}:{contacts_description}:{internal_or_external}:{is_partner}:{safe_name}"

def check_unique_ticketno(data, ticketnos, file_path, entry_type):
    """Ensure TicketNo is unique, log duplicates"""
    valid_entries = []
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and 'TicketNo' in item:
                ticketno = item['TicketNo']
                if ticketno in ticketnos:
                    logging.error(f"Duplicate TicketNo found in {entry_type}: {ticketno} in file: {file_path}. Skipping.")
                    continue  # Skip duplicates
                logging.debug(f"TicketNo is unique: {ticketno}")
                ticketnos.add(ticketno)
                valid_entries.append(item)  # Add non-duplicate entries
    return valid_entries

def merge_and_deduplicate_scopes(atm_entries):
    """Merge and deduplicate scopes in ATM entries"""
    all_scopes = []
    scope_sources = {}

    for atm in atm_entries:
        if 'scopes' in atm:
            for scope in atm['scopes']:
                if scope in scope_sources:
                    scope_sources[scope].append(atm.get('file_path', 'Unknown file'))
                else:
                    scope_sources[scope] = [atm.get('file_path', 'Unknown file')]
                all_scopes.append(scope)

    unique_scopes = list(set(all_scopes))
    if len(unique_scopes) < len(all_scopes):
        duplicate_scopes = set([scope for scope in all_scopes if all_scopes.count(scope) > 1])
        for scope in duplicate_scopes:
            logging.warning(f"Duplicate scope '{scope}' found in files: {', '.join(scope_sources[scope])}")

    return unique_scopes

def process_directory(region, env, base_path, domain_path, domain_name, current_dir, ticketnos, combined_data):
    """Process all directories and files under the domain"""
    individual_data = {
        'ATM': [],
        'clients': []
    }

    for root, dirs, files in os.walk(domain_path):
        logging.debug(f"Processing directory: {root}")

        # Find relevant YAML files in the current folder
        atm_file = os.path.join(root, 'ATM.yaml')
        clients_file = os.path.join(root, 'clients.yaml')
        app_config_file = os.path.join(root, 'appConfig.yaml')

        # Ensure appConfig.yaml exists
        if not os.path.exists(app_config_file):
            logging.warning(f"Skipping {root}: appConfig.yaml not found.")
            continue  # Skip if appConfig.yaml is missing

        # Load appConfig.yaml
        app_config = load_yaml_file(app_config_file)
        atm_description = generate_description_from_appconfig(app_config)

        # Calculate relative path and folder level
        relative_path = os.path.relpath(root, base_path).replace(os.sep, '_').lower()
        folder_level = relative_path.count('_') + 1  # Calculate folder level

        # Load and process ATM.yaml
        if os.path.exists(atm_file):
            atm_data = load_yaml_file(atm_file)
            for atm in atm_data:
                atm['description'] = atm_description
                atm['file_path'] = atm_file  # Add file path to each ATM entry
                atm['folder_level'] = folder_level  # Add folder level to each ATM entry
            valid_atm_entries = check_unique_ticketno(atm_data, ticketnos, atm_file, 'ATM')
            valid_atm_entries = generate_pfname_only(valid_atm_entries, relative_path, domain_name)
            individual_data['ATM'].extend(valid_atm_entries)
            combined_data['ATM'].extend(valid_atm_entries)

        # Load and process clients.yaml
        if os.path.exists(clients_file):
            clients_data = load_yaml_file(clients_file)
            for client in clients_data:
                client['description'] = generate_client_description(client, app_config)
                client['file_path'] = clients_file  # Add file path to each client entry
                client['folder_level'] = folder_level  # Add folder level to each client entry
            valid_clients_entries = check_unique_ticketno(clients_data, ticketnos, clients_file, 'clients')
            valid_clients_entries = generate_pfname_only(valid_clients_entries, relative_path, domain_name)
            individual_data['clients'].extend(valid_clients_entries)
            combined_data['clients'].extend(valid_clients_entries)

    # Merge and deduplicate scopes in combined_data['ATM']
    combined_data['scopes'] = merge_and_deduplicate_scopes(combined_data['ATM'])

    # Create individual JSON file for the processed domain
    if individual_data['ATM'] or individual_data['clients']:
        individual_output_file = os.path.join(current_dir, f"{region}_{env}_{domain_name}_output.json")
        try:
            with open(individual_output_file, 'w') as json_file:
                json.dump(individual_data, json_file, indent=4)
            logging.info(f"Individual JSON file created: {individual_output_file}")
        except Exception as e:
            logging.error(f"Failed to create individual JSON file: {individual_output_file}, error: {e}")
            raise

def convert_to_json(env, region, domain=None):
    """Convert YAML to JSON for all directories"""
    base_path = os.path.abspath(os.path.join(os.getcwd(), region, env))
    current_dir = os.getcwd()  # Get current working directory
    ticketnos = set()  # Track unique TicketNo

    logging.info(f"Starting conversion for {region}/{env} with domain {domain or 'all domains'}")
    logging.info(f"Current working directory: {current_dir}")
    logging.info(f"Base path: {base_path}")

    # Initialize the combined data structure
    combined_data = {
        'ATM': [],
        'clients': [],
        'scopes': []
    }

    # Check if the base path exists
    if not os.path.exists(base_path):
        logging.error(f"Base path does not exist: {base_path}")
        merged_output_file = os.path.join(current_dir, f"{region}_{env}_merged_output.json") # Create an empty merged JSON file
        try:
            with open(merged_output_file, 'w') as json_file:
                json.dump(combined_data, json_file, indent=4)
            logging.info(f"Empty merged JSON file created: {merged_output_file}")
        except Exception as e:
            logging.error(f"Failed to create empty merged JSON file: {merged_output_file}, error: {e}")
        return  # Exit the function after creating the empty JSON file

    # Process all domains if no specific domain is passed
    domains = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]

    if domain and domain in domains:
        # If a specific domain is passed, process only that domain
        domains = [domain]

    for domain in domains:
        domain_path = os.path.join(base_path, domain)
        if not os.path.exists(domain_path):
            logging.warning(f"Skipping {domain_path}: Domain path not found.")
            continue

        try:
            process_directory(region, env, base_path, domain_path, domain, current_dir, ticketnos, combined_data)
        except Exception as e:
            logging.error(f"Error processing {domain_path}: {e}")
            continue  # Log the error and continue processing other domains

    # Create the final merged JSON output file
    merged_output_file = os.path.join(current_dir, f"{region}_{env}_merged_output.json")
    try:
        with open(merged_output_file, 'w') as json_file:
            json.dump(combined_data, json_file, indent=4)
        logging.info(f"Merged JSON file created: {merged_output_file}")
    except Exception as e:
        logging.error(f"Failed to create merged JSON file: {merged_output_file}, error: {e}")
        raise

    logging.info(f"Finished processing {region}/{env}")

if __name__ == "__main__":
    # Example arguments: US Prod Inventory or just US Prod
    if len(sys.argv) < 3:
        logging.error("Usage: python script.py <Region> <Environment> [<Domain>]")
        sys.exit(1)

    region = sys.argv[1]  # US or EU
    env = sys.argv[2]     # Prod, UAT, Dev, etc.
    domain = sys.argv[3] if len(sys.argv) == 4 else None  # Optional domain

    try:
        convert_to_json(env, region, domain)
        print("Processing completed successfully.")
    except Exception as e:
        logging.error(f"Error during processing: {e}")
        sys.exit(1)