# ArtCLI
ArtCLI is a simple CLI application that connects with the Art Institute of Chicago API (see: http://api.artic.edu/docs/).

## Installation

Clone this project.

Open a terminal (Make sure you have the right permissions).

Go to the directory where these python scripts are installed.

Build and install with setup.py
```bash
py setup.py build install
```

## Usage

```bash
options:
  --help, -h            outputs this help
  --limit , -l          NUMBER outputs determined number of results (default =
                        10)
  --query , -q          STRING does a full-text and outputs the list only
                        determined fields
  --fields  [ ...], -f  [ ...]
                        STRING1 [STRING1, STRING2, STRING3] outputs only
                        determined fields
  --save, -s            FILE_NAME saves the result to a file
  --picture, -p         downloads the images to files with the title name in
                        the current directory
 ```
