import os
from datetime import datetime


def create_output_dir(base_dir='output'):
    if base_dir is None:
        base_dir = 'output'
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = os.path.join(base_dir, timestamp)
    os.makedirs(output_dir, exist_ok=True)
    print(f"Created output directory: {output_dir}")
    return output_dir


def get_latest_run_dir(base_dir='output'):
    if base_dir is None:
        base_dir = 'output'
    if not os.path.exists(base_dir):
        os.makedirs(base_dir, exist_ok=True)
        return None
    dirs = [os.path.join(base_dir, d) for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    if not dirs:
        return None
    latest_run_dir = max(dirs, key=os.path.getmtime)
    print(f"Using latest run directory: {latest_run_dir}")
    return latest_run_dir
