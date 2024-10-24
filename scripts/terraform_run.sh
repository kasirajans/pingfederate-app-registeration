#!/bin/bash

# Function to run Terraform commands
run_terraform() {
    local command=$1 #Plan
    local env=$2  #US/Prod
    local file_type=$3 #clients.yaml
    export TF_LOG=
    # Convert env from US/Prod to US_PROD
    local formatted_env=$(echo "$env" | tr '/' '_')
    envtfvars=$(echo "$env" | tr '[:upper:]' '[:lower:]' | sed 's/\//./').tfvars
    echo $output_string  # Output: us.prod.tfvars
    echo $command
    echo "Original env: $env"
    echo "Formatted env: $formatted_env"
    echo $file_type

    # Determine the state and plan file names based on parameters
    local state_file="${formatted_env}_${file_type%.yaml}_state.tfstate"
    local plan_file="${formatted_env}_${file_type%.yaml}_plan.tfplan"
    
    # Print what we are about to do for clarity
    echo "Running Terraform $command for $file_type in $env."
    echo "Using state file: $state_file"
    echo "Using plan file: $plan_file"

    # Initialize Terraform with the specified state file
    terraform init
    

    # Run Terraform plan or apply based on the command
    case "$command" in
        PlanAndApply)
# Run terraform plan and capture the exit status
terraform plan -state="$state_file" -out="$plan_file" -var="env=$formatted_env" -var="yaml_file=$file_type" -var-file=$envtfvars
# Check if the terraform plan was successful
if [ $? -eq 0 ]; then
    echo "Terraform plan was successful, proceeding to apply..."
    
    # Run terraform apply
    terraform apply -state="$state_file" $plan_file
    
    # Check if terraform apply was successful
    if [ $? -eq 0 ]; then
        # If apply was successful, delete the .tfplan file
        rm -f $plan_file
        echo "Plan file deleted successfully."
    else
        echo "Terraform apply failed, plan file not deleted."
    fi
else
    echo "Terraform plan failed, skipping apply."
fi
            ;;
        destroy)
            terraform destroy -state="$state_file" -var="env=$formatted_env"
            ;;
        *)
            echo "Invalid command. Use 'plan', 'apply', or 'destroy'."
            exit 1
            ;;
    esac
}

# Check for the correct number of arguments
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <command> <env> <file_type>"
    echo "Example: $0 plan US/Prod clients"
    exit 1
fi

# Read the command, environment, and file type from arguments
command=$1    # e.g., "plan", "apply", or "destroy"
env=$2        # e.g., "US/Prod"
file_type=$3  # e.g., "clients" or "ATM"

# Call the function to run Terraform
run_terraform "$command" "$env" "$file_type"