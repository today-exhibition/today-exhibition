function makeArtistCard(artist) {
  const id = artist['id'];
  const name = artist['name'];
  var thumbnail_img = '/img/default/default_artist.png'
  if (artist['artist_thumbnail_img']) {
    var thumbnail_img = artist['artist_thumbnail_img'];
  }
  else if (artist['exhibition_thumbnail_img']) {
    var thumbnail_img = artist['exhibition_thumbnail_img'];
  }
  var bookmark = 'off';
  if (artist['followed'] == 1) {
    bookmark = 'on';
  }

  let card_content = `
  <div class="rounded-card" id="${id}">
    <div class="bookmark ${bookmark}" onclick="followArtist(this, '${id}')"></div>
      <img src="${thumbnail_img}" alt="${name}" class="rounded-card-img" loading="lazy">
    <a href="/artist/${id}" class="rounded-card-text-container">
    <h3 class="rounded-card-name">
      ${name}
    </h3>
    </a>
  </div>
  `
  $(".artist-card-list").append(card_content);
}

$(document).ready(function() {
  for (let i = 0; i < data.artists.length; i++){
    makeArtistCard(data.artists[i]);
  }
})