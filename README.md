# FocusForge
A desktop focus timer. Not a website. Not a disposable browser tab. It's a real app that sits on your machine and counts down while you larp productivity. 

This is my Hackclub project. In fact, I did build a similar version to this before but I abandoned it halfway. But now, I'm back again. The goal is simple for me: make the timer work, then make it good. 

It's early. Nothing is polished. But it runs, and that's okay. 

## What it actually does
- The timer - you start it, it counts down from 25 minutes, you focus. When it's done, you get a 5 minute break. Logic lives in `main.py`. That's the feature list, so don't give me some unreasonable suggestions such as "cAn YoU pLeAsE aDd ChAtGpT".

If you clicked here expecting it to be a web app, https://google.com/search?q=timer

## Usage
```
python main.py
```
That's it. No subcommands and no flags. Closing it is simple, as most desktop applications (I'm sure you can figure out how to close)

## Installation
You need Python 3.10+. Be my guest to test whether it works on an older version; I'll be very intrigued at your findings. 
```
git clone https://github.com/Central3465/FocusForge.git
cd FocusForge
python main.py
```

# Privacy
Your sessions are (will) be stored in a JSON file on your machine. This app does not make requests to any of my servers. 

# Contributing
Okay. Submit a PR with your code changes and ensure it is tested (and it works). 

# License
MIT. 