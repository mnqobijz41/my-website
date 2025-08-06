const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

const pacman = {
    x: 50,
    y: 50,
    radius: 20,
    mouthOpen: 0.7,
    speed: 2,
    direction: 'right'
};

let score = 0;
let objects = [];
let triangles = [];
let gameStarted = false;
let gamePaused = false;
let intervalId;

// Load background image
const backgroundImage = new Image();
backgroundImage.src = 'jz.jpg'; // Replace 'background_image.jpg' with your image URL

backgroundImage.onload = function() {
    // Draw the background image once it's loaded
    ctx.drawImage(backgroundImage, 0, 0, canvas.width, canvas.height);

    // Other game code here...
};


function drawPacman() {
    ctx.beginPath();
    ctx.arc(pacman.x, pacman.y, pacman.radius, pacman.mouthOpen * Math.PI, (2 - pacman.mouthOpen) * Math.PI);
    ctx.lineTo(pacman.x, pacman.y);
    ctx.fillStyle = 'yellow';
    ctx.fill();
    ctx.closePath();
}

function drawObjects() {
    ctx.fillStyle = 'blue';
    objects.forEach(obj => {
        ctx.beginPath();
        ctx.arc(obj.x, obj.y, obj.radius, 0, 2 * Math.PI);
        ctx.closePath();
        ctx.fill();
    });
}

function drawTriangles() {
    ctx.fillStyle = 'red';
    triangles.forEach(triangle => {
        ctx.save(); // Save the current state of the canvas
        // Translate to the center of the triangle
        ctx.translate(triangle.x, triangle.y);
        // Rotate the canvas by an angle (in radians)
        ctx.rotate(triangle.rotation); // triangle.rotation should be in radians
        // Draw the triangle
        ctx.beginPath();
        ctx.moveTo(-5, -10); // Adjusted coordinates to center the triangle
        ctx.lineTo(5, -10);
        ctx.lineTo(0, 10);
        ctx.closePath();
        ctx.fill();
        ctx.restore(); // Restore the previous state of the canvas
    });
}

let highScores = JSON.parse(localStorage.getItem('pacmanHighScores')) || [0, 0, 0];

function updateHighScores(newScore) {
    highScores.push(newScore);
    highScores.sort((a, b) => b - a); // Descending order
    highScores = highScores.slice(0, 3); // Keep top 3
    localStorage.setItem('pacmanHighScores', JSON.stringify(highScores));
}

function displayHighScores() {
    ctx.fillStyle = 'white';
    ctx.font = 'bold 18px Arial';
    ctx.textAlign = 'right';
    ctx.fillText('Top Scores:', canvas.width - 10, 30);
    highScores.forEach((score, i) => {
        ctx.fillText(`${i + 1}. ${score}`, canvas.width - 10, 55 + i * 25);
    });
    ctx.textAlign = 'left'; // Reset alignment
}

function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function update() {
    clearCanvas();

    // REMOVE this block to allow unlimited play
    // if (score >= 200) {
    //     clearInterval(intervalId);
    //     alert("Game Over! Your score is " + score);
    //     return;
    // }

    if (pacman.direction === 'right') {
        pacman.x += pacman.speed;
    } else if (pacman.direction === 'left') {
        pacman.x -= pacman.speed;
    } else if (pacman.direction === 'down') {
        pacman.y += pacman.speed;
    } else if (pacman.direction === 'up') {
        pacman.y -= pacman.speed;
    }

  if (pacman.x + pacman.radius >= canvas.width || pacman.x - pacman.radius <= 0) {
        pacman.direction = pacman.direction === 'right' ? 'left' : 'right';
    }

    if (pacman.y + pacman.radius >= canvas.height || pacman.y - pacman.radius <= 0) {
        pacman.direction = pacman.direction === 'down' ? 'up' : 'down';
    }

    pacman.mouthOpen = (pacman.mouthOpen + 0.1) % 2;

    moveTriangles();
    drawPacman();
    drawObjects();
    drawTriangles();
    checkCollisions();
    checkTriangleCollisions();
    displayScore();
    displayHighScores(); // <-- Add this line
}

function generateObjects(count = 1) {
    let attempts = 0;
    let maxAttempts = 1000;
    let radius = 10;
    for (let i = 0; i < count; ) {
        if (attempts > maxAttempts) break; // Prevent infinite loop
        let obj = {
            x: Math.random() * (canvas.width - 2 * radius) + radius,
            y: Math.random() * (canvas.height - 2 * radius) + radius,
            radius: radius
        };
        // Check for overlap with existing coins
        let overlapping = objects.some(existing => {
            let dx = obj.x - existing.x;
            let dy = obj.y - existing.y;
            let distance = Math.sqrt(dx * dx + dy * dy);
            return distance < 2 * radius;
        });
        if (!overlapping) {
            objects.push(obj);
            i++;
        }
        attempts++;
    }
}

