import os
import os.path
import sys


def finddirs(dirname, startdir, prefix=True):
    """Determines the depth in the folder tree based at startdir at which some
       folders first match the dirname parameter, and the returns all such
       folders in that level.

       So in a structure <a, a/b, a/c, a/c/b>, finddirs('b', 'a') would return
       [`a/b'] only.

       If prefix is True, match any folders which start with dirname.
       Otherwise, match any folders whose name is precisely dirname.
    """
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
                continue  # Don't complain about permissions etc.

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

    # No matches found.
    return []


def exit(exit_code):
    """Workaround for http://bugs.python.org/issue11380.
       Exits and returns an error code, but isn't confused by pipes."""
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

    # The starting directory is the nth parent of the current working
    # directory, where n is the height.
    startdir = os.getcwd()
    height = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    while height > 0:
        startdir = os.path.dirname(startdir)
        height -= 1

    matches = finddirs(sys.argv[1], startdir, prefix=True)

    if len(matches) == 0:
        # No match was found.
        # Output the current directory for cd, and show an error.
        sys.stderr.write("No match found.\n")
        sys.stdout.write('.')
        exit(2)
    elif len(matches) > 1:
        # Multiple matches found.
        # Output the current directory for cd,  and show an error.
        sys.stderr.write("Ambiguous command: " + ', '.join(matches) + "\n")
        sys.stdout.write('.')
        exit(3)
    else:
        # Unique match found. Stdout it so that cd can pick it up.
        sys.stdout.write(list(matches)[0])
        exit(0)
