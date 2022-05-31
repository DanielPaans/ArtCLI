import requests
import argparse
import json
import os
import time


class Artwork:
    def __init__(self, _title: str, _place_of_origin: str, _artist: str) -> None:
        self.title = _title
        self.place_of_origin = _place_of_origin
        self.artist = _artist

    def print(self):
        print(f"Artwork:\n {self.title}\n {self.place_of_origin}\n Artist:\n  {self.artist}")


API_PATH = "https://api.artic.edu/api/v1/artworks"


def main():
    arguments_handler(arguments())

    # artwork: Artwork = parse(request(URL))
    # artwork.print()

def arguments_handler(args: dict):
    request(create_url(args))

    if args["save"] is not None: save_results()

    if args["picture"] is not None: download_image()

def create_url(args: dict):
    URL = API_PATH

    if args["query"] is not None:
        URL + f"/search?q={args['query']}"

    if args["fields"] is not None:
        URL + f""

    return URL + f"&limit={args['limit']}"

def save_results():
    pass

def download_image():
    pass

def request(url: str):
    request = requests.get(url)
    return request.json()


def parse(response_object):
    artwork_data = response_object["data"]

    return Artwork(
        artwork_data["title"],
        artwork_data["place_of_origin"],
        artwork_data["artist_display"].replace("\n", ", ")
        # I use the artist display, because I like the little more information you get then only the artist name.
    )


def arguments():
    ap = argparse.ArgumentParser(prog="artcli", add_help=False,
                                 usage="%(prog)s [--help] [--limit LIMIT] [--query QUERY] "
                                       "[--fields FIELDS] [--save SAVE] [--picture PICTURE]")

    ap.add_argument("--help",
                    "-h",
                    action='help',
                    default=argparse.SUPPRESS,
                    help="outputs this help")
    ap.add_argument("--limit",
                    "-l",
                    metavar="",
                    default=10,
                    help="NUMBER outputs determined number of results (default = %(default)s)")
    ap.add_argument("--query",
                    "-q",
                    metavar="",
                    help="STRING does a full-text and outputs the list only determined fields")
    ap.add_argument("--fields",
                    "-f",
                    metavar="",
                    help="NUMBER outputs determined number of results")
    ap.add_argument("--save",
                    "-s",
                    metavar="",
                    help="FILE_NAME saves the result to a file")
    ap.add_argument("--picture",
                    "-p",
                    metavar="",
                    help="downloads the images to files with the title name in the current directory")

    return vars(ap.parse_args())


if __name__ == '__main__':
    main()
