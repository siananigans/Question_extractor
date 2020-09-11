"""
Scrape dataset from json file for location data
(cities and countries)
& Add to location model

"""
import json
import pickle

def get_locations(file_path, model_location):

    file = open(file_path, 'r')
    text = json.load(file)
    file.close()

    countries = []
    cities = []
    # Get countries & cities
    for entry in text:
        country = entry['country'].split()
        for w in country:
            if w.lower() not in countries:
                countries.append(w.lower())

        city = entry['name'].split()
        for wd in city:
            if wd.lower() not in cities:
                cities.append(wd.lower())

    all = countries + cities

    # Write to model
    model = open(model_location, 'wb')
    pickle.dump(all, model)
    model.close()

    print("Successfully wrote to model.")


def main():
    path = '../test_files/data_sets/world-cities_json.json'
    model = '../models/location_model'
    get_locations(path, model)



if __name__ == '__main__':
    main()
