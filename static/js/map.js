import constants from '/static/js/constants.js';
import secrets from '/static/js/secrets.js';

function makeCard(data) {
  const id = data['exhibition_id'];
  const title = data['exhibition_title'];
  const img = data['thumbnail_img'];
  const s_date = data['start_date'];
  const e_date = data['end_date'];
  const gallery = data['gallery_name'];
  var heart = 'fa-regular';
  if (data['liked'] == 1) {
    heart = 'fa-solid';
  }

  let card_content =
  `
  <div class="map card mb-3" style="max-width: 540px;">
    <div class="row g-0">
      <div class="col-4">
        <i class="${heart} fa-heart fa-2x" onclick="likeExhibition(this, ${id})"></i>
        <img src="${img}" class="img-fluid rounded-start" alt="${title}">
      </div>
      <div class="col-8">
        <div class="card-body" onclick="window.location='/exhibition/${id}'">
          <h5 class="card-title">${title}</h5>
          <p class="card-text">${s_date}~${e_date}</p>
          <p class="card-text"><small class="text-body-secondary">${gallery}</small></p>
        </div>
      </div>
    </div>
  </div>
  `
  $("#card-list").append(card_content);
}

$(document).ready(function () {
  let script = document.createElement('script');
  let api_key = secrets.kakao_api_key;
  script.src = "https://dapi.kakao.com/v2/maps/sdk.js?appkey=" + api_key + "&libraries=services,clusterer,drawing&autoload=false";
  document.head.appendChild(script);

  script.onload = () => {
    kakao.maps.load(() => {
      // 기본 위치 : 서울시청으로 설정
      var curLoc = new kakao.maps.LatLng(constants.map.defaultLatitude, constants.map.defaultLongitude);
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

      // 마커
      var markers = [];
      for (var i = 0; i < exhibitionsArray.data.length; i++) {
        var exhibition = exhibitionsArray.data[i];
        console.log(exhibition)

        var marker = new kakao.maps.Marker({
          position: new kakao.maps.LatLng(exhibition.gpsy, exhibition.gpsx),
          clickable: true,
          image: new kakao.maps.MarkerImage(constants.imagePath.markerImagePath, new kakao.maps.Size(32, 32))
        });
        marker.data = exhibition;
        markers.push(marker);

        // 마커 클릭 시 해당 카드 리스트 조회
        kakao.maps.event.addListener(marker, 'click', function(){
          map.setCenter(this.getPosition());
          $('#card-list').text("");
          makeCard(this.data);
        });
      }

      // 마커 클러스터
      var clusterer = new kakao.maps.MarkerClusterer({
        map: map,
        averageCenter: true,
        disableClickZoom: true,
        styles: [{
          width: '32px', height: '32px',
          backgroundImage: `url(${constants.imagePath.clustererImagePath})`,
          backgroundRepeat: 'no-repeat',
          textAlign: 'center',
          lineHeight: '31px',
          color: '#EFF1F3'
        }]
      });    
      // 마커 클러스터에 마커 추가
      clusterer.addMarkers(markers);
      
      // 마커클러스터 클릭 시 해당 카드 리스트만 조회
      kakao.maps.event.addListener(clusterer, 'clusterclick', function(cluster) {
        map.setCenter(cluster.getCenter());
        $('#card-list').text("");
        var clustererMarkers = cluster.getMarkers();
        clustererMarkers.forEach(marker => {
          makeCard(marker.data);
        })
      })

      // 지도에 있는 마커만 카드 리스트 표시
      var bounds = map.getBounds();
      $('#card-list').text("");
      for (let i = 0; i < markers.length; i++) {
        var curMarker = markers[i];
        if (bounds.contain(curMarker.getPosition())) {
          makeCard(curMarker.data);
        }
      }

      // 지도 이동할 때마다 카드 리스트 변경
      kakao.maps.event.addListener(map, 'bounds_changed', function () {
        bounds = map.getBounds();
        $('#card-list').text("");
        for (let i = 0; i < markers.length; i++) {
          var curMarker = markers[i];
          if (bounds.contain(curMarker.getPosition())) {
            makeCard(curMarker.data);
          }
        }
      });
    })
  }
});