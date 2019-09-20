# reddit-usage-analysis
Analyzes reddit commenting on a per user basis (barely analysis)

## Installation
**Requirements**: argparsem, plotly, pandas

### Step-by-step
  1. Clone this repository to any folder (where you want to keep it)  
  ```$ git clone https://github.com/JuhaJGamer/reddit-usage-analysis```
  
  2. Move to that folder  
  ```$ cd reddit-usage-analysis```
  
  3. Install requirements using pip  
  ```$ python3 -m pip install -r requirements.txt```
  
  4. Run a script to test that it works  
  ```$ python3 redditscraper2.py -l 100 -a juhajgam3r +r+programmerhumor```


## Usage

All scripts have help menus that activate with ```-h```.  
Scraper scripts output their results to stdout, so use `python3 script <arguments> | tee <file>.csv`  
Additionally, because of the confusing that is the keyword system, here's a quick tutorial

  Adding a **+** before a word makes it strict. This means it can't be a part of other words but instead a word of it's own  
  EXAMPLE: `+a` matches the 'a' in 'a tree' but does not match the 'a' in 'Apple'

  Adding **r+** before a word makes it match subreddit name instead of comment body.  
  EXAMPLE: `r+a` matches the 'a' in any comment the user has posted to r/AskReddit, as well as any other subreddit name with an 'a' in it.
  
  Adding **+r+** before a word makes it a *strict* subreddit search.  
  EXAMPLE: `+r+legoyoda` matches r/legoyoda (r.i.p.) but not r/legoyodalore

## Neat tricks

The visualiser takes stdin as an input method if file is specified as ```-```. This means that you can generate graphs without the intermediate csv step, like so:  
`python3 redditscraper2.py -a -l 100 juhajgam3r +r+suomi | python3 redditchart.py -a -` | This creates a chart of my activity on r/Suomi.
