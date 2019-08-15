# Download satelite images of a geo polygon **over time**

Download (aaproximately... zoom level may vary) all satelite images (low res thumbnails) of a given geolocation.

## install

```
pip install -r requirements.txt
```

## usage

change the fetch.py file to contain your wanted date range and geo polygon, sample is given with Copenhagen, Denmark as focus.

You need a planet.com api token, which you get [here](https://developers.planet.com/docs/quickstart/getting-started/).

Store the api-token in a **.env** file in local directory.

### create folders

```
mkdir images
mkdir json_files
```

### run script

```
denv python fetch.py
```

View images coming into your `./images/` folder and metadata come into your `./json_files/` folder.
