const fadeElements = document.querySelectorAll('.fade-scroll');
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('fade-in');
      }
    });
  },
  { threshold: 0.25 }
);

fadeElements.forEach((element) => observer.observe(element));

const buttons = document.querySelectorAll('.button');
buttons.forEach((button) => {
  button.addEventListener('mouseenter', () => {
    button.style.transform = 'translateY(-3px) scale(1.02)';
  });
  button.addEventListener('mouseleave', () => {
    button.style.transform = 'translateY(0) scale(1)';
  });
});

const counters = [
  { label: 'Users', value: 7 },
  { label: 'Predictions', value: 30 },
  { label: 'Accuracy', value: 98 }
];

const counterContainer = document.createElement('div');
counterContainer.className = 'counter-block';
if (document.querySelector('.hero-copy')) {
  document.querySelector('.hero-copy').appendChild(counterContainer);
}

counters.forEach((item) => {
  const counterItem = document.createElement('div');
  counterItem.className = 'counter-item';
  counterItem.innerHTML = `<strong>0</strong><span>${item.label}</span>`;
  counterContainer.appendChild(counterItem);

  let current = 0;
  const increment = Math.ceil(item.value / 40);
  const interval = setInterval(() => {
    current += increment;
    if (current >= item.value) {
      current = item.value;
      clearInterval(interval);
    }
    counterItem.querySelector('strong').textContent = current + (item.label === 'Accuracy' ? '%' : '');
  }, 40);
});
