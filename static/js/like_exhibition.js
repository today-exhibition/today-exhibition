// 전시 좋아요
function likeExhibition(e, icon, exhibition_id) {
  e.preventDefault();

  const url = `/exhibition/${exhibition_id}/like`;
  
  $.ajax({
    type: "POST", 
    url: url,
    data: { exhibition_id: exhibition_id },
    success: function (resp) {
      if (resp == "login_required") {
        window.alert("로그인 후 이용 가능한 서비스입니다.")
      } else if (resp == "liked") {
        icon.classList.remove("off");
        icon.classList.add("on");
      } else if (resp == "unliked") {
        icon.classList.remove("on");
        icon.classList.add("off");
      }
    }
  });
}