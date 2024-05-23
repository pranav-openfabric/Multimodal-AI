import spacy
from spacy.training import Example
from spacy.util import minibatch, compounding
import random
import requests
import os
import json

# Load the dataset
with open("cryptocurrency_questions_dataset.json", "r") as f:
    question_dataset = json.load(f)

# Mock function to generate annotations for the training data
def create_train_data(questions, crypto_names):
    train_data = []
    for question in questions:
        entities = []
        for name in crypto_names:
            start = question.find(name)
            if start != -1:
                end = start + len(name)
                entities.append((start, end, "CRYPTO"))
        entities = filter_overlapping_entities(entities)
        train_data.append((question, {"entities": entities}))
    return train_data

def filter_overlapping_entities(entities):
    # Sort entities by start position
    entities = sorted(entities, key=lambda x: x[0])
    filtered_entities = []
    current_end = -1
    for start, end, label in entities:
        if start >= current_end:
            filtered_entities.append((start, end, label))
            current_end = end
    return filtered_entities

# Fetch top 1000 cryptocurrencies again
def get_top_cryptocurrencies(limit=1000):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    params = {
        "start": "1",
        "limit": str(limit),
        "convert": "USD"
    }
    headers = {
        "X-CMC_PRO_API_KEY": os.getenv("COINMARKETCAP_API_KEY")
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if 'data' in data:
        return [crypto['name'] for crypto in data['data']]
    else:
        raise Exception("Failed to fetch data from CoinMarketCap API")

try:
    top_cryptocurrencies = get_top_cryptocurrencies()
    print(f"Fetched {len(top_cryptocurrencies)} cryptocurrencies.")
except Exception as e:
    print(f"Error fetching cryptocurrencies: {e}")
    top_cryptocurrencies = []

# Create training data
TRAIN_DATA = create_train_data(question_dataset, top_cryptocurrencies)

# Initialize the blank spacy model
nlp = spacy.blank("en")
ner = nlp.add_pipe("ner")

# Add labels
for _, annotations in TRAIN_DATA:
    for ent in annotations.get("entities"):
        ner.add_label(ent[2])

# Train the NER model
optimizer = nlp.begin_training()
for i in range(20):
    random.shuffle(TRAIN_DATA)
    batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
    for batch in batches:
        for text, annotations in batch:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update([example], drop=0.5, sgd=optimizer)


# Save the model
nlp.to_disk(".")
