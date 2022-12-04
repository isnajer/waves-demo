fetch('/charts')
  .then((response) => response.json())
  .then((brain_wave_count) => 
    new Chart(document.querySelector('#bar-chart'), {
      type: 'bar',
      data: {
        labels: ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma'],
        datasets: [{
            label: 'Brain Wave Focus',
            data: [ 
              brain_wave_count[1], brain_wave_count[2], brain_wave_count[3], brain_wave_count[4], brain_wave_count[5]
            ],
          }],
      },
      options: {
          datasets: {
            bar: {
              barThickness: 50,
              // We use a function to automatically set the background color of
              // each bar in the bar chart.
              //
              // There are many other properties that accept functions. For more
              // information see: https://www.chartjs.org/docs/latest/general/options.html#scriptable-options
              backgroundColor: () =>
                // `randomColor` is a JS module we found off GitHub: https://github.com/davidmerfield/randomColor
                // We imported it in templates/chartjs.html
                randomColor(),
            },
          },
          scales: {
            // This is where you can configure x- and y-axes if you don't like the
            // automatic range that Chart.js sets for you.
            //
            // For more info see: https://www.chartjs.org/docs/latest/axes/cartesian/
            yAxes: [
              {
                ticks: {
                  suggestedMin: 0,
                  suggestedMax: 40,
                  fontSize: 20,
                },
              },
            ],
          },
        },
    }))
