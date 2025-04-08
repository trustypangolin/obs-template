import os
import json
from pathlib import Path
from main import process_template


def find_git_root(start_path: str = ".") -> str:
    """Find the Git repository root directory"""
    current = Path(start_path).absolute()
    while True:
        if (current / ".git").exists():
            return str(current)
        if current.parent == current:
            raise FileNotFoundError("Not inside a Git repository")
        current = current.parent


def test_local_processing():
    try:
        # Get Git root path
        repo_root = find_git_root(os.path.dirname(__file__))

        # Set file paths relative to Git root
        config_path = os.path.join(repo_root, 'obs', 'config.yaml')
        template_path = os.path.join(repo_root, 'obs', 'scenes.json')
        output_path = os.path.join(repo_root, 'obs', 'output.json')

        # Process files
        result = process_template(
            repo_owner='',
            repo_name='',
            config_path=config_path,
            template_path=template_path,
            github_token=None  # Forces local file loading
        )

        # Save output
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)

        print(f"Processing complete. Output saved to {output_path}")
        return True

    except Exception as e:
        print(f"Error: {str(e)}")
        return False


if __name__ == '__main__':
    test_local_processing()