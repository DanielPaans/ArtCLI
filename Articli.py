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


def main():
    URL = "https://api.artic.edu/api/v1/artworks/51349"
    artwork: Artwork = parse(request(URL))
    artwork.print()


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


def argument():
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", "--name", required=True, help="name of the user")
    args = vars(ap.parse_args())

    # display a friendly message to the user
    print(f"Hi there {args['name']}, it's nice to meet you!")


if __name__ == '__main__':
    argument()
    # main()
