<h1 align="center">Fifteen puzzle game</h1>

A puzzle game known as "Pyatnashki" in my country which i loved to play in childhood. The rules are simple - you need to assemble numbers from 1 to 15 in right order.

<h2 align="center">About the project</h2>

This is my very first project. It is realized on *Python3* :snake: with `pygame` module and represents a basic version of "fifteen puzzle" with a minimal functionality.
**Just shuffle and assemble**:

<p align="center">
  <img src="https://sun9-4.userapi.com/ZjWTdlhruhGGjrTkwRPlDnHTUep2ydILj-b2tQ/2zJrdBx5mRs.jpg" width="20%"></p>

### How to start a game:

Game starts after running a python script (*main.py*). But before that you need to install `pygame` module (version 1.9.6) to virtual environment. Write in command line
in working directory:

`pip install pygame==1.9.6`

### How to play:
- to **shuffle** puzzle press ***Space***
- **move** blocks using ***Left***, ***Up***, ***Right*** and ***Down*** keys
- to **quit** a game press ***Esc***

<h2 align="center">Interesting facts</h2>

The "fifteen puzzle" game was invented in the late 19th century in America. It peaked in popularity in 1879-1880 when in newpapers was announced
a $1,000 reward 💰💰💰 (worth over $25000 today) for one who could complete a puzzle from the starting position below (with swapped 14 and 15 numbers):

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/15-puzzle-loyd.svg/220px-15-puzzle-loyd.svg.png"></p>

But noone have solved this task yet, so you have chance to be the first man on Earth who reach that :sweat_smile:.

But to be serious, mathematicians have long proved that this is impossible. More details here:
<https://kconrad.math.uconn.edu/blurbs/grouptheory/15puzzle.pdf>

<h2 align="center">Quick shuffling option</h2>

You probably noticed this :point_down: function in my script *main.py* and wondered: "What is this for and how it works"🤔:
```python
# Checking if it is possible to assemble "15 puzzle":
def isGood(a):
    n = 0
    for i in range(len(a) - 1):
        if a[i] == 0:
            continue
        for j in range(i + 1, len(a)):
            if a[j] == 0:
                continue
            if a[i] > a[j]:
                n += 1
    if n % 2 != 0:
        return True
    return False
```

There is an ability to quickly reshuffle numbers in the game. This functionality is implemented using randomness and in this case there are 50/50 odds
that it would be impossible to assemble the puzzle. So function above checks is it possible or not to collect the puzzle.
I'm not good enough at math to explain in details the mathematical proof of the 15 puzzle theorem, but you can trust me, function works well.

But you are welcome to write your own more simple and readable code:wink:.
