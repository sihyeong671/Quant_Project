
var chartJsonSet = [chartSet['1'], chartSet['2'], chartSet['3'], chartSet['4'], chartSet['5']];
var chartBaseSet = [1, 2, 3, 4, 5];
var jsonDataSet = chartJsonSet;

var data = {
    labels: [
      'Red',
      'Green',
      'Yellow',
      'Grey',
      'Blue'
    ],
    datasets: [{
      label: 'My First Dataset',
      data: jsonDataSet,
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
var line_C_config = {
    type: 'line',
    data,
    options: {}
};
var line_C = new Chart(
    document.querySelector('#line_chart'),
    line_C_config
); 

// RADER
var rader_C_config = {
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
var rader_C = new Chart(
    document.querySelector('#rader_chart'),
    rader_C_config
); 

// DOUGHNUT
var doughnut_C_config = {
    type: 'doughnut',
    data,
    options: {}
};
var doughnut_C = new Chart(
    document.querySelector('#doughnut_chart'),
    doughnut_C_config
); 

// POLAR
var polar_C_config = {
    type: 'polarArea',
    data,
    options: {}
};
var polar_C = new Chart(
    document.querySelector('#polar_chart'),
    polar_C_config
); 

var $chartCanvas = $('<canvas id="line_chart"></canvas>');
var chartChanger = document.querySelector('.chartChanger');
chartChanger.addEventListener('click', ()=>{
    $('#line_chart').remove()
    $('.line_chart-wrapper').append($chartCanvas);
    jsonDataSet = chartJsonSet;
    line_C = new Chart(
        document.querySelector('#line_chart'),
        line_C_config
    ); 
});