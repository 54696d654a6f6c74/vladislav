from os import walk, makedirs
from os.path import basename
from settings import settings
from processor import unfold


def get_files() -> []:
    targets = []

    for node in walk("./"):
        for file in node[2]:
            if (node[0] in settings.data["except_dir"]
            or node[0] == settings.data["output_dir"]
            or file in settings.data["except_filename"]):
                continue

            if file.endswith(settings.data["file_ext"]):
                path = node[0]

                if path.endswith('/'):
                    path += file
                else:
                    path += "/" + file

                if(path in settings.data["except_path"]):
                    continue

                targets.append(path)

    return targets


def run(targets: []):
    for target in targets:
        unfolded = unfold(target)
        filename = ''.join((basename(target).split('.')[:-1]))
        path = settings.data["output_dir"] + "/" + filename + "." + settings.data["output_ext"]

        with open(path, "w+") as out:
            out.write(unfolded)


makedirs(settings.data["output_dir"], exist_ok = True)
run(get_files())
