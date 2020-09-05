import pymongo

from pymongo import MongoClient
import time

client = MongoClient("mongodb://localhost:27017")

db = client["sser"]

idents = db["idents"]


threshold = '0.90'

start = time.time()
dkey = {'mwsPREDTOP':'human'}
query = idents.find(dkey)
print(dkey, query.count())
print('query time = ', time.time()-start, " secs")

# find just species model predictions of thomson's gazelle
start = time.time()
dkey = {'mwsPREDTOP':'gazellethomsons'}
query = idents.find(dkey)
print(dkey, query.count())
print('query time = ', time.time()-start, " secs")

# find just species model predictions of thomson's gazelle
# and mwe predicts species, with a confidence greater that the threshold defined
start = time.time()
dkey = {'mwsPREDTOP':'gazellethomsons', 'mwePREDTOP':'species', 'mweCONFTOP' : {'$gt': threshold}}
query = idents.find(dkey)
print(dkey, query.count())
print('query time = ', time.time()-start, " secs")

# species model predicts humans, mwe predicts species, with a confidence greater that the threshold defined
start = time.time()
dkey = {'mwsPREDTOP':'human', 'mwePREDTOP':'species', 'mweCONFTOP' : {'$gt': threshold}}
query = idents.find(dkey)
print(dkey, query.count())
print('query time = ', time.time()-start, " secs")

# What percentage of pictures need to be examined?
start = time.time()
total_pictures = idents.find().count()
print("total pictures=", total_pictures)
print('query time = ', time.time()-start, " secs")

empty_threshold = '0.9'
species_threshold = '0.9'
total_empty_query = {'mwePREDTOP':'empty', 'mweCONFTOP': {'$gt':empty_threshold}}
total_species_query = {'mwePREDTOP':'species', 'mweCONFTOP': {'$gt':species_threshold}}

start = time.time()
total_empty_count = idents.find(total_empty_query).count()
print(f"total empty @ {empty_threshold} = {total_empty_count}")
print('query time = ', time.time()-start, " secs")

start = time.time()
total_species_count = idents.find(total_species_query).count()
print(f"total species @ {species_threshold} = {total_species_count}")
print('query time = ', time.time()-start, " secs")




print(f"percent needed for humans to classify at {species_threshold} confidence = ")
classification_total = 1-(total_empty_count + total_species_count)/total_pictures
print(classification_total)
