import json
import subprocess
from collections import defaultdict
from prettytable import PrettyTable
from colorama import Fore, Style, init

# Run the terraform show -json command and capture the output
try:
    result = subprocess.run(
        ["terraform", "show", "-json", "tfplan"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Load the JSON output
    plan_data = json.loads(result.stdout)

    # Initialize dictionaries to store counts of resource changes by type
    to_create = defaultdict(int)
    to_update = defaultdict(int)
    to_delete = defaultdict(int)

    # Iterate through the resource changes
    for resource in plan_data.get("resource_changes", []):
        # Extract the resource type and name from the address
        resource_address = resource.get("address", "")
        
        if "." in resource_address:
            resource_type, resource_name = resource_address.split(".", 1)
        
            # If the resource_type is 'null_resource', use the resource_name as the type
            if resource_type == "null_resource":
                if "[\"" in resource_name:
                    resource_type = resource_name.split('[')[0]

            # Get the actions (create, update, delete) for the resource
            actions = resource.get("change", {}).get("actions", [])

            # Increment counts based on the action
            if "create" in actions:
                to_create[resource_type] += 1
            if "update" in actions:
                to_update[resource_type] += 1
            if "delete" in actions:
                to_delete[resource_type] += 1

    # Resource type to exclude
    exclude_resource_type = "aws_instance"

    # Create a pretty table
    table = PrettyTable()
    table.field_names = ["Resource Type", "To Create", "To Update", "To Delete", "Total Changes"]

    # Get a list of all resource types involved
    all_resource_types = set(to_create.keys()).union(to_update.keys(), to_delete.keys())

    # Prepare the list for sorting by total changes
    sorted_resources = []
    for resource_type in all_resource_types:
        if resource_type != exclude_resource_type:  # Exclude the specific resource type
            create_count = to_create.get(resource_type, 0)
            update_count = to_update.get(resource_type, 0)
            delete_count = to_delete.get(resource_type, 0)
            total_changes = create_count + update_count + delete_count
            sorted_resources.append((resource_type, create_count, update_count, delete_count, total_changes))

    # Sort by total changes (descending order)
    sorted_resources.sort(key=lambda x: x[4], reverse=True)

    # Populate the table with sorted data
    for resource in sorted_resources:
        resource_type, create_count, update_count, delete_count, total_changes = resource
    
        # Determine the color for "To Update" and "To Delete"
        update_color = Fore.GREEN if update_count > 0 else Fore.RESET
        delete_color = Fore.RED if delete_count > 0 else Fore.RESET
        
        # Add the row with colored text
        table.add_row([
            resource_type,
            create_count,
            f"{update_color}{update_count}{Style.RESET_ALL}",
            f"{delete_color}{delete_count}{Style.RESET_ALL}",
            total_changes
        ])

    # Print the table
    print(table)
except subprocess.CalledProcessError as e:
    print(f"Error running terraform command: {e.stderr}")
except json.JSONDecodeError:
    print("Failed to parse the Terraform plan JSON output.")