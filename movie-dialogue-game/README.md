# 🎬 Bollywood Dialogue Quiz

Test your Bollywood knowledge by guessing movies from famous dialogues!

## 🎮 How to Play

1. **Start the Quiz** - Click "Start Quiz" to begin
2. **Answer Questions** - Read the dialogue and select the correct movie from 4 options
3. **Progress Through Levels** - Complete all 10 questions to advance to the next level
4. **Watch Your Lives** - You have 3 lives. Wrong answer? Start from Level 1!
5. **Win the Game** - Complete all 5 levels to see the victory fireworks! 🎉

## ✨ Features

- **50 Unique Questions** across 5 difficulty levels
- **3 Lives System** - visual hearts tracking
- **Light/Dark Mode** - toggle with the sun/moon button
- **Responsive Design** - works on mobile and desktop
- **Progress Tracking** - see your level completion
- **Celebration Animation** - fireworks when you win!
- **High Score** - saved in your browser

## 🎯 Difficulty Levels

1. **Level 1**: Popular Recent Movies (2009-2023)
2. **Level 2**: Mix of Popular and Recent
3. **Level 3**: Mix of Popular and Classic
4. **Level 4**: Classic Movies
5. **Level 5**: Classic and Challenging

## 🔧 Technical Details

### Files
- `index.html` - Main HTML structure
- `styles.css` - Styling with light/dark mode
- `script.js` - Game logic and questions

### Technologies Used
- **HTML5** - Structure and Canvas for fireworks
- **CSS3** - Animations, transitions, and responsive design
- **Vanilla JavaScript** - Game logic and interactivity
- **LocalStorage** - Save theme preference and high scores

### ChatGPT API Integration (Optional)

The game includes a commented-out ChatGPT API integration for generating dynamic questions. To enable:

1. Open `script.js`
2. Find the commented section at the top (lines 6-37)
3. Add your OpenAI API key: `const OPENAI_API_KEY = 'your-api-key-here';`
4. Uncomment the code block
5. Modify the `loadQuestion()` function to use the API

## 🚀 Getting Started

### Local Development

1. Clone the repository
2. Navigate to `/movie-dialogue-game/`
3. Open `index.html` in a browser
   - Or use a local server: `python -m http.server 8000`

### Live Demo

Visit: [https://shubhamsnehil07.github.io/movie-dialogue-game/](https://shubhamsnehil07.github.io/movie-dialogue-game/)

## 📱 Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🎨 Customization

### Change Theme Colors

Edit CSS variables in `styles.css`:

```css
:root {
    --bg-primary: #fff5e6;
    --accent-color: #ff6b6b;
    /* ... more variables */
}
```

### Add More Questions

Edit `QUESTIONS_BANK` in `script.js`:

```javascript
const QUESTIONS_BANK = {
    level1: [
        {
            dialogue: "Your dialogue here",
            correct: "Movie Name",
            options: ["Option1", "Option2", "Option3", "Option4"],
            hint: "Hint text"
        }
    ]
};
```

## 📄 License

This project is open source and available for personal and educational use.

## 👨‍💻 Developer

Created by Shubham Snehil

---

**Enjoy the quiz and test your Bollywood knowledge! 🎬✨**
