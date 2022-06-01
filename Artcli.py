import requests
import argparse
import json
import os
import time
import datetime

# Predefined
API_PATH = "https://api.artic.edu/api/v1/artworks"

class Artwork:
    def __init__(self, _id: str, _title: str = None, _place_of_origin: str = None,
                 _artist: str = None, _image_id: str = None, _iiif_url: str = None) -> None:

        self.id = _id
        self.title = _title
        self.place_of_origin = _place_of_origin
        self.artist = _artist
        self.image_id = _image_id
        self.iiif_url = _iiif_url

    def __str__(self):
        string = ""
        if self.title is not None: string += f"Artwork: {self.title}\n"
        if self.place_of_origin is not None: string += f"From: {self.place_of_origin}\n"
        if self.artist is not None: string += f"Artist: {self.artist}\n"

        return string


# Main functions
def main() -> None:
    args = arguments()
    options = {"title": False, "place_of_origin": False, "artist": False, "picture": False}

    if args["fields"] is not None:
        fields = "".join(args["fields"]).lower()
        if "title" in fields:
            options["title"] = True
        if "origin" in fields:
            options["place_of_origin"] = True
        if "artist" in fields:
            options["artist"] = True
    else:
        options = {option: True for option in options}

    options["picture"] = args["picture"]

    results = parse_artworks(request(create_url(args)), options)

    if args["picture"]:
        print(f"{len([download_image(artwork) for artwork in results])} artworks downloaded")
        return

    if args["save"]:
        print(f"results are saved at {save_results(results)}")
        return

    [print(artwork) for artwork in results]


def arguments() -> dict:
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
                    nargs="+",
                    help="STRING1 [STRING1, STRING2, STRING3] outputs only determined fields")
    ap.add_argument("--save",
                    "-s",
                    action="store_true",
                    help="FILE_NAME saves the result to a file")
    ap.add_argument("--picture",
                    "-p",
                    action="store_true",
                    help="downloads the images to files with the title name in the current directory")

    return vars(ap.parse_args())


# Util functions
def request(url: str) -> json:
    request = requests.get(url)
    return request.json()


def create_url(args: dict) -> str:
    url = API_PATH

    if args["query"] is not None:
        url += f"/search?q={args['query']}"

    url += f"&limit={args['limit']}"

    return url


def parse_artwork(response_object: json, options: dict) -> Artwork:
    artwork_data: dict = response_object["data"]
    artwork_config: dict = response_object["config"]

    artwork = Artwork(artwork_data["id"])

    if options["title"]:
        artwork.title = artwork_data["title"]
    if options["place_of_origin"]:
        artwork.place_of_origin = artwork_data["place_of_origin"]
    if options["artist"]:
        artwork.artist = artwork_data["artist_display"].replace("\n", ", ")
    if options["picture"]:
        artwork.image_id = artwork_data["image_id"]
        artwork.iiif_url = artwork_config["iiif_url"]

    return artwork


def parse_artworks(response_object: json, options: dict) -> list[Artwork]:
    ids = retrieve_artwork_ids(response_object)

    artworks: list[Artwork] = []
    for id in ids:
        artworks.append(parse_artwork(request(f"{API_PATH}/{id}"), options))

    return artworks


def retrieve_artwork_ids(response_object: json) -> list[int]:
    artworks_data = response_object["data"]

    ids: list[str] = []
    for artwork in artworks_data:
        ids.append(artwork["id"])

    return ids


def save_results(artworks: list[Artwork]) -> str:
    filename = f"artwork_data_{datetime.datetime.now().strftime('%d%m%y_%H%M%S')}.txt"
    with open(filename, "w+") as f:
        [f.write(str(artwork) + "\n") for artwork in artworks]

    return filename


def download_image(artwork: Artwork) -> None:
    request_url = f"{artwork.iiif_url}/{artwork.image_id}/full/843,/0/default.jpg"

    with open(f'{artwork.title}.jpg', 'wb') as f:
        f.write(requests.get(request_url).content)


if __name__ == '__main__':
    main()
