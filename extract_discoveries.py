import xml.etree.ElementTree as ET
import requests
from lxml import html

rss_url = "https://latenightlinux.com/feed/mp3"

discoveries = []

r = requests.get(rss_url)
root = ET.fromstring(r.text)
for item in root.iter("item"):

    episode_info = {
        "name": item.find("title").text,
        "url": item.find("link").text,
    }

    r = requests.get(episode_info["url"])

    if "<strong>Discoveries</strong></p>" not in r.text:
        continue
    episode_description = r.text.split("<strong>Discoveries</strong></p>", 1)[1].split("<strong>", 1)[0]
    episode_description_root = html.fromstring(episode_description)
    for discovery in episode_description_root.xpath(".//a"):
        # Get discovery description
        r = requests.get(discovery.get("href"))
        description_root = html.fromstring(r.text)
        discovery_description = description_root.xpath("//p")
        if len(discovery_description) > 0:
            for paragraph in discovery_description:
                desc = "".join(paragraph.xpath(".//text()"))
                if desc.strip() != "":
                    break
            discovery_description = desc
        else:
            discovery_description = ""

        discoveries.append({
            "episode": episode_info,
            "name": discovery.text,
            "url": discovery.get("href"),
            "description": discovery_description.strip()
        })
        print(discoveries[-1])
