function makeCard(title, img, s_date, e_date, gallery) {
  let card_content =
  `
  <div class="card">
    <div class="card-img">
      <img src="${img}" alt="">
    </div>
    <div class="card-content">
      <h3>${title}</h3>
      <p>${s_date}~${e_date}</p>
      <p>${gallery}</p>
    </div>
  </div>
  `
  $("#card-list").append(card_content);
}

$(document).ready(function () {
  kakao.maps.load(() => {
    // 기본 위치 : 서울시청으로 설정
    var curLoc = new kakao.maps.LatLng(37.5667, 126.9784);
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position) {  
        curLoc = new kakao.maps.LatLng(position.coords.latitude, position.coords.longitude);
      });
    }

    // 지도
    var map = new kakao.maps.Map(document.getElementById('map'), {
      center: curLoc,
      level: 10
    });

    // 마커 클러스터
    var clusterer = new kakao.maps.MarkerClusterer({
      map: map,
      averageCenter: true, 
      minLevel: 10,
      disableClickZoom: true,
      styles: [{
        width: '32px', height: '32px',
        background: 'url(https://github.com/today-exhibition/today-exhibition/assets/63828057/d1c02f39-df31-4b74-a0a0-f781893b6baf) no-repeat',
        textAlign: 'center',
        lineHeight: '31px',
        color: '#EFF1F3'
      }]
    });
    
    // 마커
    var markers = [];
    for (var i = 0; i < exhibitionsArray.length; i++) {
      var position = exhibitionsArray[i];
      var marker = new kakao.maps.Marker({
        position: new kakao.maps.LatLng(position.gpsy, position.gpsx),
        image: new kakao.maps.MarkerImage('https://github.com/today-exhibition/today-exhibition/assets/63828057/b86a1ed4-40b0-4c8b-ba66-fe5529841546', new kakao.maps.Size(32, 32))
      });
      markers.push(marker);
    }

    // 지도에 있는 마커만 카드 리스트 표시
    var bounds = map.getBounds();
    $('#card-list').text(bounds.toString());

    clusterer.addMarkers(markers);
    for (let i = 0; i < exhibitionsArray.length; i++) {
      makeCard(exhibitionsArray[i]['exhibition_title'], exhibitionsArray[i]['thumbnail_img'], exhibitionsArray[i]['start_date'], exhibitionsArray[i]['end_date'], exhibitionsArray[i]['gallery_name']);
    }

    // 지도 이동할 때마다 카드 리스트 변경
    kakao.maps.event.addListener(map, 'bounds_changed', function () {
      bounds = map.getBounds();
      $('#card-list').text(bounds.toString());
      clusterer.addMarkers(markers);
      for (let i = 0; i < exhibitionsArray.length; i++) {
        l = new kakao.maps.LatLng(exhibitionsArray[i].gpsy, exhibitionsArray[i].gpsx);
        if (bounds.contain(l)) {
          makeCard(exhibitionsArray[i]['exhibition_title'], exhibitionsArray[i]['thumbnail_img'], exhibitionsArray[i]['start_date'], exhibitionsArray[i]['end_date'], exhibitionsArray[i]['gallery_name']);
        }
      }
    });
  })
});