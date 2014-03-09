bashtools
=========

Bashtools is a collection of useful tools for BASH.

It's powerful and easy to set up - just add one line to your .bashrc and you're away!

Requirements
============
* Python V2.6 or above. This must be on your system path.


Installation
============

1.) Check out the repository.    
2.) In your .bashrc file, add a line `. <path_to_bashtools>/shortcuts`.    
3.) Enjoy your newfound efficiency!

Tools
=====

###fd - like cd, but awesome
fd is a powerful upgrade of the standard UNIX 'cd' command.    
It supports prefix matching and recursive folder search.

Usage: `fd DIRECTORY_PREFIX [start-level]`

fd searches through all subdirectories of your current directory, and if it
finds a directory starting with the term you gave it, it makes that your
current working directory.

fd will choose directories higher up the hierarchy in preference to those that
are several subfolders deep. If there are multiple matches in the highest
matching level, it will show an error and will not change your directory.

fd also takes an optional `start-level` parameter. This causes fd to start its
directory n levels higher; so for example `fd foo 1` will look for 'foo\*' in
siblings of the current directory as well as children.
