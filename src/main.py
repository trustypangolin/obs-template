import json
import yaml
import os
from typing import Dict, Any
import requests
from decimal import Decimal, getcontext
getcontext().prec = 15  # Set precision

def lambda_handler(event=None, context=None):
    """AWS Lambda entry point"""
    # Get inputs from Lambda environment or event
    repo_owner = os.getenv('GITHUB_REPO_OWNER', 'your-default-owner')
    repo_name = os.getenv('GITHUB_REPO_NAME', 'your-default-repo')
    config_path = os.getenv('CONFIG_PATH', 'obs/config.yaml')
    template_path = os.getenv('TEMPLATE_PATH', 'obs/scenes.json')
    
    try:
        github_token = os.getenv('GITHUB_TOKEN')
        
        # Fetch and process files
        merged = process_template(
            repo_owner=repo_owner,
            repo_name=repo_name,
            config_path=config_path,
            template_path=template_path,
            github_token=github_token
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps(merged, indent=2)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }

def process_template(repo_owner: str, repo_name: str, 
                   config_path: str, template_path: str,
                   github_token: str = None) -> Dict[str, Any]:
    """Core processing logic usable both locally and in Lambda"""
    # Get file contents
    config_content = get_github_file(
        repo_owner, repo_name, config_path, github_token
    ) if github_token else get_local_file(config_path)
    
    template_content = get_github_file(
        repo_owner, repo_name, template_path, github_token
    ) if github_token else get_local_file(template_path)
    
    # Parse and merge
    config_data = yaml.safe_load(config_content)
    template_data = json.loads(template_content)
    
    return merge_config(template_data, config_data)

# File fetching functions
def get_github_file(owner: str, repo: str, path: str, token: str) -> str:
    """Fetch file from GitHub (for Lambda/production)"""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3.raw"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def get_local_file(relative_path: str) -> str:
    """Fetch file locally (for testing)"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(base_dir, relative_path)
    with open(full_path, 'r') as f:
        return f.read()

# Merging logic (unchanged from previous)
def merge_config(template: dict, config: dict, precision: int = 15) -> dict:
    """
    Safely merges YAML config into JSON template with precision control.

    Args:
        template: Original JSON data (dict)
        config: YAML configuration (dict)
        precision: Decimal places for rounding (default: 4)

    Returns:
        New dictionary with merged values (original remains unchanged)
    """
    if not isinstance(template, dict) or not isinstance(config, dict):
        raise TypeError("Both inputs must be dictionaries")

    result = template.copy()  # Preserve original
    common_keys = set(template.keys()) & set(config.keys())

    for key in common_keys:
        if isinstance(config[key], float):
            result[key] = round(config[key], precision)
        elif isinstance(config[key], (int, str, bool)):  # Explicit basic types
            result[key] = config[key]
        # Else: ignores complex types (arrays/dicts)

    return result