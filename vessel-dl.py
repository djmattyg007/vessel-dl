#!/usr/bin/python3

import sys
from argparse import ArgumentParser
import requests

USER_AGENT = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"

def get_args():
    parser = ArgumentParser(description="Obtain direct download links for Vessel videos.")
    parser.add_argument("--url")
    parser.add_argument("--videoid")
    parser.add_argument("--username")
    parser.add_argument("--password")
    parser.add_argument("--usertoken")

    return parser.parse_args()

def vessel_api_login(username, password):
    payload = {
        "user_key": username, "password": password,
        "type": "password", "client_id": "web"
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": USER_AGENT
    }
    r = requests.post("https://www.vessel.com/api/account/login", json=payload, headers=headers)
    return r.json()

def vessel_videodata(url):
    import json

    headers = {"User-Agent": USER_AGENT}
    r = requests.get(url, headers=headers)
    html = r.text

    start_string = 'App.bootstrapData('
    start = html.index(start_string) + len(start_string)
    end = html.index(');', start)
    return json.loads(html[start:end])

def vessel_api_video(videoid, usertoken):
    payload = {
        "client": "web"
    }
    cookies = {
        "user_token": usertoken
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": USER_AGENT
    }
    url = "https://www.vessel.com/api/view/items/{0}".format(videoid)
    r = requests.post(url, json=payload, cookies=cookies, headers=headers)
    return r.json()

def vessel_api_video_sources(videodata):
    video_item = None
    for item in videodata["assets"]:
        if item["type"] == "video" and item["is_actual_video"] == True:
            if item["sources"][0]["bitrate"] is not None and "?" in item["sources"][0]["location"]:
                video_item = item
                break
            if item["sources"][1]["bitrate"] is not None and "?" in item["sources"][1]["location"]:
                video_item = item
                break
    if not video_item:
        raise ValueError("Cannot find actual video data in API response.")
    sources = [s for s in video_item["sources"] if s["bitrate"] is not None]
    return sorted(sources, key=lambda k: k["height"])

def get_usertoken(args):
    if args.usertoken:
        return args.usertoken
    elif args.username:
        if args.password is None:
            from getpass import getpass
            password = getpass()
        else:
            password = args.password
        login_data = vessel_api_login(args.username, password)
        return login_data["user_token"]
    else:
        return None

def get_videoid(args):
    if args.videoid:
        return args.videoid
    elif args.url:
        video_data = vessel_videodata(args.url)
        return video_data["model"]["summary"]["id"]
    else:
        return None

args = get_args()

usertoken = get_usertoken(args)
if usertoken is None:
    print("Cannot authenticate with Vessel API.")
    print("Please supply a username and password, or a user token.")
    sys.exit(1)
print("User Token: {0}".format(usertoken))

videoid = get_videoid(args)
if videoid is None:
    print("Cannot discover direct video URLs without video ID.")
    print("Please supply a video page URL, or the video ID if you already know it.")
    sys.exit(2)
print("Video ID: {0}".format(videoid))

video_api_data = vessel_api_video(videoid, usertoken)
video_sources = vessel_api_video_sources(video_api_data)
for source in video_sources:
    print("{0}: {1}".format(source["name"], source["location"]))
