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