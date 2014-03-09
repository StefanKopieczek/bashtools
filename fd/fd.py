import os
import os.path
import sys


def finddirs(dirname, startdir, prefix=True):
    is_match = dirname.__eq__
    if prefix:
        def is_match(directory):
            return directory.startswith(dirname)

    dirs_on_current_level = [startdir]

    while True:
        dirs_on_next_level = []
        matches = set([])
        for directory in dirs_on_current_level:
            try:
                contents = [os.path.join(directory, f)
                            for f in os.listdir(directory)]
            except OSError:
                pass
            folders = [item for item in contents if os.path.isdir(item)]
            for folder in folders:
                if is_match(os.path.basename(folder)):
                    matches.add(folder)
                dirs_on_next_level.append(folder)

        if len(matches) != 0:
            return matches
        elif len(dirs_on_next_level) == 0:
            break
        else:
            dirs_on_current_level = dirs_on_next_level

    return []


def exit(exit_code):
    """Workaround for http://bugs.python.org/issue11380."""
    try:
        sys.stdout.close()
    except:
        pass
    try:
        sys.stderr.close()
    except:
        pass
    sys.exit(exit_code)


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        sys.stderr.write("Usage: python fd.py <directory> [start-height]\n")
        exit(1)

    startdir = os.getcwd()
    height = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    while height > 0:
        startdir = os.path.dirname(startdir)
        height -= 1

    matches = finddirs(sys.argv[1], startdir, prefix=True)

    if len(matches) == 0:
        # No match was found, so the command should CD to the current
        # directory - i.e. do nothing.
        sys.stderr.write("No match found.\n")
        sys.stdout.write('.')
        exit(2)
    elif len(matches) > 1:
        # Multiple matches found.
        # CD to the current directory and show an error.
        sys.stderr.write("Ambiguous command: " + ', '.join(matches) + "\n")
        sys.stdout.write('.')
        exit(3)
    else:
        sys.stdout.write(list(matches)[0])
        exit(0)
