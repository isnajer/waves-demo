// function that randomly selects quote from dict.

let quote_gen = document.getElementById('quote_gen');
let output = document.getElementById('output');
let quotes = 
    [' "If you want to find the secrets of the universe, think in terms of energy, frequency and vibration." - Nikola Tesla',
     ' "Sound is the Medicine of the future."    - Edgar Cayce',
     ' "If you do not make time for your wellness, you will be forced to make time for your illness."    - N/A',
     ' “Keep taking time for yourself until you are you again.”    —Lalah Delia ',
     ' “Almost everything will work again if you unplug it for a few minutes, including you.”    — Anne Lamott',
     ' “Your work is to discover your world and then with all your heart give yourself to it.”    — Buddha',
     ' “The thing that is really hard, and really amazing, is giving up on being perfect and beginning the work of becoming yourself.”    — Anna Quindlen',
     ' “Women need solitude in order to find again the true essence of themselves.”    ― Anne Morrow Lindbergh',
     ' “If you don’t love yourself, nobody will. Not only that, you won’t be good at loving anyone else. Loving starts with the self.”   — Wayne Dyer',
     ' “It is not the mountain we conquer but ourselves.”   — Sir Edmund Hillary',
     ' “Loving yourself isn’t vanity. It’s sanity.”    — Katrina Mayer',
     ' “Never bend your head. Always hold it high. Look the world straight in the face.”    — Helen Keller',
     ' “You find peace not by rearranging the circumstances of your life, but by realizing who you are at the deepest level.”    — Eckhart Tolle',
     ' “Part of courage is simple consistency.”    — Peggy Noonan',
     ' “Breathe. Let go. And remind yourself that this very moment is the only one you know you have for sure."    — Oprah Winfrey',
     ' “You are magnificent beyond measure, perfect in your imperfections, and wonderfully made.”    — Abiola Abrams',
     ' “As you grow older, you will discover that you have two hands, one for helping yourself, the other for helping others.”    — Maya Angelou',
     ' “To love oneself is the beginning of a lifelong romance.”   — Oscar Wilde',
     ' "Self-care means giving yourself permission to pause.”    — Cecilia Tran',
     ' "Be patient with yourself. Self-growth is tender; it’s holy ground. There’s no greater investment.”    — Stephen Covey',
     ' "Self-care doesn’t necessarily mean jogging!”    — Sandra Oh',
     ' "The most important investment you can make is in yourself. Very few people get anything like their potential horsepower translated into the actual horsepower of their output in life. Potential exceeds realization for many people ... The best asset is your own self. You can become to an enormous degree the person you want to be.”    — Warren Buffett',
     ' "You wash your hands when you shake a bunch of hands. You have to wash your energy when you’re around people. It’s hard for me to say self-care is washing, although I think it is. So I made music for self-care. That’s what it’s for.”    — India Arie',
     ' "If you can’t fly then run, if you can’t run then walk, if you can’t walk then crawl, but whatever you do you have to keep moving forward.”    — Martin Luther King Jr.',
     ' "Forgiveness isn’t just the absence of anger. I think it’s also the presence of self-love, when you actually begin to value yourself.”    — Tara Westover',
     ' "Self-care equals success. You’re going to be more successful if you take care of yourself and you’re healthy.”    — Beth Behrs',
     ' "Every small positive change we make in ourselves repays us in confidence in the future.”    — Alice Walker',
     ' "Yesterday I was clever, so I wanted to change the world. Today I am wise, so I am changing myself.”    — Rumi',
     ' "The most creative act you will ever undertake is the act of creating yourself.”    — Deepak Chopra',
     ' "Do something nice for yourself today. Find some quiet, sit in stillness, breathe. Put your problems on pause. You deserve a break.”    ―Akiroq Brost'


    ];


window.onload =  function(){
    const randomQuote = quotes[Math.floor(Math.random() * quotes.length)]
    output.innerHTML = randomQuote;
};