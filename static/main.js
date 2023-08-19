function changeLikeState(icon, exhibition_id) {
  const url = `/search/exhibition/${exhibition_id}/like`;

  $.ajax({
    type: "POST", 
    url: url, 
    data: { exhibition_id: exhibition_id }, 
    success: function (resp) {
      if (resp === "login_required") {
        window.location.href = "/user"; 
      } else if (resp == "liked") {
        icon.classList.remove("fa-regular");
        icon.classList.add("fa-solid");
      } else if (resp === "unliked") {
        icon.classList.remove("fa-solid");
        icon.classList.add("fa-regular");
      }
    }
  });
}

function GalleryFollow(icon, gallery_id) {
  const url = `/search/gallery/${gallery_id}/following`;

  $.ajax({
    type: "POST", 
    url: url, 
    data: { gallery_id: gallery_id }, 
    success: function (resp) {
      if (resp === "login_required") {
        window.location.href = "/user"; 
      } else if (resp == "followed") {
        icon.classList.remove("fa-regular");
        icon.classList.add("fa-solid");
      } else if (resp === "unfollowed") {
        icon.classList.remove("fa-solid");
        icon.classList.add("fa-regular");
      }
    }
  });
}


