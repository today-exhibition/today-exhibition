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

// 전시 좋아요
function likeExhibition(icon, exhibition_id) {
  const url = `/exhibition/${exhibition_id}/like`;
  
  $.ajax({
    type: "POST", 
    url: url,
    data: { exhibition_id: exhibition_id },
    success: function (resp) {
      if (resp === "login_required") {
        window.location.href = "/user"; 
      } else if (resp == "liked") {
        icon.classList.remove("fa-regular");
        icon.classList.add("fa-solid");
      } else if (resp === "unliked") {
        icon.classList.remove("fa-solid");
        icon.classList.add("fa-regular");
      }
    }
  });
}

// 미술관 팔로우
function followGallery(icon, gallery_id) {
  const url = `/search/gallery/${gallery_id}/following`;

  $.ajax({
    type: "POST", 
    url: url, 
    data: { gallery_id: gallery_id }, 
    success: function (resp) {
      if (resp === "login_required") {
        window.location.href = "/user"; 
      } else if (resp == "followed") {
        icon.classList.remove("fa-regular");
        icon.classList.add("fa-solid");
      } else if (resp === "unfollowed") {
        icon.classList.remove("fa-solid");
        icon.classList.add("fa-regular");
      }
    }
  });
}