function makeExhibitionCard(data) {
  const id = data['id'];
  const title = data['title'];
  const thumbnail_img = data['thumbnail_img'];
  const start_date = data['start_date'];
  const end_date = data['end_date'];
  const gallery = data['name'];

  let card_content = `
  <div class="exhibition-card">
    <div class="heart on" onclick="likeExhibition(this, ${id})"></div>
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