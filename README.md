# Week 01 AI Log

## Tool used 
github copilot in Vs code

## Prompt given
1)Create a simple browser game called Bug Dodger using only HTML, CSS, and JavaScript.

Rules:
- The player controls a square at the bottom of the screen.
- Bugs fall from the top.
- The player moves left and right using arrow keys.
- If a bug hits the player, the game ends.
- The score increases over time.
- Add a restart button.
- Keep the files as index.html, style.css, and game.js.
- Explain how to run it locally.

2)Review this game code. Find at least five possible bugs, missing edge cases, or design problems. Do not rewrite yet.

3)Fix the top three issues while keeping the code simple enough for a beginner to understand.

4)what are the changes of now and before while playing game

## What AI produced
It generated a index.html,styl.css, game.js file. in that it generated a code for playing a game where player has to move from arrow key, and playerr has to escape from the falling bugs otherwise games end , and there is a restart button 
## What I changed manually
For now did not change anything manualy 
## How I verified it
I opened the link given by the copilot that i opened in the browser and played a game trying to test the arrow keys,
collision detection, score, game-over, and restart button, whether bugs falling from the top. and it was working properly.
## What I still do not understand
when I asked to find the problem bugs, it found so many bugs approx 10 bugs, and when i ask to fix the top3 issue, it fixes it but i could not catch some of the change, or verify the changesIafter fixing issue 
1)Sudden jumps in gameplay when the browser slows down
3)Player can drift off the board when the window is resized

also I do not completely understand how requestAnimationFrame() works and how timestamp and delta control the movement of the game. I also want to understand the collision detection conditions using the left, right, top, and bottom coordinates