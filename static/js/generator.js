// function that randomly selects quote from dict.

let quote_gen = document.getElementById('quote_gen');
let output = document.getElementById('output');
let quotes = 
    [' "If you want to find the secrets of the universe, think in terms of energy, frequency and vibration." - Nikola Tesla',
     ' "Sound is the Medicine of the future." - Edgar Cayce',
     ' "If you don not make time for your wellness, you will be forced to make time for your illness." - N/A',
    ];


window.onload =  function(){
    const randomQuote = quotes[Math.floor(Math.random() * quotes.length)]
    output.innerHTML = randomQuote;
};