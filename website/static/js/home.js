document.addEventListener('DOMContentLoaded', () => {
  const slider = document.querySelector('.slider');
  const prevButton = document.querySelector('.prev-button');
  const nextButton = document.querySelector('.next-button');
  const cardWidth = document.querySelector('.card').offsetWidth + 10;
  const cardsToShow = 3; // Number of cards to show at once
  let currentIndex = 0;

  prevButton.addEventListener('click', () => {
    if (currentIndex > 0) {
      currentIndex -= cardsToShow;
    }
    updateSliderPosition();
  });

  nextButton.addEventListener('click', () => {
    if (currentIndex < slider.children.length - cardsToShow) {
      currentIndex += cardsToShow;
    }
    updateSliderPosition();
  });

  function updateSliderPosition() {
    const slideAmount = currentIndex * (cardWidth); // Adjusted for card margin
    slider.style.transform = `translateX(-${slideAmount}px)`;
  }
});