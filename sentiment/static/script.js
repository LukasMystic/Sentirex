
const style = document.createElement('style');
style.innerHTML = `
    ::-webkit-scrollbar {
        width: 8px; 
        height: 8px; 
    }

    ::-webkit-scrollbar-thumb {
        background-color: transparent; 
        border-radius: 4px;
    }

    ::-webkit-scrollbar-track {
        background-color: transparent; 
    }

    body {
        scrollbar-width: thin; 
        scrollbar-color: transparent transparent; 
    }
`;
document.head.appendChild(style);


function countTo(element, targetNumber) {
    let counter = 0;
    const increment = 1; 
    const intervalDuration = 5; 
    const delayDuration = 500; 
    const totalCounts = Math.ceil(targetNumber / increment);
    let currentCount = 0; 

  
    const interval = setInterval(() => {
      element.textContent = counter;
      counter += increment; 
      currentCount++;
  
    
      if (currentCount > totalCounts - 3) {
        clearInterval(interval); 
        
        setTimeout(() => {
          
          const finalInterval = setInterval(() => {
            element.textContent = counter;
            counter += increment; 
            currentCount++;
  
            if (currentCount >= totalCounts) {
              clearInterval(finalInterval);
              element.textContent = targetNumber; 
            }
          }, delayDuration); 
        }, intervalDuration);
      }
  
      
      if (counter > targetNumber) {
        clearInterval(interval);
        element.textContent = targetNumber; 
      }
    }, intervalDuration); 
  }


  function smoothScrollTo(element, duration) {
    const targetPosition = element.getBoundingClientRect().top + window.pageYOffset;
    const startPosition = window.pageYOffset;
    const distance = targetPosition - startPosition;
    let startTime = null;
  
    function animation(currentTime) {
      if (startTime === null) startTime = currentTime;
      const timeElapsed = currentTime - startTime;
      const run = ease(timeElapsed, startPosition, distance, duration);
      window.scrollTo(0, run);
      if (timeElapsed < duration) requestAnimationFrame(animation);
    }
  
    function ease(t, b, c, d) {
      t /= d / 2;
      if (t < 1) return c / 2 * t * t + b;
      t--;
      return -c / 2 * (t * (t - 2) - 1) + b;
    }
  
    requestAnimationFrame(animation);
  }

document.addEventListener('DOMContentLoaded', () => {
    const goUpBtn = document.querySelector('.go-up-btn'); 

    const boxes = document.querySelectorAll('.decor-analyze > .pattern > div');

    const userAnalysed = document.getElementById('user');
    const sendRecommendation =document.getElementById('recommend');
    const processingSpeed =document.getElementById('process');

    const heroBtn = document.querySelector('.hero-button');

    const nav = document.querySelector('nav');

    const aboutBtn = document.querySelector('.nav-links > #nl1');
    const contactBtn = document.querySelector('.nav-links > #nl2');

    const analyseBtn = document.querySelector('#analyze-button')
    const summaryArea = document.querySelector('.summary')
    


    let currentIndex = 0;
    let boxesLength = boxes.length;
    let numAnalysed = parseInt(userAnalysed.textContent,10);
    let numRecommend = parseInt(sendRecommendation.textContent,10);
    let numProcess = parseInt(processingSpeed.textContent,10);



  
    goUpBtn.addEventListener('click', function() {
      const top = document.querySelector('html')
      smoothScrollTo(top , 1000);

    });

    setInterval(() => {
        boxes.forEach(box => box.classList.remove('active'));
    
        boxes[currentIndex].classList.add('active');
    
        currentIndex = (currentIndex + 1) % boxesLength;
    }, 500); 


    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
          
        if (entry.isIntersecting) {
          countTo(userAnalysed, numAnalysed);
          countTo(sendRecommendation, numRecommend);
          countTo(processingSpeed, numProcess);
          observer.unobserve(userAnalysed, sendRecommendation, processingSpeed); 

          goUpBtn.classList.add('hidden');

        }else{
          goUpBtn.classList.remove('hidden');
        }
      });
    }, { threshold: 0.5 });

    observer.observe(userAnalysed,sendRecommendation,processingSpeed);
    observer.observe(nav);

    heroBtn.addEventListener('click', function() {
       const sectionAnalyze = document.querySelector('section.analyze');
       smoothScrollTo(sectionAnalyze,1000); //ms
    });

    aboutBtn.addEventListener('click', function(){
      const about = document.querySelector('section.intro');
      smoothScrollTo(about, 1000); //ms
    });
    
    contactBtn.addEventListener('click', function(){
      const contact = document.querySelector('section.cot');
      smoothScrollTo(contact,1000); //ms
    });

    analyseBtn.addEventListener('click', function(){
      smoothScrollTo(summaryArea,1000);
    })
    
  
});
document.getElementById('sentimentForm').addEventListener('submit', async function (e) {
  e.preventDefault(); 
  const textArea = document.getElementById('ta-post');
  const textValue = textArea.value;

  if (!textValue) {
      alert('Please enter some text to analyze.');
      return;
  }

  try {
      const response = await fetch('/predict/', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/x-www-form-urlencoded', 
              'X-CSRFToken': getCSRFToken(), 
          },
          body: `text=${encodeURIComponent(textValue)}`
      });

     
      const result = await response.json();

      if (response.ok) {
          
          document.getElementById('prediction').innerText = result.prediction;
      } else {
          alert(result.error || 'An error occurred.');
      }
  } catch (error) {
      console.error('Error:', error);
      alert('Failed to connect to the server.');
  }
});

