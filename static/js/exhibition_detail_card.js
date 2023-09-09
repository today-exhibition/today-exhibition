function makeExhibitionCard(exhibition) {
  const id = exhibition['exhibition_id'];
  const title = exhibition['exhibition_title'];
  const thumbnail_img = exhibition['thumbnail_img'];
  const start_date_str = exhibition['start_date'];
  const end_date_str = exhibition['end_date'];
  const gallery = exhibition['gallery_name'];
  var heart = 'off';
  if (exhibition['liked'] == 1) {
    heart = 'on';
  }

  // 문자열로 저장된 날짜를 Date 객체로 변환
  const start_date = new Date(start_date_str);
  const end_date = new Date(end_date_str);

  let card_content = `
    <div class="exhibition-card">
      <div class="heart ${heart}" onclick="likeExhibition(event, this, '${id}')"></div>
      <div class="exhibition-card-img-container">
        <img src="${thumbnail_img}" alt="${title}" class="exhibition-card-img" loading="lazy">
      </div>
      <a href="/exhibition/${id}" class="exhibition-card-text-container">
        <h3 class="exhibition-title">
          ${title}
        </h3>
        <p class="exhibition-desc">${start_date.toLocaleDateString()} - ${end_date.toLocaleDateString()}</p>
        <p class="exhibition-desc">${gallery}</p>
      </a>
    </div>
  `;

  const today = new Date();

  if (today >= start_date && today <= end_date) {
    $(".ongoing_exhibitions").append(card_content);
  } else if (today < start_date) {
    $(".upcoming_exhibitions").append(card_content);
  } else {
    $(".ended_exhibitions").append(card_content);
  }
}

$(document).ready(function() {
  let hasOngoingExhibitions = false;
  let hasUpcomingExhibitions = false;
  let hasEndedExhibitions = false;

  for (let i = 0; i < data.exhibitions.length; i++) {
    const exhibition = data.exhibitions[i];
    const start_date = new Date(exhibition['start_date']);
    const end_date = new Date(exhibition['end_date']);
    const today = new Date();

    if (today >= start_date && today <= end_date) {
      makeExhibitionCard(exhibition);
      hasOngoingExhibitions = true;
    } else if (today < start_date) {
      makeExhibitionCard(exhibition);
      hasUpcomingExhibitions = true;
    } else {
      makeExhibitionCard(exhibition);
      hasEndedExhibitions = true;
    }
  }

  if (!hasOngoingExhibitions) {
    $(".ongoing_exhibitions").append('<p>진행중 전시회가 없습니다.</p>');
  }

  if (!hasUpcomingExhibitions) {
    $(".upcoming_exhibitions").append('<p>예정중 전시회가 없습니다.</p>');
  }

  if (!hasEndedExhibitions) {
    $(".ended_exhibitions").append('<p>지난 전시회가 없습니다.</p>');
  }
});
