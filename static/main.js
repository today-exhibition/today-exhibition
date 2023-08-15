document.addEventListener("DOMContentLoaded", function() {
    const maxlen = 15;
  
    // 전시 제목 길이 자르기
    const spanTexts = document.querySelectorAll(".card-title");
    spanTexts.forEach(function(spanText) {
      const text = spanText.textContent;
      if (text.length > maxlen) {
        const truncatedText = text.substring(0, maxlen) + "...";
        spanText.textContent = truncatedText;
      }
    })
  
    // 전시 장소 길이 자르기
    const cardTexts = document.querySelectorAll(".gallery-place");
    cardTexts.forEach(function(cardText) {
      const text = cardText.textContent;
      if (text.length > maxlen) {
        const truncatedText = text.substring(0, maxlen) + "...";
        cardText.textContent = truncatedText;
      }
    })
  
  })