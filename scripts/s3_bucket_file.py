import boto3
import re
import sys

def remove_comments_from_hcl(content):
    """Remove comments from HCL content."""
    return re.sub(r'#.*', '', content)

def get_bucket_name_from_backend_file(file_path):
    # Open the HCL file and remove commented lines
    bucket_name = None

    with open(file_path, 'r') as f:
        for line in f:
            stripped_line = line.strip()
            # Look for the 'bucket' line inside a comment
            if stripped_line.startswith('#') or stripped_line.startswith('//'):
                # Use regex to find the bucket value in the commented line
                match = re.search(r'bucket\s*=\s*"([^"]+)"', stripped_line)
                if match:
                    bucket_name = match.group(1)
                    break  # Exit after finding the bucket name
    
    return bucket_name

def download_and_rename_s3_file(bucket_name, s3_file_path, local_file_path, profile_name):
    # Create a session using the specified profile
    session = boto3.Session(profile_name=profile_name)

    # Create an S3 client using the session
    s3 = session.client('s3')

    # Download the file
    try:
        s3.download_file(bucket_name, s3_file_path, local_file_path)
        print(f"File {s3_file_path} successfully downloaded as {local_file_path}")
    except Exception as e:
        print(f"Error downloading file: {e}")

def upload_file_to_s3(bucket_name, local_file_path, s3_file_path, profile_name):
    # Create a session using the specified profile
    session = boto3.Session(profile_name=profile_name)

    # Create an S3 client using the session
    s3 = session.client('s3')

    # Upload the file
    try:
        s3.upload_file(local_file_path, bucket_name, s3_file_path)
        print(f"File {local_file_path} successfully uploaded as {s3_file_path}")
    except Exception as e:
        print(f"Error uploading file: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python get_s3_bucket_file.py <operation> <region> <env>")
        sys.exit(1)

    operation = sys.argv[1].lower()
    region = sys.argv[2]
    env = sys.argv[3]
    workspace = f"{region}_{env}"

    backend_file_path = "backend-template.tf"
    bucket_name = get_bucket_name_from_backend_file(backend_file_path)
    s3_file_path = f'ping/appreg/{workspace}/terraform.tfstate'  # Path to the file in S3
    local_file_path = f'{workspace}.tfstate'  # Local file with new name
    profile_name = 'Emily-profile-admin'  # Replace with your AWS SSO profile name

    if operation == "download":
        download_and_rename_s3_file(bucket_name, s3_file_path, local_file_path, profile_name)
    elif operation == "upload":
        upload_file_to_s3(bucket_name, local_file_path, s3_file_path, profile_name)
    else:
        print("Invalid operation. Use 'download' or 'upload'.")
        sys.exit(1)