function generateTriangles() {
    for (let i = 0; i < 5; i++) {
        let triangle = {
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            radius: 10, // Size of triangles
            velocityX: Math.random() * 2 - 1,
            velocityY: Math.random() * 2 - 1,
            rotation: 0,
            rotationSpeed: 2 // degrees per frame
        };
        triangles.push(triangle);
    }
}

function moveTriangles() {
    triangles.forEach(triangle => {
        triangle.x += triangle.velocityX;
        triangle.y += triangle.velocityY;

        if (triangle.x <= 0 || triangle.x >= canvas.width) {
            triangle.velocityX *= -1;
        }
        if (triangle.y <= 0 || triangle.y >= canvas.height) {
            triangle.velocityY *= -1;
        }

        // Increment rotation (convert degrees to radians)
        triangle.rotation += triangle.rotationSpeed * Math.PI / 180; // rotationSpeed in degrees per frame
    });
}

function increaseTriangleSpeed() {
    triangles.forEach(triangle => {
        // Increase speed by 10%
        triangle.velocityX *= 1.1;
        triangle.velocityY *= 1.1;
        triangle.rotationSpeed *= 1.1;
    });
}

function checkCollisions() {
    objects.forEach((obj, index) => {
        let dx = pacman.x - obj.x;
        let dy = pacman.y - obj.y;
        let distance = Math.sqrt(dx * dx + dy * dy);
        if (distance < pacman.radius + obj.radius) {
            objects.splice(index, 1);
            score += 10; // Increase score
            generateObjects(2); // Add 2 new coins
            increaseTriangleSpeed(); // Increase triangle speed
        }
    });
}

function checkTriangleCollisions() {
    triangles.forEach((triangle, index) => {
        let dx = pacman.x - triangle.x;
        let dy = pacman.y - triangle.y;
        let distance = Math.sqrt(dx * dx + dy * dy);
        if (distance < pacman.radius + triangle.radius) {
            clearInterval(intervalId);
            updateHighScores(score); // <-- Add this line
            alert("Game Over! Your score is " + score);
        }
    });
}

function displayScore() {
    ctx.fillStyle = 'white';
    ctx.font = 'bold 20px Arial';
    ctx.fillText('Score: ' + score, 10, 30);
}

function keyDownHandler(event) {
    if (!gameStarted || gamePaused) return;

    if (event.key === 'ArrowRight' || event.key === 'd') {
        pacman.direction = 'right';
    } else if (event.key === 'ArrowLeft' || event.key === 'a') {
        pacman.direction = 'left';
    } else if (event.key === 'ArrowDown' || event.key === 's') {
        pacman.direction = 'down';
    } else if (event.key === 'ArrowUp' || event.key === 'w') {
        pacman.direction = 'up';
    }
}

document.addEventListener('keydown', keyDownHandler);

function startGame() {
    gameStarted = true;
    startButton.disabled = true;
    pauseButton.disabled = false;
    restartButton.disabled = false;
    intervalId = setInterval(update, 1000 / 60);
    generateObjects();
    generateTriangles();
}

function pauseGame() {
    gamePaused = !gamePaused;
    if (gamePaused) {
        clearInterval(intervalId);
        pauseButton.innerText = 'Resume';
    } else {
        intervalId = setInterval(update, 1000 / 60);
        pauseButton.innerText = 'Pause';
    }
}

function restartGame() {
    score = 0;
    objects = [];
    triangles = [];
    clearInterval(intervalId);
    pacman.x = 50;
    pacman.y = 50;
    pacman.direction = 'right';
    pacman.mouthOpen = 0.7;
    gamePaused = false;
    gameStarted = true;
    pauseButton.innerText = 'Pause';
    startButton.disabled = true;
    pauseButton.disabled = false;
    restartButton.disabled = false;
    generateObjects(10);
    generateTriangles();
    intervalId = setInterval(update, 1000 / 60);
}

document.getElementById('startButton').addEventListener('click', startGame);
document.getElementById('pauseButton').addEventListener('click', pauseGame);
document.getElementById('restartButton').addEventListener('click', restartGame);

generateObjects();
generateTriangles();
