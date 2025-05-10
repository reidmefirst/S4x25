# Rule checker script to look for missing 'flow' directional keywords in rules

## Background

This analyzes a suricata rule file. If the rule defines source or destination ports above 1024, it will proceed to check if you defined a 'flow' directional keyword.

The script returns 0 if all rules passed, and 1 if any rule failed. It will display the rule SIDs for any rule which failed the check.

## Preparation

This tool relies on the `py-idstools` package, which may be installed via pip using `python3 -m pip install https://github.com/jasonish/py-idstools/archive/master.zip`.

Of course note that this is a repository not under my controller, always appropriate caution when installing third party libraries, etc etc.
## Usage

`python3 rulechecker.py -f <rules file>`

You may run this script against any of the suricata rules files included in the S4x25 talk archive.

## License

Please use for this educational purposes only. If you find it useful for work purposes, I encourage you to make a donation to OISF, the nonprofit which develops Suricata.
