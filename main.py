import yaml
f = open('config.yaml', 'r')
doc = yaml.load(f)

users = doc['users']
port = doc['port']
max_num_messages_per_user = doc['max_num_messages_per_user']
groups = doc['groups']
group1 = groups['group1']
group2 = groups['group2']
print(doc)
