// ============================================
// GAME CONFIGURATION
// ============================================

// ChatGPT API Configuration (Commented out for user to fill in)

const OPENAI_API_KEY = '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'; // Add your OpenAI API key here
const OPENAI_API_URL = 'https://api.openai.com/v1/chat/completions';

// Function to fetch dialogue from ChatGPT API
async function fetchDialogueFromAPI(level) {
    const difficulty = ['popular recent movies', 'mix of popular and recent', 'mix of popular and classic', 'classic movies', 'classic and challenging'][level - 1];
    
    const prompt = `Generate a famous Bollywood movie dialogue and provide 4 movie options (one correct and three wrong). The dialogue should be from ${difficulty}. Return in JSON format: {"dialogue": "...", "correct": "Movie Name", "options": ["Option1", "Option2", "Option3", "Option4"], "hint": "Year or genre"}`;
    
    try {
        const response = await fetch(OPENAI_API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${OPENAI_API_KEY}`
            },
            body: JSON.stringify({
                model: 'gpt-3.5-turbo',
                messages: [{ role: 'user', content: prompt }],
                temperature: 0.8
            })
        });
        
        const data = await response.json();
        return JSON.parse(data.choices[0].message.content);
    } catch (error) {
        console.error('API Error:', error);
        return null;
    }
}


// ============================================
// HARDCODED QUESTIONS (Fallback - 50 Unique Questions)
// ============================================

const QUESTIONS_BANK = {
    // Level 1: Popular Recent Movies (2015-2023)
    level1: [
        {
            dialogue: "Ek baar jo maine commitment kar di, toh main khud ki bhi nahi sunta",
            correct: "Wanted",
            options: ["Wanted", "Dabangg", "Kick", "Tiger Zinda Hai"],
            hint: "2009 Salman Khan action film"
        },
        {
            dialogue: "Don ka intezaar toh gyarah mulkon ki police kar rahi hai, lekin Don ko pakadna mushkil hi nahi, namumkin hai",
            correct: "Don",
            options: ["Don", "Don 2", "Race", "Dhoom 3"],
            hint: "SRK 2006 remake"
        },
        {
            dialogue: "Kabhi kabhi kuch jeetne ke liye kuch haarna bhi padta hai, aur haar kar jeetne wale ko hi baazigar kehte hai",
            correct: "Baazigar",
            options: ["Baazigar", "Darr", "Dilwale", "Anjaam"],
            hint: "1993 SRK thriller"
        },
        {
            dialogue: "Mere paas maa hai",
            correct: "Deewar",
            options: ["Deewar", "Trishul", "Agneepath", "Coolie"],
            hint: "1975 Amitabh classic"
        },
        {
            dialogue: "Pushpa naam sunke flower samjhe kya? Flower nahi, fire hai main",
            correct: "Pushpa",
            options: ["Pushpa", "KGF", "RRR", "Vikram"],
            hint: "2021 Allu Arjun blockbuster"
        },
        {
            dialogue: "Haath ki safai mein toh hum shehar mein mashhoor hai sahib",
            correct: "Mr. India",
            options: ["Mr. India", "Tezaab", "Nayak", "Chandni"],
            hint: "1987 Anil Kapoor sci-fi"
        },
        {
            dialogue: "All is well",
            correct: "3 Idiots",
            options: ["3 Idiots", "PK", "Munna Bhai MBBS", "Taare Zameen Par"],
            hint: "2009 Aamir Khan comedy"
        },
        {
            dialogue: "Bade bade deshon mein aisi chhoti chhoti baatein hoti rehti hai",
            correct: "Dilwale Dulhania Le Jayenge",
            options: ["Dilwale Dulhania Le Jayenge", "Kuch Kuch Hota Hai", "Kabhi Khushi Kabhie Gham", "Mohabbatein"],
            hint: "1995 SRK-Kajol romance"
        },
        {
            dialogue: "Picture abhi baaki hai mere dost",
            correct: "Om Shanti Om",
            options: ["Om Shanti Om", "Chennai Express", "Happy New Year", "Raees"],
            hint: "2007 SRK double role"
        },
        {
            dialogue: "Mogambo khush hua",
            correct: "Mr. India",
            options: ["Mr. India", "Shaan", "Kala Patthar", "Shahenshah"],
            hint: "1987 - Villain's famous dialogue"
        }
    ],
    
    // Level 2: Mix of Popular and Recent
    level2: [
        {
            dialogue: "Kitne aadmi the?",
            correct: "Sholay",
            options: ["Sholay", "Deewar", "Zanjeer", "Don"],
            hint: "1975 Gabbar Singh dialogue"
        },
        {
            dialogue: "Rishte mein toh hum tumhare baap lagte hai, naam hai Shahenshah",
            correct: "Shahenshah",
            options: ["Shahenshah", "Agneepath", "Khuda Gawah", "Muqaddar Ka Sikandar"],
            hint: "1988 Amitabh Bachchan"
        },
        {
            dialogue: "Main apni favourite hoon",
            correct: "Jab We Met",
            options: ["Jab We Met", "Cocktail", "Piku", "Highway"],
            hint: "2007 Kareena Kapoor"
        },
        {
            dialogue: "Tumse na ho payega",
            correct: "Gangs of Wasseypur",
            options: ["Gangs of Wasseypur", "Mirzapur", "Sacred Games", "Gulaal"],
            hint: "2012 Anurag Kashyap"
        },
        {
            dialogue: "Beta, tumse na ho payega",
            correct: "Gangs of Wasseypur",
            options: ["Gangs of Wasseypur", "Satya", "Company", "Delhi Belly"],
            hint: "2012 Crime saga"
        },
        {
            dialogue: "Tareekh pe tareekh, tareekh pe tareekh",
            correct: "Damini",
            options: ["Damini", "Ghayal", "Khalnayak", "Saudagar"],
            hint: "1993 courtroom drama"
        },
        {
            dialogue: "Main kehta hoon arrey wow",
            correct: "Partner",
            options: ["Partner", "Mujhse Shaadi Karogi", "Judwaa", "Housefull"],
            hint: "2007 Govinda comedy"
        },
        {
            dialogue: "Aaj maine kuch khaas nahi kiya, par jab karunga toh history ban jayegi",
            correct: "Student of the Year",
            options: ["Student of the Year", "Kuch Kuch Hota Hai", "Kabhi Alvida Naa Kehna", "My Name is Khan"],
            hint: "2012 Karan Johar"
        },
        {
            dialogue: "Main hoon Don, jiski talash mein police, banhe khoon ko tapish mein",
            correct: "Don",
            options: ["Don", "Deewaar", "Trishul", "Shakti"],
            hint: "1978 original"
        },
        {
            dialogue: "Pyaar dosti hai",
            correct: "Kuch Kuch Hota Hai",
            options: ["Kuch Kuch Hota Hai", "Dilwale Dulhania Le Jayenge", "Dil To Pagal Hai", "Mohabbatein"],
            hint: "1998 love triangle"
        }
    ],
    
    // Level 3: Mix of Popular and Classic
    level3: [
        {
            dialogue: "Jaa Simran jaa, jee le apni zindagi",
            correct: "Dilwale Dulhania Le Jayenge",
            options: ["Dilwale Dulhania Le Jayenge", "Mohabbatein", "Veer-Zaara", "Kal Ho Naa Ho"],
            hint: "1995 Amrish Puri's dialogue"
        },
        {
            dialogue: "Prem naam hai mera, Prem Chopra",
            correct: "Bobby",
            options: ["Bobby", "Amar Akbar Anthony", "Hera Pheri", "Raja Babu"],
            hint: "1973 Rishi Kapoor debut"
        },
        {
            dialogue: "Crime master Gogo naam hai mera, aankhen nikal ke gotiyan khelta hoon",
            correct: "Andaz Apna Apna",
            options: ["Andaz Apna Apna", "Hera Pheri", "Golmaal", "Phir Hera Pheri"],
            hint: "1994 cult comedy"
        },
        {
            dialogue: "Kuttey, kaminey, main tera khoon pee jaunga",
            correct: "Karan Arjun",
            options: ["Karan Arjun", "Khoon Bhari Maang", "Baazigar", "Darr"],
            hint: "1995 Amrish Puri villain"
        },
        {
            dialogue: "Jo darr gaya samjho marr gaya",
            correct: "Sholay",
            options: ["Sholay", "Deewar", "Don", "Zanjeer"],
            hint: "1975 Veeru's dialogue"
        },
        {
            dialogue: "Sara sheher mujhe lion ke naam se jaanta hai",
            correct: "Kaala Patthar",
            options: ["Kaala Patthar", "Shahenshah", "Muqaddar Ka Sikandar", "Laawaris"],
            hint: "1979 Amitabh coal mine film"
        },
        {
            dialogue: "Tension lene ka nahi, sirf dene ka",
            correct: "Munna Bhai MBBS",
            options: ["Munna Bhai MBBS", "Lage Raho Munna Bhai", "3 Idiots", "PK"],
            hint: "2003 Sanjay Dutt"
        },
        {
            dialogue: "Mujhe drugs do",
            correct: "Udta Punjab",
            options: ["Udta Punjab", "Haider", "Rockstar", "Tamasha"],
            hint: "2016 Shahid Kapoor"
        },
        {
            dialogue: "Thappad se darr nahi lagta sahab, pyaar se lagta hai",
            correct: "Dabangg",
            options: ["Dabangg", "Singham", "Rowdy Rathore", "Wanted"],
            hint: "2010 Salman Khan"
        },
        {
            dialogue: "Dosti ka ek usool hai madam, no sorry, no thank you",
            correct: "Maine Pyar Kiya",
            options: ["Maine Pyar Kiya", "Hum Aapke Hain Koun", "Hum Saath Saath Hain", "Vivah"],
            hint: "1989 Salman debut hit"
        }
    ],
    
    // Level 4: Classic Movies
    level4: [
        {
            dialogue: "Khush toh bohot hoge tum, ke tumne Vijay Deenanath Chauhan ko maar diya",
            correct: "Agneepath",
            options: ["Agneepath", "Deewar", "Trishul", "Coolie"],
            hint: "1990 revenge drama"
        },
        {
            dialogue: "Rishtey mein toh hum tumhare baap lagte hai",
            correct: "Shahenshah",
            options: ["Shahenshah", "Coolie", "Agneepath", "Muqaddar Ka Sikandar"],
            hint: "1988 vigilante film"
        },
        {
            dialogue: "Thoda khao, thoda phenko",
            correct: "Padosan",
            options: ["Padosan", "Chalti Ka Naam Gaadi", "Half Ticket", "Bombay to Goa"],
            hint: "1968 Kishore Kumar comedy"
        },
        {
            dialogue: "Main hoon na",
            correct: "Main Hoon Na",
            options: ["Main Hoon Na", "Swades", "Chak De India", "Kal Ho Naa Ho"],
            hint: "2004 SRK military film"
        },
        {
            dialogue: "Aaj khush toh bahut hoge tum",
            correct: "Deewar",
            options: ["Deewar", "Trishul", "Don", "Muqaddar Ka Sikandar"],
            hint: "1975 brothers conflict"
        },
        {
            dialogue: "Basanti, in kutto ke samne mat nachna",
            correct: "Sholay",
            options: ["Sholay", "Amar Akbar Anthony", "Don", "Coolie"],
            hint: "1975 Veeru to Basanti"
        },
        {
            dialogue: "Parampara, pratishtha, anushasan. Yeh is gurukul ke teen stambh hai",
            correct: "Mohabbatein",
            options: ["Mohabbatein", "Chalte Chalte", "Kabhi Alvida Naa Kehna", "Kal Ho Naa Ho"],
            hint: "2000 Amitabh-SRK"
        },
        {
            dialogue: "Bhai ka birthday hai, aur bhai apne birthday par kisi ko maarta nahi, sirf chhod deta hai",
            correct: "Tere Naam",
            options: ["Tere Naam", "Wanted", "Ready", "Bodyguard"],
            hint: "2003 Salman intense role"
        },
        {
            dialogue: "Tumhara naam kya hai Basanti?",
            correct: "Sholay",
            options: ["Sholay", "Silsila", "Kabhi Kabhie", "Deewar"],
            hint: "1975 Veeru's famous line"
        },
        {
            dialogue: "Prem rog ho jayega, iska koi ilaaj nahi",
            correct: "Prem Rog",
            options: ["Prem Rog", "Bobby", "Chandni", "Saagar"],
            hint: "1982 Rishi Kapoor film"
        }
    ],
    
    // Level 5: Classic and Challenging
    level5: [
        {
            dialogue: "Aaj mere paas bangla hai, gaadi hai, paisa hai, tumhare paas kya hai?",
            correct: "Deewar",
            options: ["Deewar", "Trishul", "Kaala Patthar", "Shakti"],
            hint: "1975 iconic dialogue"
        },
        {
            dialogue: "Yeh andar ki baat hai",
            correct: "Hera Pheri",
            options: ["Hera Pheri", "Phir Hera Pheri", "Gol Maal", "Chupke Chupke"],
            hint: "2000 Paresh Rawal"
        },
        {
            dialogue: "Namaazi khiladi yeh hai ke jeet jaye",
            correct: "Guide",
            options: ["Guide", "Jewel Thief", "Teesri Manzil", "Johny Mera Naam"],
            hint: "1965 Dev Anand classic"
        },
        {
            dialogue: "Ek ladki ko dekha toh aisa laga",
            correct: "1942: A Love Story",
            options: ["1942: A Love Story", "Dilwale Dulhania Le Jayenge", "Qayamat Se Qayamat Tak", "Dil"],
            hint: "1994 period romance"
        },
        {
            dialogue: "Dosti ka ek hi matlab hota hai, dost ki zaroorat ko pehchanna",
            correct: "Dosti",
            options: ["Dosti", "Anand", "Mili", "Guddi"],
            hint: "1964 friendship classic"
        },
        {
            dialogue: "Babumoshai, zindagi badi honi chahiye, lambi nahi",
            correct: "Anand",
            options: ["Anand", "Mili", "Abhimaan", "Guddi"],
            hint: "1971 Rajesh Khanna"
        },
        {
            dialogue: "Zindagi ek safar hai suhana",
            correct: "Andaz",
            options: ["Andaz", "Aradhana", "Safar", "Aap Ki Kasam"],
            hint: "1971 Rajesh Khanna hit"
        },
        {
            dialogue: "Pushpa, I hate tears",
            correct: "Amar Prem",
            options: ["Amar Prem", "Anand", "Aradhana", "Safar"],
            hint: "1972 classic romance"
        },
        {
            dialogue: "Bade miyan toh bade miyan, chote miyan subhan allah",
            correct: "Bade Miyan Chote Miyan",
            options: ["Bade Miyan Chote Miyan", "Hera Pheri", "Andaz Apna Apna", "Coolie No. 1"],
            hint: "1998 Amitabh-Govinda"
        },
        {
            dialogue: "Hum jahan khade ho jaate hai, line wahi se shuru hoti hai",
            correct: "Kaalia",
            options: ["Kaalia", "Namak Halaal", "Satte Pe Satta", "Naseeb"],
            hint: "1981 Amitabh action"
        }
    ]
};

// ============================================
// GAME STATE
// ============================================

let gameState = {
    currentLevel: 1,
    currentQuestionIndex: 0,
    lives: 3,
    usedQuestions: new Set(),
    score: 0
};

// ============================================
// DOM ELEMENTS
// ============================================

const screens = {
    start: document.getElementById('startScreen'),
    game: document.getElementById('gameScreen'),
    victory: document.getElementById('victoryScreen'),
    gameOver: document.getElementById('gameOverScreen')
};

const buttons = {
    start: document.getElementById('startBtn'),
    playAgain: document.getElementById('playAgainBtn'),
    retry: document.getElementById('retryBtn'),
    themeToggle: document.getElementById('themeToggle')
};

const displays = {
    currentLevel: document.getElementById('currentLevel'),
    currentQuestion: document.getElementById('currentQuestion'),
    livesDisplay: document.getElementById('livesDisplay'),
    dialogueText: document.getElementById('dialogueText'),
    hintText: document.getElementById('hintText'),
    optionsContainer: document.getElementById('optionsContainer'),
    progressBar: document.getElementById('progressBar'),
    feedbackMsg: document.getElementById('feedbackMsg'),
    finalScore: document.getElementById('finalScore'),
    gameOverStats: document.getElementById('gameOverStats')
};

const fireworksCanvas = document.getElementById('fireworksCanvas');

// ============================================
// INITIALIZATION
// ============================================

function init() {
    // Load theme from localStorage
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    
    // Event Listeners
    buttons.start.addEventListener('click', startGame);
    buttons.playAgain.addEventListener('click', startGame);
    buttons.retry.addEventListener('click', startGame);
    buttons.themeToggle.addEventListener('click', toggleTheme);
    
    // Show start screen
    showScreen('start');
}

// ============================================
// THEME TOGGLE
// ============================================

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

// ============================================
// SCREEN MANAGEMENT
// ============================================

function showScreen(screenName) {
    Object.values(screens).forEach(screen => screen.classList.remove('active'));
    screens[screenName].classList.add('active');
}

// ============================================
// GAME FUNCTIONS
// ============================================

function startGame() {
    // Reset game state
    gameState = {
        currentLevel: 1,
        currentQuestionIndex: 0,
        lives: 3,
        usedQuestions: new Set(),
        score: 0
    };
    
    updateDisplay();
    updateLevelIndicators();
    showScreen('game');
    loadQuestion();
}

function loadQuestion() {
    // Get questions for current level
    const levelKey = `level${gameState.currentLevel}`;
    const levelQuestions = QUESTIONS_BANK[levelKey];
    
    // Get unused question from current level
    const availableQuestions = levelQuestions.filter((_, index) => {
        const questionId = `${levelKey}-${index}`;
        return !gameState.usedQuestions.has(questionId);
    });
    
    if (availableQuestions.length === 0) {
        // Level completed
        levelComplete();
        return;
    }
    
    // Select random question from available
    const randomIndex = Math.floor(Math.random() * availableQuestions.length);
    const question = availableQuestions[randomIndex];
    
    // Mark question as used
    const originalIndex = levelQuestions.indexOf(question);
    const questionId = `${levelKey}-${originalIndex}`;
    gameState.usedQuestions.add(questionId);
    
    // Display question
    displayQuestion(question);
    
    // Update question counter
    gameState.currentQuestionIndex++;
    updateDisplay();
}

function displayQuestion(question) {
    // Clear feedback
    displays.feedbackMsg.classList.remove('show', 'correct', 'wrong');
    displays.feedbackMsg.textContent = '';
    
    // Display dialogue and hint
    displays.dialogueText.textContent = `"${question.dialogue}"`;
    displays.hintText.textContent = question.hint ? `Hint: ${question.hint}` : '';
    
    // Shuffle options
    const shuffledOptions = [...question.options].sort(() => Math.random() - 0.5);
    
    // Clear and create option buttons
    displays.optionsContainer.innerHTML = '';
    shuffledOptions.forEach(option => {
        const btn = document.createElement('button');
        btn.className = 'option-btn';
        btn.textContent = option;
        btn.addEventListener('click', () => checkAnswer(option, question.correct, btn));
        displays.optionsContainer.appendChild(btn);
    });
}

function checkAnswer(selected, correct, btn) {
    // Disable all buttons
    const allButtons = displays.optionsContainer.querySelectorAll('.option-btn');
    allButtons.forEach(button => button.disabled = true);
    
    if (selected === correct) {
        // Correct answer
        btn.classList.add('correct');
        displays.feedbackMsg.textContent = '🎉 Correct! Well done!';
        displays.feedbackMsg.classList.add('show', 'correct');
        gameState.score += 10;
        
        setTimeout(() => {
            loadQuestion();
        }, 1500);
    } else {
        // Wrong answer
        btn.classList.add('wrong');
        
        // Highlight correct answer
        allButtons.forEach(button => {
            if (button.textContent === correct) {
                button.classList.add('correct');
            }
        });
        
        gameState.lives--;
        updateLives();
        
        displays.feedbackMsg.textContent = `❌ Wrong! Correct answer: ${correct}`;
        displays.feedbackMsg.classList.add('show', 'wrong');
        
        if (gameState.lives <= 0) {
            setTimeout(() => {
                gameOver();
            }, 2000);
        } else {
            setTimeout(() => {
                // Restart from Level 1
                gameState.currentLevel = 1;
                gameState.currentQuestionIndex = 0;
                gameState.usedQuestions.clear();
                updateDisplay();
                updateLevelIndicators();
                loadQuestion();
            }, 2000);
        }
    }
}

function levelComplete() {
    if (gameState.currentLevel >= 5) {
        // All levels completed - Victory!
        victory();
    } else {
        // Move to next level
        gameState.currentLevel++;
        gameState.currentQuestionIndex = 0;
        updateDisplay();
        updateLevelIndicators();
        
        // Show level up message
        displays.feedbackMsg.textContent = `🎊 Level ${gameState.currentLevel - 1} Complete! Moving to Level ${gameState.currentLevel}`;
        displays.feedbackMsg.classList.add('show', 'correct');
        
        setTimeout(() => {
            displays.feedbackMsg.classList.remove('show');
            loadQuestion();
        }, 2000);
    }
}

function victory() {
    displays.finalScore.textContent = `Final Score: ${gameState.score} points!`;
    showScreen('victory');
    
    // Start fireworks animation
    startFireworks();
    
    // Save progress
    saveProgress();
}

function gameOver() {
    displays.gameOverStats.innerHTML = `
        You reached Level ${gameState.currentLevel}<br>
        Score: ${gameState.score} points
    `;
    showScreen('gameOver');
}

function updateDisplay() {
    displays.currentLevel.textContent = gameState.currentLevel;
    displays.currentQuestion.textContent = gameState.currentQuestionIndex;
    updateLives();
    updateProgressBar();
}

function updateLives() {
    const hearts = '❤️'.repeat(gameState.lives) + '🖤'.repeat(3 - gameState.lives);
    displays.livesDisplay.textContent = hearts;
}

function updateProgressBar() {
    const totalQuestionsInLevel = 10;
    const progress = (gameState.currentQuestionIndex / totalQuestionsInLevel) * 100;
    displays.progressBar.style.width = `${progress}%`;
}

function updateLevelIndicators() {
    const indicators = document.querySelectorAll('.level-indicator');
    indicators.forEach((indicator, index) => {
        const level = index + 1;
        indicator.classList.remove('active', 'completed');
        
        if (level === gameState.currentLevel) {
            indicator.classList.add('active');
        } else if (level < gameState.currentLevel) {
            indicator.classList.add('completed');
        }
    });
}

// ============================================
// FIREWORKS ANIMATION
// ============================================

function startFireworks() {
    fireworksCanvas.classList.add('active');
    const ctx = fireworksCanvas.getContext('2d');
    
    // Set canvas size
    fireworksCanvas.width = window.innerWidth;
    fireworksCanvas.height = window.innerHeight;
    
    const particles = [];
    const fireworks = [];
    
    class Particle {
        constructor(x, y, color) {
            this.x = x;
            this.y = y;
            this.color = color;
            this.velocity = {
                x: (Math.random() - 0.5) * 6,
                y: (Math.random() - 0.5) * 6
            };
            this.alpha = 1;
            this.decay = Math.random() * 0.02 + 0.01;
        }
        
        update() {
            this.velocity.y += 0.1;
            this.x += this.velocity.x;
            this.y += this.velocity.y;
            this.alpha -= this.decay;
        }
        
        draw() {
            ctx.save();
            ctx.globalAlpha = this.alpha;
            ctx.fillStyle = this.color;
            ctx.beginPath();
            ctx.arc(this.x, this.y, 3, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
        }
    }
    
    class Firework {
        constructor() {
            this.x = Math.random() * fireworksCanvas.width;
            this.y = fireworksCanvas.height;
            this.targetY = Math.random() * fireworksCanvas.height * 0.5;
            this.color = `hsl(${Math.random() * 360}, 100%, 50%)`;
            this.velocity = 5;
        }
        
        update() {
            this.y -= this.velocity;
            
            if (this.y <= this.targetY) {
                this.explode();
                return true;
            }
            return false;
        }
        
        draw() {
            ctx.fillStyle = this.color;
            ctx.beginPath();
            ctx.arc(this.x, this.y, 3, 0, Math.PI * 2);
            ctx.fill();
        }
        
        explode() {
            for (let i = 0; i < 50; i++) {
                particles.push(new Particle(this.x, this.y, this.color));
            }
        }
    }
    
    function animate() {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
        ctx.fillRect(0, 0, fireworksCanvas.width, fireworksCanvas.height);
        
        // Create new fireworks
        if (Math.random() < 0.1) {
            fireworks.push(new Firework());
        }
        
        // Update and draw fireworks
        for (let i = fireworks.length - 1; i >= 0; i--) {
            fireworks[i].draw();
            if (fireworks[i].update()) {
                fireworks.splice(i, 1);
            }
        }
        
        // Update and draw particles
        for (let i = particles.length - 1; i >= 0; i--) {
            particles[i].update();
            particles[i].draw();
            
            if (particles[i].alpha <= 0) {
                particles.splice(i, 1);
            }
        }
        
        if (particles.length > 0 || fireworks.length > 0) {
            requestAnimationFrame(animate);
        } else {
            fireworksCanvas.classList.remove('active');
        }
    }
    
    // Run animation for 8 seconds
    animate();
    setTimeout(() => {
        particles.length = 0;
        fireworks.length = 0;
    }, 8000);
}

// ============================================
// LOCAL STORAGE
// ============================================

function saveProgress() {
    const progress = {
        highScore: Math.max(gameState.score, parseInt(localStorage.getItem('highScore') || 0)),
        completedLevels: 5
    };
    
    localStorage.setItem('highScore', progress.highScore);
    localStorage.setItem('completedLevels', progress.completedLevels);
}

function loadProgress() {
    const highScore = localStorage.getItem('highScore') || 0;
    const completedLevels = localStorage.getItem('completedLevels') || 0;
    
    return { highScore, completedLevels };
}

// ============================================
// RESPONSIVE CANVAS
// ============================================

window.addEventListener('resize', () => {
    if (fireworksCanvas.classList.contains('active')) {
        fireworksCanvas.width = window.innerWidth;
        fireworksCanvas.height = window.innerHeight;
    }
});

// ============================================
// START THE GAME
// ============================================

document.addEventListener('DOMContentLoaded', init);
