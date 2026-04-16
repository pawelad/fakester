import yaml

with open(".github/workflows/ghcr.yml", "r") as f:
    yaml.safe_load(f)
