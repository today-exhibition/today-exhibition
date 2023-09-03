function makeExhibitionCard(exhibition) {
  const id = exhibition['exhibition_id'];
  const title = exhibition['exhibition_title'];
  const thumbnail_img = exhibition['thumbnail_img'];
  const start_date = exhibition['start_date'];
  const end_date = exhibition['end_date'];
  const gallery = exhibition['gallery_name'];
  var heart = 'off';
  if (exhibition['liked'] == 1) {
    heart = 'on';
  }

  let card_content = `
  <div class="exhibition-card">
    <div class="heart ${heart}" onclick="likeExhibition(this, '${id}')"></div>
    <div class="exhibition-card-img-container">
      <img src="${thumbnail_img}" alt="${title}" class="exhibition-card-img">
    </div>
    <a href="/exhibition/${id}" class="exhibition-card-text-container">
      <h3 class="exhibition-title">
        ${title}
      </h3>
      <p class="exhibition-desc">${start_date} - ${end_date}</p>
      <p class="exhibition-desc">${gallery}</p>
    </a>
  </div>
  `
  $(".exhibition-card-list").append(card_content);
}

$(document).ready(function() {
  for (let i = 0; i < data.exhibitions.length; i++){
    makeExhibitionCard(data.exhibitions[i]);
  }
})