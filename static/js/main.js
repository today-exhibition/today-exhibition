// 전시 좋아요
function likeExhibition(e, icon, exhibition_id) {
  e.preventDefault();

  const url = `/exhibition/${exhibition_id}/like`;
  
  $.ajax({
    type: "POST", 
    url: url,
    data: { exhibition_id: exhibition_id },
    success: function (resp) {
      if (resp == "liked") {
        icon.classList.remove("off");
        icon.classList.add("on");
      } else if (resp == "unliked") {
        icon.classList.remove("on");
        icon.classList.add("off");
      }
    }
  });
}

// 작가 팔로우
function followArtist(icon, artist_id) {
  const url = `/artist/${artist_id}/following`;

  $.ajax({
    type: "POST", 
    url: url, 
    data: { artist_id: artist_id }, 
    success: function (resp) {
      if (resp == "followed") {
        icon.classList.remove("fa-regular");
        icon.classList.add("fa-solid");
      } else if (resp == "unfollowed") {
        icon.classList.remove("fa-solid");
        icon.classList.add("fa-regular");
      }
    }
  });
}

// 미술관 팔로우
function followGallery(icon, gallery_id) {
  const url = `/gallery/${gallery_id}/following`;

  $.ajax({
    type: "POST", 
    url: url, 
    data: { gallery_id: gallery_id }, 
    success: function (resp) {
      if (resp == "followed") {
        icon.classList.remove("fa-regular");
        icon.classList.add("fa-solid");
      } else if (resp == "unfollowed") {
        icon.classList.remove("fa-solid");
        icon.classList.add("fa-regular");
      }
    }
  });
}
