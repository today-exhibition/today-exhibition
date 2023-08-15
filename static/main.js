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

  // 선택한 조건을 서버로 전송하여 쿼리 실행
  await sendQueryToServer(selectedSubSorts, selectedAreas, selectedSort, keyword);

  // 검색 버튼 클릭 후에 검색어 입력란 초기화
  keywordInput.value = "";
});


});



// 서버로 선택한 조건들을 전송하여 쿼리 실행하는 함수
async function sendQueryToServer(selectedSubSorts, selectedAreas, selectedSort, keyword) {
  const subSortsParam = selectedSubSorts.join(",");
  const areasParam = selectedAreas.join(",");

  // areasParam이 콤마로 구분된 문자열이므로 encodeURIComponent를 적용해야함
  const url = `/search/exhibition?keyword=${encodeURIComponent(keyword)}&sub_sort=${encodeURIComponent(subSortsParam)}&area=${encodeURIComponent(areasParam)}&sort=${selectedSort}`;

  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Network response was not ok. Status: ${response.status}`);
    }
    
    const data = await response.json();
    // 서버에서 받은 데이터를 화면에 표시하거나 처리하는 로직 추가
    console.log(data);
  } catch (error) {
    console.error("Error fetching data:", error);
  }
}













