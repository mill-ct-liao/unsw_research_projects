import yaml

def read_config(yml_file):

    with open(yml_file, "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return config

def run_time(end_time, start_time):
    print('Run Time:')
    print('{:.20f} secs'.format(end_time-start_time))
    print('{:.20f} mins'.format((end_time-start_time)/60))
    print('{:.20f} hours'.format((end_time-start_time)/3600))