import pandas as pd
import sys
import random
from random import shuffle


"""
Collaborative approach data setup

This script takes the data from the anime csv and the user ratings csv files
and reads how many ratings there are for each show.
"""
def setup_data(seed=None):
  if seed:
    print("Using seed", seed)
    random.seed(seed)

  print("Reading the datasets...")

  # Read the datasets
  anime = pd.read_csv('./data/series.csv')
  ratings = pd.read_csv('./data/rating.csv')

  # We will pick 50 anime shows and 200 ratings for these shows
  # Get 50 random anime shows
  anime_ids = list(anime['anime_id'])
  shuffle(anime_ids)
  anime_ids = anime_ids[:1000]
  anime = anime[anime['anime_id'].isin(anime_ids)].sort_values(by='anime_id')

  # Remove negative ratings (ratings that have not be made)
  ratings = ratings[ratings['rating'] > -1]
  ratings = ratings[ratings['anime_id'].isin(anime_ids)]

  ratings_count = []
  added_id = []
  for anime_id in anime_ids:
    if anime_id in added_id:
      continue
    rating_count = len(ratings[ratings['anime_id'] == anime_id])
    if rating_count < 30:
      continue
    ratings_count.append((anime_id, rating_count))
    added_id.append(anime_id)

  ratings_count.sort(key=lambda tup: tup[0])

  new_anime_ids = [anime_id[0] for anime_id in ratings_count]
  ratings_count = [anime_id[1] for anime_id in ratings_count]
  processed_anime = anime[anime['anime_id'].isin(new_anime_ids)]
  processed_anime.insert(6, 'score_count', ratings_count)

  # Remove useless columns
  columns_to_keep = ['anime_id', 'title', 'score', 'score_count', 'rank', 'popularity', 'background', 'related', 'genre']
  processed_anime = processed_anime[columns_to_keep]

  path = './data/processed_series.csv'
  print("Writing the new dataset to %s..." % path)
  print(processed_anime)
  processed_anime.to_csv(path)
  print("Done.")

seed = sys.argv[1] if len(sys.argv) > 1 else None
setup_data(seed=seed)
