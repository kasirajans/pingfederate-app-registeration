import os
import json
from collections import defaultdict
import yaml
import sys

import tkinter as tk
from tkinter import ttk
from dotenv import load_dotenv

load_dotenv('')

def parse_arguments(args):
    # Create a dictionary to store the key-value pairs
    arg_dict = {}

    # Iterate over the passed arguments
    for arg in args:
        # Split the argument into key and value
        if '=' in arg:
            key, value = arg.split('=', 1)
            arg_dict[key] = value
        else:
            print(f"Skipping invalid argument: {arg}")

    return arg_dict


def list_files(base_path):
    files = []
    for root, dirs, filenames in os.walk(base_path):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files
# Check this value during the BUILD ENV TEST_MODE


def build_hierarchy(paths):
    tree = {}

    for path in paths:
        parts = path.split('/')
        current_level = tree

        for part in parts[:-1]:  # Navigate to the last directory
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]

        # Add the file to the directory
        filename = parts[-1]
        if filename not in current_level:
            if ".yaml" in filename:
                with open(path, 'r') as yaml_file:
                    # Load YAML content
                    yaml_content = yaml.safe_load(yaml_file)
            # Convert the YAML content (Python dictionary) to JSON string
                current_level[filename[:-len('.yaml')]] = yaml_content
                if 'ATM' in current_level and filename == 'ATM.yaml':
                    if current_level['ATM']:
                        for _ in current_level["ATM"]:
                            if 'name' in _:
                                _['name'] = (
                                    '_'.join((parts[1:])[:-1]))+"_"+_['name']
                            else:
                                _['name'] = ('_'.join((parts[1:])[:-1]))
                if 'clients' in current_level and filename == 'clients.yaml':
                    if current_level['clients']:
                        for _ in current_level["clients"]:
                            if 'name' in _:
                                _['name'] = (
                                    '_'.join((parts[1:])[:-1]))+"_"+_['name']
                            else:
                                _['name'] = ('_'.join((parts[1:])[:-1]))
                # if 'appConfig' in current_level and filename == 'appConfig.yaml':
                #     if current_level['appConfig']:
                #         for _ in current_level["appConfig"]:
                #             _['name'] = ('_'.join((parts[1:])[:-1]))
        update_oauth_apps = {}
        teamMetadata = {}
        for team in tree[base_path]:
            for team1 in tree[base_path][team]:
                if team1 not in ['ATM', 'clients', 'appConfig']:
                    # test = tree[base_path][team]
                    # tree[base_path][f'{team}_{team1}']=tree[base_path][team][team1]
                    update_oauth_apps.update(
                        {f'{team}_{team1}': tree[base_path][team][team1]})
                    # tree[base_path] +tree[base_path][f'{team}_{team1}']=tree[base_path][team][team1]
                else:
                    update_oauth_apps.update(
                        {f'{team}': tree[base_path][team]})
    return update_oauth_apps


if __name__ == "__main__":
    # Build the hierarchy
    env = os.getenv('PING_ENV')
    arguments = sys.argv[1:]
    arg_dict = parse_arguments(arguments)
    # print(sys.argv)
    if 'treeStructure.py' in sys.argv[0]:
        testapp = True
    else:
        testapp = eval((arg_dict["testmode"]).capitalize())
    if testapp:
        base_path = 'local'
    else:
        base_path = os.getenv('PING_ENV')
    files = list_files(base_path)
    hierarchy = build_hierarchy(files)
    resources = json.dumps(hierarchy)
    if not 'treeStructure.py' in sys.argv[0]:
        print(json.dumps({"resources": resources}))
