import yaml


def print_as_yaml(dict):
    yaml.Dumper.ignore_aliases = lambda *args: True
    print(yaml.dump(dict, sort_keys=False))


def load_from_yaml(filename):
    yaml.Dumper.ignore_aliases = lambda *args: True
    with open(filename) as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def save_as_yaml(to_save, filename):
    yaml.Dumper.ignore_aliases = lambda *args: True
    with open(filename, 'w') as file:
        documents = yaml.dump(to_save, file, sort_keys=False)

