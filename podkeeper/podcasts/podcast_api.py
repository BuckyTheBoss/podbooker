import requests
from django.conf import settings
from . models import Episode

def search_by_owner(name):
  name = name.repalce(' ', '%20')
  response = requests.get(f"https://listen-api.listennotes.com/api/v2/search?q={name}&only_in=author",
  headers={
    "X-ListenAPI-Key": settings.LISTENNOTES_API_KEY,
    },
  )
  return response.json()


def search_by_name(text)
  text = text.repalce(' ', '%20')
  response = requests.get(f"https://listen-api.listennotes.com/api/v2/search?q={text}&only_in=title2%Cdescription",
  headers={
    "X-ListenAPI-Key": settings.LISTENNOTES_API_KEY,
    },
  )
  return response.json()


def populate_podcast_object(listennotes_id, hostprofile):
  response = requests.get("https://listen-api.listennotes.com/api/v2/podcasts/4d3fe717742d4963a85562e9f84d8c79?sort=recent_first",
  headers={
    "X-ListenAPI-Key": settings.LISTENNOTES_API_KEY,
    },
  )
  podcast = hostprofile.podcast_set.first()
  content = response.json()
  hostprofile.pub_email = content.get('email')
  podcast.cover_art_link = content.get('image')
  podcast.itunes_id = content.get('itunes_id')
  podcast.description = content.get('description')
  podcast.total_episodes = content.get('total_episodes')
  podcast.first_episode_date = content.get('earliest_pub_date_ms')


  episodes = []
  for item in content.get('episodes'):
    episode = Episode(title=item.get('title'), podcast=podcast, description=item.get('description'), length=item.get('audio_length_sec'))
    episodes.append(episode)
  Episode.objects.bulk_create(episodes)
  podcast.save()
  hostprofile.save()




  



