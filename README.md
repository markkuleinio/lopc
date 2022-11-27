# lopc (Lines of Python Code)

    usage: lopc [-h] [-e EXCLUDE_DIR] [--no-defaults] [-v] TARGET [TARGET ...]

    Count lines of Python code

    positional arguments:
      TARGET                File or directory to scan (can be given multiple times)

    optional arguments:
      -h, --help            show this help message and exit
      -e EXCLUDE_DIR, --exclude-dir EXCLUDE_DIR
                            Add directory (and its subdirectories) to the
                            exclusion list. Can be given multiple times. Unix
                            shell-style wildcards (?*) are allowed. Default =
                            'venv', '.*' and '__pycache__'
      --no-defaults         Don't exclude any directories by default (use
                            --exclude-dir as needed)
      -v, --verbose         More output (can be given multiple times, default =
                            not verbose)


## Install

    (venv) $ pip install lopc


## Run

    (venv) $ lopc /home/markku/devel/lopc
    /home/markku/devel/lopc Files: 4 Lines: 144

    (venv) $ lopc /home/markku/devel/lopc -v
    File: /home/markku/devel/lopc/setup.py (15 lines)
    File: /home/markku/devel/lopc/lopc/__main__.py (5 lines)
    File: /home/markku/devel/lopc/lopc/lopc.py (124 lines)
    File: /home/markku/devel/lopc/lopc/__init__.py (0 lines)
    /home/markku/devel/lopc Files: 4 Lines: 144

    (venv) $ lopc /home/markku/devel/lopc -vv
    Directory: /home/markku/devel/lopc
    File: /home/markku/devel/lopc/setup.py (15 lines)
    Directory: /home/markku/devel/lopc/lopc
    File: /home/markku/devel/lopc/lopc/__main__.py (5 lines)
    File: /home/markku/devel/lopc/lopc/lopc.py (124 lines)
    File: /home/markku/devel/lopc/lopc/__init__.py (0 lines)
    Directory: /home/markku/devel/lopc/lopc.egg-info
    /home/markku/devel/lopc Files: 4 Lines: 144
