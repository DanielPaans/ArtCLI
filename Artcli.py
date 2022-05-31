import requests
import argparse
import json
import os
import time


class Artwork:
    def __init__(self, _id: str, _title: str, _place_of_origin: str, _artist: str, _image_id: str, _iiif_url: str) -> None:
        self.id = _id
        self.title = _title
        self.place_of_origin = _place_of_origin
        self.artist = _artist
        self.image_id = _image_id
        self.iiif_url = _iiif_url

    def to_string(self):
        return (f"Artwork: {self.title}\n"
                f"From: {self.place_of_origin}\n"
                f"Artist: {self.artist}\n")


API_PATH = "https://api.artic.edu/api/v1/artworks"


def main():
    args = arguments()
    results = parse_artworks(request(create_url(args)))

    if args["save"]:
        print(f"results are saved at {save_results(results)}")
        return

    if args["picture"]:
        print(f"{len([download_image(artwork) for artwork in results])} artworks downloaded")
        return

    [print(artwork.to_string()) for artwork in results]


def create_url(args: dict):
    URL = API_PATH

    if args["query"] is not None:
        URL += f"/search?q={args['query']}"

    if args["fields"] is not None:
        URL += f""

    URL += f"&limit={args['limit']}"

    return URL


def save_results(artworks: list[Artwork]):

    filename = "artwork_data.txt"
    with open(filename, "w+") as f:
        [f.write(artwork.to_string() + "\n") for artwork in artworks]

    return filename


def download_image(artwork: Artwork):
    request_url = f"{artwork.iiif_url}/{artwork.image_id}/full/843,/0/default.jpg"

    with open(f'{artwork.title}.jpg', 'wb') as f:
        f.write(requests.get(request_url).content)


def request(url: str):
    request = requests.get(url)
    return request.json()


def parse_artworks(response_object):

    ids = retrieve_artwork_ids(response_object)

    artworks: list[Artwork] = []
    for id in ids:
        artworks.append(parse_artwork(request(f"{API_PATH}/{id}")))

    return artworks


def retrieve_artwork_ids(response_object):
    artworks_data = response_object["data"]

    ids: list[str] = []
    for artwork in artworks_data:
        ids.append(artwork["id"])

    return ids


def parse_artwork(response_object):
    artwork_data: dict = response_object["data"]
    artwork_config: dict = response_object["config"]

    return Artwork(
        artwork_data["id"],
        artwork_data["title"],
        artwork_data["place_of_origin"],
        artwork_data["artist_display"].replace("\n", ", "),
        # I use the artist display, because I like the little more information you get then only the artist name.
        artwork_data["image_id"],
        artwork_config["iiif_url"]
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
                    action="store_true",
                    help="FILE_NAME saves the result to a file")
    ap.add_argument("--picture",
                    "-p",
                    action="store_true",
                    help="downloads the images to files with the title name in the current directory")

    return vars(ap.parse_args())


if __name__ == '__main__':
    main()
