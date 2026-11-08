# FocusForge
A desktop focus timer. Not a website. Not a disposable browser tab. It's a real app that sits on your machine and counts down while you larp productivity. 

This is my Hackclub project. In fact, I did build a similar version to this before but I abandoned it halfway. But now, I'm back again. The goal is simple for me: make the timer work, then make it good. 

It's early. Nothing is polished. But it runs, and that's okay. 

## What it actually does
- The timer - you start it, it counts down from 25 minutes, you focus. When it's done, you get a 5 minute break. Logic lives in `main.py`. That's the feature list, and no I'm not adding "cAn YoU pLeAsE aDd ChAtGpT".

If you clicked here expecting it to be a web app, https://google.com/search?q=timer

## Known issues
In the interest of honesting, here's what's currently in the code:
- **Water counter is decorative.** It says "Water: 0 / 1" and does not update. I do plan on making this feature work soon. 
- **It saves to disk every second** while you're focused larping. Somewhere, an SSD weeps, sorry!
- **Variable naming.** I do apologise for my variable naming, but just keep in mind that a means self and b means window. I might use the whole alphabet soon.
## Usage
```
python main.py
```
That's it. No subcommands and no flags. Closing it is simple, as most desktop applications (I'm sure you can figure out how to close)

## Installation
You need Python 3.10+ with Tkinter (it ships with most Python installs; if yours doesn't have it, that's between you and your package manager). Feel free to test whether it works on an older version; let me know if you got it to work. 
```
git clone https://github.com/Central3465/FocusForge.git
cd FocusForge
python main.py
```

# Privacy
You stats are stored in a JSON file (`data.json`) on your machine. This app makes zero network requests. It does not know your IP address nor your full name, and frankly it couldn't care less. 

# Contributing
Okay. Submit a PR with your code changes and ensure it is tested (and it works). 

# License
MIT. 