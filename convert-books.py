#!/usr/bin/env python

__doc__ = r"""
A script for converting multiple AAX files to a different format.

Essentially just wraps `AAXtoMP3` to be more convenient for me.
For each file, we create a new directory named accordingly, and put the 
converted output within that directory.
"""

__epilog= r"""
Example
-------
    # Convert single audiobook, store result in in `~audiobooks` 
    python convert-books.py --outdir=~/audiobooks --authcode=<YOUR_AUTHCODE> ~/Downloads/MyImmortal.aax
    
    # Convert many audiobooks at once, letting `AAXtoMP3` try to find authcode 
    python convert-books.py --outdir=~/audiobooks ~/Downloads/*.aax


Notes
-----
Ensure that you're passing viable files to this script, and that your authcode 
works correctly.

If you want to change the options for `AAXtoMP3` you're going to have to 
modify this script file.
This could be necessary if you want to save the books in a different format, 
or change the naming scheme for the output.

"""
__author__ = "rldotai"
__version__ = "0.1.0"
__license__ = "GPL3"


# Usage:
# ./convert-books /path/to/audiobooks/*.aax

# bash AAXtoMP3 --authcode ae3e7d0a  --chaptered --target_dir $(basename $(realpath ~/Downloads/audible-downloads/Awakenings_ep6.aax) .aax) ~/Downloads/audible-downloads/Awakenings_ep6.aax
import argparse
import logging
import os
import subprocess
import sys
from pathlib import Path

try:
    import logzero

    logger = logzero.setup_logger(__name__)
except ModuleNotFoundError:
    def get_logger(name=__name__):
        """Create and setup a logger."""
        ret = logging.getLogger(name)
        ret.propagate = False
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        formatter = logging.Formatter('[%(levelname)1.1s %(module)s:%(lineno)d] %(message)s')
        ch = logging.StreamHandler()
        ch.setLevel(level=logging.DEBUG)
        ch.setFormatter(formatter)
        ret.addHandler(ch)
        return ret
    logger = get_logger()




def main(argv=None):
    parser = argparse.ArgumentParser(prog='convert-books.py', description=__doc__, epilog=__epilog, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        "filenames", nargs="*", type=Path, help="Names of audiobook files"
    )
    parser.add_argument(
        "--outdir",
        "-o",
        type=Path,
        default="output",
        help="Directory in which outputs will be stored",
    )
    parser.add_argument(
        "--authcode",
        "-A",
        type=str,
        default='',
        help="Authorization code for audiobooks (can be found using `audible-activator`).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run, just printing the commands that would be executed.",
    )

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
    )

    # Set logging verbosity
    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument(
        "-v",
        "--verbose",
        action="store_const",
        const=logging.DEBUG,
        default=logging.INFO,
        help="Logging verbosity",
    )
    verbosity.add_argument(
        "--quiet",
        action="store_const",
        const=logging.WARNING,
        dest="verbose",
        help="Logging verbosity",
    )

    # Parse arguments
    args = vars(parser.parse_args(argv))

    # Set logging level
    logger.setLevel(args["verbose"])

    # See arguments
    logger.debug(args)


    # Assumes that `AAXtoMP3` is in a submodule of current directory
    __AAXtoMP3_PATH = Path(__file__).resolve().parent / "AAXtoMP3/AAXtoMP3"

    if not __AAXtoMP3_PATH.exists():
        raise FileNotFoundError(f"Path to `AAXtoMP3` not found ({__AAXtoMP3_PATH})")

    # Directory to store conversion results
    outdir = Path(args['outdir'])
    if not outdir.exists():
        if args['dry_run']:
            logger.info(f"(DRY RUN) Creating directory {outdir.absolute()}")
        else:
            logger.info(f"Creating directory {outdir.absolute()}")
            outdir.mkdir()


    for name in args['filenames']:
        path = Path(name).absolute()
        logger.info(f"Converting audiobook at: {path}")
        
        stem = path.stem


        # Construct command
        cmd = " ".join([
            f"bash {__AAXtoMP3_PATH}",
            f"--authcode {args['authcode']}" if args['authcode'] else '',
            f"--target_dir {outdir}",
            "-e:m4a",
            "--chaptered",
            "--dir-naming-scheme '$artist -- $title'",
            f"{path}"
        ])


        # Execute the command
        if args['dry_run']:
            logger.info(f"(DRY RUN) running {cmd}")
        else:
            logger.info(f"running {cmd}")
            subprocess.call(cmd, shell=True)

    # retval = subprocess.call(f"bash {script!s}", shell=True)


if __name__ == "__main__":
    main(sys.argv[1:])
