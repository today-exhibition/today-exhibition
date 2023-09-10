function makeGalleryCard(gallery) {
  const id = gallery['id'];
  const name = gallery['name'];
  var thumbnail_img = '/static/img/icon/gallery_default.svg'
  if (gallery['gallery_thumbnail_img']) {
    thumbnail_img = gallery['gallery_thumbnail_img'];
  }
  // 전시 이미지 사용 시 gallery.py의 get_gallery_data 함수 수정 필요
  // else if (gallery['exhibition_thumbnail_img']) {
  //   thumbnail_img = gallery['exhibition_thumbnail_img'];
  // }

  console.log(gallery)
  let card_content = `
  <div class="rounded-card" id="${id}">
      <img src="${thumbnail_img}" alt="${name}" class="rounded-card-img" loading="lazy">
  </div>
  `
  $(".gallery-card-list").append(card_content);
}

$(document).ready(function() {
    makeGalleryCard(data.gallery[0]);
})