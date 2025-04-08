from main import process_template
import json
import os

def test_local_processing():
    # Point to local files
    config_path = os.path.join('..', 'obs', 'config.yaml')
    template_path = os.path.join('..', 'obs', 'scenes.json')
    
    # Process without GitHub
    result = process_template(
        repo_owner='', 
        repo_name='',
        config_path=config_path,
        template_path=template_path,
        github_token=None  # Forces local file loading
    )
    
    # Save output for inspection
    output_path = os.path.join('..', 'obs', 'output.json')
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"Processing complete. Output saved to {output_path}")

if __name__ == '__main__':
    test_local_processing()