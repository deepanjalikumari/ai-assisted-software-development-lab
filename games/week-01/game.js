const gameArea = document.getElementById('gameArea');
const player = document.getElementById('player');
const scoreEl = document.getElementById('score');
const statusEl = document.getElementById('status');
const restartButton = document.getElementById('restartButton');

const playerWidth = 42;
const playerHeight = 42;
const playerSpeed = 7;
let playerX = 0;
let score = 0;
let gameOver = false;
let spawnTimer = 0;
let bugs = [];
let animationFrameId = null;

const keys = {
  ArrowLeft: false,
  ArrowRight: false,
};

function updatePlayerPosition() {
  player.style.left = `${playerX}px`;
}

function setPlayerStart() {
  const areaWidth = gameArea.clientWidth;
  playerX = (areaWidth - playerWidth) / 2;
  updatePlayerPosition();
}

function updateScore() {
  scoreEl.textContent = Math.floor(score);
}

function resetKeys() {
  keys.ArrowLeft = false;
  keys.ArrowRight = false;
}

function spawnBug() {
  const bug = document.createElement('div');
  bug.className = 'bug';

  const bugSize = 28;
  const x = Math.random() * (gameArea.clientWidth - bugSize);

  bug.style.left = `${x}px`;
  bug.style.top = `-30px`;
  gameArea.appendChild(bug);

  bugs.push({
    element: bug,
    x,
    y: -30,
    size: bugSize,
    speed: 160 + Math.random() * 120 + score * 0.25,
  });
}

function handleInput() {
  if (keys.ArrowLeft) {
    playerX -= playerSpeed;
  }

  if (keys.ArrowRight) {
    playerX += playerSpeed;
  }

  const maxX = gameArea.clientWidth - playerWidth;
  playerX = Math.max(0, Math.min(playerX, maxX));
  updatePlayerPosition();
}

function checkCollision(playerBox, bugBox) {
  return (
    playerBox.left < bugBox.right &&
    playerBox.right > bugBox.left &&
    playerBox.top < bugBox.bottom &&
    playerBox.bottom > bugBox.top
  );
}

function gameLoop(timestamp) {
  if (gameOver) {
    return;
  }

  const delta = Math.min((timestamp - (gameLoop.lastTime || timestamp)) / 1000, 0.04);
  gameLoop.lastTime = timestamp;

  score += delta * 10;
  updateScore();

  spawnTimer += delta;
  if (spawnTimer > 0.7) {
    spawnBug();
    spawnTimer = 0;
  }

  handleInput();

  bugs.forEach((bug) => {
    bug.y += bug.speed * delta;
    bug.element.style.top = `${bug.y}px`;

    const playerBox = {
      left: playerX,
      top: gameArea.clientHeight - playerHeight - 12,
      right: playerX + playerWidth,
      bottom: gameArea.clientHeight - 12,
    };

    const bugBox = {
      left: bug.x,
      top: bug.y,
      right: bug.x + bug.size,
      bottom: bug.y + bug.size,
    };

    if (checkCollision(playerBox, bugBox)) {
      endGame();
    }
  });

  bugs = bugs.filter((bug) => {
    const stillVisible = bug.y < gameArea.clientHeight + 40;
    if (!stillVisible) {
      bug.element.remove();
    }
    return stillVisible;
  });

  animationFrameId = requestAnimationFrame(gameLoop);
}

function endGame() {
  gameOver = true;
  statusEl.textContent = 'Game Over';
  statusEl.style.color = '#f87171';
  restartButton.textContent = 'Play Again';
  restartButton.disabled = false;
  cancelAnimationFrame(animationFrameId);
}

function resetGame() {
  bugs.forEach((bug) => bug.element.remove());
  bugs = [];
  score = 0;
  spawnTimer = 0;
  gameOver = false;
  resetKeys();
  statusEl.textContent = 'Playing';
  statusEl.style.color = '#60a5fa';
  restartButton.textContent = 'Restart';
  setPlayerStart();
  updateScore();
  gameLoop.lastTime = 0;
  cancelAnimationFrame(animationFrameId);
  animationFrameId = requestAnimationFrame(gameLoop);
}

window.addEventListener('resize', () => {
  const maxX = gameArea.clientWidth - playerWidth;
  playerX = Math.max(0, Math.min(playerX, maxX));
  updatePlayerPosition();
});

document.addEventListener('keydown', (event) => {
  if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
    event.preventDefault();
    keys[event.key] = true;
  }
});

document.addEventListener('keyup', (event) => {
  if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
    keys[event.key] = false;
  }
});

restartButton.addEventListener('click', resetGame);

setPlayerStart();
updateScore();
statusEl.textContent = 'Playing';
statusEl.style.color = '#60a5fa';
resetGame();
