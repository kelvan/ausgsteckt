var map;

function onEachFeature(feature, layer) {
  layer.on('click', function (e) {
    $.ajax($('#buschenschank_maps').data('details-url').replace('000', feature.id), {success: function(data) {
        if ($('#buschenschank_details').is(":visible")) {
          $('#buschenschank_details_content').html(data);
          $('#buschenschank_details').show();
        } else {
          $('#buschenschank_maps').removeClass('col-md-12');
          $('#buschenschank_maps').addClass('col-md-8');
          $('#buschenschank_details').removeClass('col-md-0');
          $('#buschenschank_details').addClass('col-md-4');
          $('#buschenschank_maps').one("webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend",
          function(e){
            $('#buschenschank_details_content').html(data);
            $('#buschenschank_details').show();
            $('#buschenschank_maps').off();
          });
        }
      }
    })
  });
}

function main_map_init (mapid, options) {
  map = L.map(mapid, {zoom: 8, center: L.latLng(47.6, 14.0)});
  var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
	var osmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
	var osm = new L.TileLayer(
	  osmUrl, {
	    minZoom: 5, maxZoom: 18, attribution: osmAttrib
	  }
	);
	map.addLayer(osm);
  L.Icon.Default.imagePath = '/static/images/';

  window.map = map;
  var dataurl = $('#buschenschank_maps').data('geojson-url');
  // Download GeoJSON via Ajax
  $.getJSON(dataurl, function (data) {
    // Add GeoJSON layer
    L.geoJson(data, {onEachFeature: onEachFeature}).addTo(map);
  });
  map.locate({setView : true, maxZoom: 11});
}

function close_details() {
  $('#buschenschank_details_content').html('');
  $('#buschenschank_details').hide();
  $('#buschenschank_maps').removeClass('col-md-8');
  $('#buschenschank_maps').addClass('col-md-12');
}
