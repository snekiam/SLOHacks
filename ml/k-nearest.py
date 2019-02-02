# Libraries

import json

import pandas as pd
from pandas.io.json import json_normalize

import numpy as np

from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score

# Import JSON files

with open("top_tracks_attributes.json") as f:
    top_tracks_json = json.load(f)
    
with open("rap_tracks.json") as f:
    genre_tracks_json = json.load(f)
    
top_tracks = json_normalize(top_tracks_json)
top_tracks['rank'] = range(1, len(top_tracks) + 1)

genre_tracks = json_normalize(genre_tracks_json)

train = top_tracks.sample(frac=.8)
test = top_tracks.drop(train.index)

X_train = train[['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'valence']]
y_train = train['rank']
X_test = test[['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'valence']]
y_test = test['rank']

# Finding Optimal K

def get_Kneighbors_test_error(k):
    scaler = StandardScaler()
    model = KNeighborsRegressor(n_neighbors=k)
    pipeline = Pipeline([('transform', scaler), ('fit', model)])
    return np.sqrt(np.abs(cross_val_score(pipeline, X_train, y_train, cv=10, scoring="neg_mean_squared_error").mean()))

ks = pd.Series(range(1, 30, 1))
ks.index = ks

k_cross_val = ks.apply(get_Kneighbors_test_error)

k = k_cross_val.idxmin()

# KKN Analysis

scaler = StandardScaler()
model = KNeighborsRegressor(n_neighbors= k)
pipeline = Pipeline([('transform', scaler), ('fit', model)])
np.sqrt(np.abs(cross_val_score(pipeline, X_train, y_train, cv=10, scoring="neg_mean_squared_error").mean()))

model.fit(X_train, y_train)

y_test_pred = model.predict(X_test)
y_test_pred

genre_test = genre_tracks[['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'valence']]

ranked_indices = genre_test.join(pd.Series(model.predict(genre_test)).rename("predicted_rank")).sort_values("predicted_rank").index.tolist()

return genre_tracks.loc[ranked_indices, 'id'].tolist()
