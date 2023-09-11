// 작가 팔로우
function followArtist(icon, artist_id) {
  const url = `/artist/${artist_id}/following`;

  $.ajax({
    type: "POST", 
    url: url, 
    data: { artist_id: artist_id }, 
    success: function (resp) {
      if (resp == "login_required") {
        $('#alertmodal').modal('show');
      } else if (resp == "followed") {
        icon.classList.remove("off");
        icon.classList.add("on");
      } else if (resp == "unfollowed") {
        icon.classList.remove("on");
        icon.classList.add("off");
      }
    }
  });
}