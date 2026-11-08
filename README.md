# FocusForge
A desktop focus timer. Not a website. Not a disposable browser tab. It's a real app that sits on your machine and counts down while you larp productivity. Yes, yes, I know there are approximately 47 million of these already including in Terra but this one is unique. 

This is my Hackclub project. In fact, I did build a similar version to this before but I abandoned it halfway. But now, I'm back again. The goal is simple for me: make the timer work, then make it good. 

It's early. Nothing is polished. But it runs, and that's okay. 

## What it actually does
- The timer - you start it, it counts down from 25 minutes, you focus. When it's done, you get a 5 minute break. Logic lives in `main.py`. There will be some cool gamified features later, and no I'm not adding "cAn YoU pLeAsE aDd ChAtGpT" mainly due to me being too lazy to topup on my OpenAI credits. 
- Virtual farm - grow four crops by earning water through 1 hour of focus time and watering your farm daily (your motivation for larping)
- Watering streaks - keep your larp streak going to help your crops grow through different stages otherwise they wither.

If you clicked here expecting it to be a web app, https://google.com/search?q=timer. Google has a cool and interactive timer built directly in the search results. 

## Known issues (some won't be fixed if they don't affect the core functionality)
In the interest of honesting, here's what's currently in the code: 
- **It saves to disk every second** while you're focused larping. Somewhere, an SSD weeps, sorry!
- **Variable naming.** I do apologise for my variable naming, but just keep in mind that a means self and b means window. I might use the whole alphabet soon.
- **Light mode only.** Sorry for people that are nocturnal! I might not have time to do this, so please do submit a PR!

## Goals for me
Here is a list of my dreams that I want to see accomplished in this project:
- Lofi music integration allowing you to be in the zen.
- Gamified focus timer: you get a virtual farm and you need to water your crops every day otherwise they wither. 
- A better visual look.

## Usage
```
python main.py
```
That's it. No subcommands and no flags. Closing it is simple, as most desktop applications.

## Installation
You need Python 3.10+ with Tkinter (it ships with most Python installs). Feel free to test whether it works on an older version; let me know if you got it to work. 
```
git clone https://github.com/Central3465/FocusForge.git
cd FocusForge
python main.py
```

# Privacy
Your stats are stored in a JSON file (`data.json`) on your machine. This app makes zero network requests. It does not know your IP address nor your full name, and frankly it couldn't care less. 

# Contributing
Submit a PR with your code changes and ensure it is tested (and it works). I do not mind AI assisted coding, in fact I support AI, however you must be able to verify its code and understand what it does. I'm not to strict on the PR formatting as long as it's legible.

# License
MIT. 