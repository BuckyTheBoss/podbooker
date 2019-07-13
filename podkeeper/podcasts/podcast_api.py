import requests
from django.conf import settings
from . models import Episode
from accounts.models import Category
import datetime

def search_by_owner(name):
  name = name.replace(' ', '%20')
  response = requests.get(f"https://listen-api.listennotes.com/api/v2/search?q={name}&only_in=author&type=podcast",
  headers={
    "X-ListenAPI-Key": settings.LISTENNOTES_API_KEY,
    },
  )
  return response.json()['results']


def search_by_text(text):
  text = text.replace(' ', '%20')
  response = requests.get(f"https://listen-api.listennotes.com/api/v2/search?q={text}&only_in=title2%Cdescription&type=podcast",
  headers={
    "X-ListenAPI-Key": settings.LISTENNOTES_API_KEY,
    },
  )
  return response.json()['results']


def populate_podcast_object(listennotes_id, hostprofile):
  response = requests.get(f"https://listen-api.listennotes.com/api/v2/podcasts/{listennotes_id}?sort=recent_first",
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
  podcast.first_episode_date = datetime.datetime.fromtimestamp(content.get('earliest_pub_date_ms')/1000).strftime('%Y-%m-%d %H:%M:%S.%f')
  podcast.title = content.get('title')
  for genre_id in content.get('genre_ids'):
    podcast.category.add(Category.objects.filter(listen_note_id=genre_id).first())

  episodes = []
  for item in content.get('episodes'):
    episode = Episode(title=item.get('title'), podcast=podcast, description=item.get('description'), length=item.get('audio_length_sec'))
    episodes.append(episode)
  Episode.objects.bulk_create(episodes)

  podcast.save()
  hostprofile.save()



def populate_categories():
  response = requests.get("https://listen-api.listennotes.com/api/v2/genres",
    headers={
    "X-ListenAPI-Key": settings.LISTENNOTES_API_KEY,
    },
  )
  categories = []
  for item in response.json()['genres']:
    category = Category.objects.create(value=item.get('name'), listen_note_id=item.get('id'), parent_listen_notes_id=item.get('parent_id'))
    categories.append(category)

  Category.objects.bulk_create(categories)

