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

//============================================================================================

document.addEventListener("DOMContentLoaded", function() {
  const searchButton = document.getElementById("filter-button");
  const typeSortButtons = document.querySelectorAll(".btn-type");
  const areaSortButtons = document.querySelectorAll(".btn-area");
  const topSortButtons = document.querySelectorAll(".btn-top");

  // type, area 정렬 버튼 여러개 선택 가능
  typeSortButtons.forEach(button => {
    button.addEventListener('click', () => {
      button.classList.toggle('selected'); // 'selected'가 있으면 classList에서 없애고, 없으면 만들어줌.
      button.classList.toggle('active');
    });
  });

  areaSortButtons.forEach(button => {
    button.addEventListener('click', ()=> {
      button.classList.toggle('selected');
      button.classList.toggle('active');
    });
  });

  // top 정렬 버튼 하나 선택 가능
  topSortButtons.forEach(button => {
    button.addEventListener('click', () => {
      topSortButtons.forEach(btn => {
        btn.classList.remove('selected');
        btn.classList.remove('active');
      });
      button.classList.add('selected');
      button.classList.add('active');
    });
  });

  // 검색 버튼 클릭 시 처리
  searchButton.addEventListener("click", async (event) => {
    event.preventDefault(); // 폼의 기본 제출 동작 막기

    const keywordInput = document.getElementById("keyword-input");
    const keyword = keywordInput.value;

    const selectedSubSorts = Array.from(typeSortButtons)
                              .filter(button => button.classList.contains("selected"))
                              .map(button => button.getAttribute("sub-sort"));

    const selectedAreas = Array.from(areaSortButtons)
                            .filter(button => button.classList.contains("selected"))
                            .map(button => button.getAttribute("sub-sort"));

    const selectedSortButtons = Array.from(topSortButtons)
                                .filter(button => button.classList.contains("selected"));
    const selectedSort = selectedSortButtons.length > 0 ? selectedSortButtons[0].getAttribute("sub-sort") : null;

    const subSortsParam = selectedSubSorts.join(",");
    const areasParam = selectedAreas.join(",");
    const sortedSort = selectedSort || ""; // selectedSort가 null일 경우 빈 문자열로 초기화
  
    // areasParam이 콤마로 구분된 문자열이므로 encodeURIComponent 적용
    const url = `/search/exhibition?keyword=${encodeURIComponent(keyword)}&sub_sort=${encodeURIComponent(subSortsParam)}&area=${encodeURIComponent(areasParam)}&sort=${encodeURIComponent(sortedSort)}`;
  
    window.location.href = url;
  });
});

//============================================================================================
function HeartIcon(icon, exhibition_id) {
  const url = `/search/exhibition/${exhibition_id}/like`;

  $.ajax({
    type: "POST", 
    url: url, 
    data: { exhibition_id: exhibition_id }, 
    success: function (resp) {
      if (resp === "login_required") {
        window.location.href = "/user"; 
      } else if (resp == "exist") {
        icon.classList.remove("fa-regular");
        icon.classList.add("fa-solid");
      } else if (resp === "success") {
        icon.classList.remove("fa-solid");
        icon.classList.add("fa-regular");
      }
    }
  });
}



