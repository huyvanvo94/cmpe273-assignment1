import yaml
with open('config.yaml', 'r') as f:
    doc = yaml.load(f)

    print(doc)