const data = {
    labels: [
      'Red',
      'Green',
      'Yellow',
      'Grey',
      'Blue'
    ],
    datasets: [{
      label: 'My First Dataset',
      data: [11, 16, 7, 3, 14],
      backgroundColor: [
        'rgb(255, 99, 132)',
        'rgb(75, 192, 192)',
        'rgb(255, 205, 86)',
        'rgb(201, 203, 207)',
        'rgb(54, 162, 235)'
      ],
      borderColor: 'rgb(100, 100, 100)',
    }]
};


// LINE
const line_C_config = {
    type: 'line',
    data,
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    fontSize: 150
                }
            }]
        }
    }
};
const line_C = new Chart(
    document.querySelector('#line_chart'),
    line_C_config
); 

// RADER
const rader_C_config = {
    type: 'radar',
    data,
    options: {
        elements: {
            line: {
                borderWidth: 3
            }
        }
    }
};
const rader_C = new Chart(
    document.querySelector('#rader_chart'),
    rader_C_config
); 

// DOUGHNUT
const doughnut_C_config = {
    type: 'doughnut',
    data,
    options: {}
};
const doughnut_C = new Chart(
    document.querySelector('#doughnut_chart'),
    doughnut_C_config
); 

// POLAR
const polar_C_config = {
    type: 'polarArea',
    data,
    options: {}
};
const polar_C = new Chart(
    document.querySelector('#polar_chart'),
    polar_C_config
); 

