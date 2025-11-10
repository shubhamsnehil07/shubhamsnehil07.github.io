// Function to initialize the Bollywood quiz game
function initializeBollywoodQuiz() {
    // Existing initialization code...

    // Add hint button feature
    const hintBtn = document.createElement('button');
    hintBtn.id = 'hintBtn';
    hintBtn.innerText = 'Hint';
    document.getElementById('quizControls').appendChild(hintBtn);

    let hintUsed = false;
    hintBtn.addEventListener('click', function() {
        if (!hintUsed && lives > 0) {
            // Show hint
            document.getElementById('hintText').style.display = 'block';
            lives--;
            hintUsed = true;
        }
    });

    // Existing game setup and event listeners...
}

// Function called on level completion
function levelComplete() {
    // Show level complete screen with celebration
    document.getElementById('levelCompleteScreen').style.display = 'block';

    // Trigger confetti celebration
    triggerConfetti();
}

// Function to trigger confetti animation
function triggerConfetti() {
    const canvas = document.createElement('canvas');
    // Confetti animation logic...
    document.body.appendChild(canvas);
}

// Manage state for level complete choices
function manageLevelCompleteChoices() {
    const nextLevelBtn = document.createElement('button');
    nextLevelBtn.innerText = 'Next Level';
    nextLevelBtn.addEventListener('click', function() {
        proceedToNextLevel();
    });
    document.getElementById('levelCompleteScreen').appendChild(nextLevelBtn);

    const replayLevelBtn = document.createElement('button');
    replayLevelBtn.innerText = 'Replay Level';
    replayLevelBtn.addEventListener('click', function() {
        replayCurrentLevel();
    });
    document.getElementById('levelCompleteScreen').appendChild(replayLevelBtn);
}

// Add the levelCompleteScreen object to existing screens
screens.levelCompleteScreen = {
    // Level complete screen properties...
};

// Call initialization function
initializeBollywoodQuiz();