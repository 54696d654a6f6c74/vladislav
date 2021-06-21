from os import stat
from os.path import exists


def log_mods(targets: []):
    with open(".vlad_watch", "w+") as watch:
        for target in targets:
            mod_time = stat(target).st_mtime
            watch.write(target + "\t" + str(mod_time) + '\n')


def load_log(keys: [], values: []) -> dict:
    data = {}

    for i in range(len(keys)):
        data[keys[i]] = values[i]

    return data


def get_modified(targets: []) -> []:
    if not exists(".vlad_watch"):
        log_mods(targets)
        return targets
    else:
        with open(".vlad_watch", 'r') as watch_file:
            entries = watch_file.read().split('\n')

        files = []
        mod_times = []

        for i in range(len(entries) - 1):  # -1 to ignore last '\n'
            parts = entries[i].split('\t')
            files.append(parts[0])
            mod_times.append(parts[1])

        watch_data = load_log(files, mod_times)
        modified_files = []

        for target in targets:
            if (target not in watch_data.keys()
            or watch_data[target] != str(stat(target).st_mtime)):
                modified_files.append(target)

        log_mods(targets)

        return modified_files
