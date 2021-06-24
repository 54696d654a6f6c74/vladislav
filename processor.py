from re import compile
from io import StringIO


# Group 1: flags
# Group 2: path
regex = compile(r"<!--\s?include(\s\-\w+)?\s+([^\s]*)\s?-->")


def unfold(file) -> str:
    with open(file, 'r') as html_file:
        html = html_file.read()
        matches = regex.finditer(html)

        progress = 0
        out = StringIO()

        for match in matches:
            include = match.groups()
            out.write(html[progress:match.start()])
            progress = match.start() + len(match.group())

            try:
                template = str
                if include[0] is not None and 'r' in include[0]:
                    template = unfold(include[1])
                else:
                    with open(include[1], 'r') as file:
                        template = file.read()
                out.write(template)
            except FileNotFoundError:
                print(include[1] + " is not a valid path! Ignoring...")

        out.write(html[progress:len(html)])

        return out.getvalue()
