// 미술관 팔로우
function followGallery(icon, gallery_id) {
  const url = `/gallery/${gallery_id}/following`;

  $.ajax({
    type: "POST", 
    url: url, 
    data: { gallery_id: gallery_id }, 
    success: function (resp) {
      if (resp == "login_required") {
        window.alert("로그인 후 이용 가능한 서비스입니다.")
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
