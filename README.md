# aozora analyzer
Scrape Aozora bunko page, parse aozora bunko datas, analyze aozora bunko novels.


## aozora_scraper
This script can be used to parse the html novel data in aozora_bunko repository.

At first, clone following repository.

```
git clone https://github.com/aozorabunko/aozorabunko
```

Next, move cards directory to the root of this project.

```
mv ./aozorabunko/cards ./
```

convert file encoding Shift-JIS to UTF-8.

```
find cards -name '*.html' -exec nkf -w --overwrite {} \; 
```

parse novel html files.

'''
python aozora_parser.py
'''