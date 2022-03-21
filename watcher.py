from os import stat
from os.path import exists
from processor import get_included
from ast import literal_eval


def log_mods(targets: list):
    with open(".vlad_watch", "w+") as watch_file:
        for target in targets:
            mod_time = stat(target).st_mtime
            includes = get_included(target)
            includes_times = {}

            for i in range(len(includes)):
                include_mod_time = stat(includes[i]).st_mtime
                includes_times[includes[i]] = include_mod_time

            watch_file.write(f"{target}\t{str(mod_time)}\t{includes_times}\n")


# Entry data structure
# <path>    <mod_time>  <dependencies>

def parse_watch_file(watch_file) -> {dict}:
    def parse_entries(entries: [str]) -> [dict]:
        loaded_entries = []

        for i in range(entries):
            entry_data = entries[i].split('\t')
            entry = {
                "path": entry_data[0],
                "mod_time": entry_data[1]
            }
            try:
                entry["deps"] = literal_eval(entry_data[2])
            except IndexError:
                pass

            loaded_entries.append(entry)

        return loaded_entries

    def parse_deps(deps: [str]) -> {dict}:
        # decide wether to key on index or on path
        pass

    with open(watch_file, 'r') as watch_file:
        content = watch_file.read().split("---SEPARATOR---")
        entries = content.pop().splitlines()
        try:
            deps = content.pop().splitlines()
        except IndexError:
            return {parse_entries(entries)}

    return {parse_entries(entries), parse_deps(deps)}


def get_modified(targets: list) -> list:
    if not exists(".vlad_watch"):
        log_mods(targets)
        return targets

    watch_data = parse_watch_file(".vlad_watch")

    files = []
    mod_times = []
    includes = {}

    for i in range(len(watch_data.entries) - 1):  # -1 to ignore last '\n'
        parts = watch_data.entries[i].split('\t')
        files.append(parts[0])
        mod_times.append(parts[1])
        try:
            includes = literal_eval(parts[2])
        except IndexError:
            pass

    watch_data = load_log(files, mod_times)
    modified_files = []

    for target in targets:
        if (target not in watch_data.keys()
        or watch_data[target] != str(stat(target).st_mtime)):
            modified_files.append(target)

    log_mods(targets)

    return modified_files
