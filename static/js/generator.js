// function that randomly selects quote from dict.

let btn = document.getElementById('btn');
let output = document.getElementById('output');
let quotes = 
    [' "If you want to find the secrets of the universe, think in terms of energy, frequency and vibration." - Nikola Tesla',
     ' "Sound is the Medicine of the future." - Edgar Cayce',
     ' "If you do not make time for your wellness, you will be forced to make time for your illness." - N/A',
    ];


btn.addEventListener('click', function(){
    var randomQuote = quotes[Math.floor(Math.random() * quotes.length)]
    output.innerHTML = randomQuote;
})

// what I think it should be like:

// document.querySelector('#output').addEventListener('load', (evt) => {
//     evt.preventDefault();
    
//     let output = document.getElementById('output');
//     let quotes = 
//         [' "If you want to find the secrets of the universe, think in terms of energy, frequency and vibration." - Nikola Tesla',
//          ' "Sound is the Medicine of the future." - Edgar Cayce',
//          ' "If you do not make time for your wellness, you will be forced to make time for your illness." - N/A',
//         ];
    
    
//     output.addEventListener('load', function(){
//         var randomQuote = quotes[Math.floor(Math.random() * quotes.length)]
//         output.innerHTML = randomQuote;
//     })
    
//     });