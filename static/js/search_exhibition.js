document.addEventListener("DOMContentLoaded", function() {
  const searchButton = document.getElementById("filter-button");
  const typeSortButtons = document.querySelectorAll(".btn-type"); // 전시중, 종료, 예정
  const areaSortButtons = document.querySelectorAll(".btn-area"); 
  const topSortButtons = document.querySelectorAll(".btn-top"); // 인기순, 지금 주목 받는 전시..

  // type, area 정렬 버튼 여러개 선택 가능
  typeSortButtons.forEach(button => {
    button.addEventListener('click', () => {
      button.classList.toggle('selected'); 
    });
  });

  areaSortButtons.forEach(button => {
    button.addEventListener('click', ()=> {
      button.classList.toggle('selected');
    });
  });

  // top 정렬 버튼 하나 선택 가능
  topSortButtons.forEach(button => {
    button.addEventListener('click', () => {
      const buttonSelected = button.classList.contains('selected');
  
      topSortButtons.forEach(btn => {
        btn.classList.remove('selected');
      });
  
      if (!buttonSelected) {
        button.classList.add('selected');
      }
    });
  });

  // 검색 버튼 클릭 시 처리
  searchButton.addEventListener("click", event => {
    event.preventDefault();

    const keywordInput = document.getElementById("keyword-input");
    const keyword = keywordInput.value;

    const selectedSubSorts = Array.from(typeSortButtons)
                              .filter(button => button.classList.contains("selected"))
                              .map(button => button.getAttribute("sub-sort"));

    const selectedAreas = Array.from(areaSortButtons)
                            .filter(button => button.classList.contains("selected"))
                            .map(button => button.getAttribute("sub-sort"));

    const selectedSort = Array.from(topSortButtons)
                                .filter(button => button.classList.contains("selected"))
                                .map(button => button.getAttribute("sub-sort"));

    const subSortsParam = selectedSubSorts.join(",");
    const areasParam = selectedAreas.join(",");
  
    const url = `/search/exhibition?keyword=${keyword}&sub_sort=${subSortsParam}&area=${areasParam}&sort=${selectedSort}`;
  
    window.location.href = url;
  });
});