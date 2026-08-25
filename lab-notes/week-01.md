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
## Additional Notes
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

Also, I do not completely understand how `requestAnimationFrame()` works, or how the timestamp and delta control the movement of the game. I also want to understand how collision detection compares the left, right, top, and bottom coordinates.
## Tool Used

GitHub Copilot in VS Code

## Prompt Given

1. Create a simple browser game called **Bug Dodger** using only HTML, CSS, and JavaScript.

   **Rules:**

   * The player controls a square at the bottom of the screen.
   * Bugs fall from the top.
   * The player moves left and right using the arrow keys.
   * If a bug hits the player, the game ends.
   * The score increases over time.
   * Add a restart button.
   * Keep the files as `index.html`, `style.css`, and `game.js`.
   * Explain how to run it locally.

2. Review this game code. Find at least five possible bugs, missing edge cases, or design problems. Do not rewrite the code yet.

3. Fix the top three issues while keeping the code simple enough for a beginner to understand.

4. What are the changes now compared to before while playing the game?

## What AI Produced

GitHub Copilot generated three files: `index.html`, `style.css`, and `game.js`. The code created a simple browser game in which the player moves left and right using the arrow keys and tries to avoid falling bugs. If a bug hits the player, the game ends. It also included a score system and a restart button.

After reviewing the code, Copilot identified several possible bugs and edge cases. I then asked it to fix the top three issues while keeping the code simple and beginner-friendly.

## What I Changed Manually

For now, I did not make any manual changes to the code. I used the code generated and modified by GitHub Copilot.

## How I Verified It

I opened the link provided by Copilot in the browser and played the game to test the main features. I checked whether:

* The player could move using the arrow keys.
* Bugs were falling from the top.
* Collision detection was working.
* The game ended when a bug hit the player.
* The score increased during gameplay.
* The restart button worked correctly.

The game was working properly during my testing.

## What I Still Do Not Understand

When I asked Copilot to find problems in the code, it identified around 10 possible bugs or design issues. After asking it to fix the top three issues, I could see that the code had changed, but I could not clearly understand or verify some of the changes.

Two issues that I especially want to understand better are:

1. **Sudden jumps in gameplay when the browser slows down**
   I do not completely understand how `requestAnimationFrame()` helps solve this problem or how the timestamp and delta time are used to control the movement of the game.

2. **Player can drift off the board when the window is resized**
   I want to understand how the updated code keeps the player inside the game area after the browser window is resized.

I also want to understand **collision detection** better, especially how the code compares the player's `left`, `right`, `top`, and `bottom` coordinates with the corresponding coordinates of the falling bugs to determine whether they are overlapping.

Overall, I understand how to play and test the game, but I need to understand the underlying code changes more clearly so that I can verify whether the fixes made by the AI are actually correct.
