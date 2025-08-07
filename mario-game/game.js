const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Player properties
const player = {
    x: 100,
    y: 400,
    width: 50,
    height: 50,
    color: 'red',
    dx: 0,
    dy: 0,
    speed: 5,
    jumpStrength: 15,
    isJumping: false
};

// Platforms
const platforms = [
    { x: 0, y: 550, width: canvas.width, height: 50, color: 'green' }, // Ground
    { x: 200, y: 450, width: 150, height: 20, color: 'brown' },
    { x: 400, y: 350, width: 150, height: 20, color: 'brown' },
    { x: 600, y: 250, width: 150, height: 20, color: 'brown' }
];

// Keyboard input handling
const keys = {
    ArrowLeft: false,
    ArrowRight: false,
    Space: false
};

window.addEventListener('keydown', (e) => {
    if (e.code === 'Space') {
        keys[e.code] = true;
    } else if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
        keys[e.key] = true;
    }
});

window.addEventListener('keyup', (e) => {
    if (e.code === 'Space') {
        keys[e.code] = false;
    } else if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
        keys[e.key] = false;
    }
});


// Gravity
const gravity = 0.8;

function update() {
    // Player movement
    player.dx = 0;
    if (keys.ArrowLeft) {
        player.dx = -player.speed;
    }
    if (keys.ArrowRight) {
        player.dx = player.speed;
    }

    // Jumping
    if (keys.Space && !player.isJumping) {
        player.dy = -player.jumpStrength;
        player.isJumping = true;
    }

    // Apply gravity
    player.dy += gravity;

    // Update player position
    player.x += player.dx;
    player.y += player.dy;

    // Boundary detection for walls
     if (player.x < 0) {
        player.x = 0;
    }
    if (player.x + player.width > canvas.width) {
        player.x = canvas.width - player.width;
    }

    // Collision with platforms
    let onPlatform = false;
    for (const platform of platforms) {
        if (
            player.x < platform.x + platform.width &&
            player.x + player.width > platform.x &&
            player.y + player.height > platform.y &&
            player.y + player.height < platform.y + platform.height + player.dy
        ) {
            player.y = platform.y - player.height;
            player.dy = 0;
            player.isJumping = false;
            onPlatform = true;
            break;
        }
    }
}


// Game loop
function gameLoop() {
    update(); // Update game state

    // Clear the canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw the platforms
    for (const platform of platforms) {
        ctx.fillStyle = platform.color;
        ctx.fillRect(platform.x, platform.y, platform.width, platform.height);
    }

    // Draw the player
    ctx.fillStyle = player.color;
    ctx.fillRect(player.x, player.y, player.width, player.height);

    // Request the next frame
    requestAnimationFrame(gameLoop);
}

// Start the game loop
gameLoop();
