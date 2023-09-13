function makeGalleryCard(gallery) {
  const id = gallery['id'];
  const name = gallery['name'];
  var thumbnail_img = '/static/img/default/default_artist.png'
  if (gallery['gallery_thumbnail_img']) {
    thumbnail_img = gallery['gallery_thumbnail_img'];
  }
  else if (gallery['exhibition_thumbnail_img']) {
    thumbnail_img = gallery['exhibition_thumbnail_img'];
  }
  var bookmark = 'off';
  if (gallery['followed'] >= 1) {
    bookmark = 'on';
  }

  let card_content = `
  <div class="rounded-card" id="${id}">
    <div class="bookmark ${bookmark}" onclick="followGallery(this, '${id}')"></div>
      <img src="${thumbnail_img}" alt="${name}" class="rounded-card-img" loading="lazy">
    <a href="/gallery/${id}" class="rounded-card-text-container">
    <h3 class="rounded-card-name">
      ${name}
    </h3>
    </a>
  </div>
  `
  $(".gallery-card-list").append(card_content);
}

$(document).ready(function() {
  for (let i = 0; i < data.galleries.length; i++){
    makeGalleryCard(data.galleries[i]);
  }
})