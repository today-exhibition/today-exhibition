import constants from '/static/js/constants.js';
import secrets from '/static/js/secrets.js';

function makeCard(data) {
  const maxLenght = 25;
  const id = data['exhibition_id'];
  var title = data['exhibition_title'];
  if (title.length > maxLenght) {
    title = title.substring(0, maxLenght) + "...";
  }
  var img = '/static/img/default/default_exhibition.png'
  if (data['low_thumbnail_img']) {
    img = data['low_thumbnail_img'];
  }
  else {
    img = data['thumbnail_img'];
  }
  const s_date = data['start_date'];
  const e_date = data['end_date'];
  const gallery = data['gallery_name'];
  var heart = 'off';
  if (data['liked'] == 1) {
    heart = 'on';
  }

  let card_content =
  `
    <div class="map-exhibition-card">
      <div class="map-exhibition-card-img-container">
        <img src="${img}" class="map-exhibition-card-img" loading="lazy" >
      </div>
      <a href="/exhibition/${id}" class="map-exhibition-card-text-container">
        <div class="heart ${heart}" onclick="likeExhibition(event, this, '${id}')"></div>
        <h3 class="map-exhibition-title">
          ${title}
        </h3>
        <p class="map-exhibition-desc">${s_date} - ${e_date}</p>
        <p class="map-exhibition-desc">${gallery}</p>
      </a>
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
      const maxCardList = 20;
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
        $('.card-list-container').scrollTop(0);
      })

      // 지도에 있는 마커만 카드 리스트 표시
      var bounds = map.getBounds();
      var count = 0;
      $('#card-list').text("");
      for (let i = 0; i < markers.length; i++) {
        var curMarker = markers[i];
        if (bounds.contain(curMarker.getPosition())) {
          makeCard(curMarker.data);
          count++;
          if (count >= maxCardList) {
            break;
          }
        }
      }

      // 지도 이동할 때마다 카드 리스트 변경
      kakao.maps.event.addListener(map, 'bounds_changed', function () {
        bounds = map.getBounds();
        count = 0;
        $('#card-list').text("");
        for (let i = 0; i < markers.length; i++) {
          var curMarker = markers[i];
          if (bounds.contain(curMarker.getPosition())) {
            makeCard(curMarker.data);
            count++;
            if (count >= maxCardList) {
              break;
            }
          }
        }
        $('.card-list-container').scrollTop(0);
      });
    })
  }
});