function sendText(event) {
  event.preventDefault();

  const text = document.getElementById('ta-post').value;
  
  if (text.trim() === '') {
      alert('Masukan Text!');
      return;
  }

  const data = new FormData();
  data.append('text', text);

  fetch('/predict/', {
      method: 'POST',
      body: data
  })
  .then(response => response.json())
  .then(result => {
    if (result.error) {
        alert(result.error);
    } else {
        
        const sentimentPercentages = result.sentiment_percentages;

        
        const highestSentiment = Object.keys(sentimentPercentages).reduce((a, b) => 
            sentimentPercentages[a] > sentimentPercentages[b] ? a : b
        );

        const conclusionText = `Berdasarkan analisa kami, sentimen Anda tergolong sebagai ${highestSentiment}, dengan persentase ${sentimentPercentages[highestSentiment].toFixed(2)}% dari total sentimen.`;
        document.querySelector('.conclusion p').innerText = conclusionText;

       
        updateCharts(sentimentPercentages);
    }
})

  .catch(error => {
      alert('Error occurred: ' + error.message);
  });
}


var barChartInstance = null;
var pieChartInstance = null;

function updateCharts(sentimentPercentages) {
  const chartData = {
      labels: ['Negatif', 'Positif', 'Netral'],
      datasets: [{
          label: 'Persentase Sentiment',
          data: [sentimentPercentages['Negative'], sentimentPercentages['Positive'], sentimentPercentages['Neutral']],
          backgroundColor: ['#FF4E4E', '#4EAF41', '#FFC107'],
      }]
  };

  const barCtx = document.getElementById('barChart').getContext('2d');
  const pieCtx = document.getElementById('pieChart').getContext('2d');


  if (barChartInstance) {
      barChartInstance.destroy(); 
  }
  barChartInstance = new Chart(barCtx, {
      type: 'bar',
      data: chartData,
      options: {
          responsive: true,
          maintainAspectRatio: false,  
          plugins: {
              legend: {
                  labels: {
                      color: 'white' 
                  }
              },
              title: {
                  display: true,
                  text: 'Sentimen Analisis',
                  color: 'white',
              },
              tooltip: {
                  callbacks: {
                      label: function(tooltipItem) {
                          return tooltipItem.label + ': ' + tooltipItem.raw.toFixed(2) + '%';
                      }
                  },
                  bodyColor: 'white', 
                  titleColor: 'white',
              }
          },
          scales: {
              x: {
                  ticks: {
                      color: 'white' 
                  },
                  grid: {
                      color: 'white' 
                  },
                  border: {
                      color: 'white' 
                  }
              },
              y: {
                  ticks: {
                      color: 'white', 
                      beginAtZero: true, 
                      stepSize: 10 
                  },
                  grid: {
                      color: 'white'
                  },
                  border: {
                      color: 'white'
                  },
                  min: 0,   
                  max: 100 
              }
          }
      },
      height: 500  
  });


  if (pieChartInstance) {
      pieChartInstance.destroy(); 
  }
  
  const pieCanvas = document.getElementById('pieChart');
  pieCanvas.width = 10;  
  pieCanvas.height = 10;

  pieChartInstance = new Chart(pieCtx, {
      type: 'pie',
      data: chartData,
      options: {
          responsive: true,
          maintainAspectRatio: false, 
          plugins: {
              legend: {
                  labels: {
                      color: 'white' 
                  }
              },
              tooltip: {
                  callbacks: {
                      label: function(tooltipItem) {
                          return tooltipItem.label + ': ' + tooltipItem.raw.toFixed(2) + '%';
                      }
                  },
                  bodyColor: 'white', 
                  titleColor: 'white', 
              }
          }
      }
  });
}

document.getElementById('charts-section').scrollIntoView({ behavior: 'smooth' });


