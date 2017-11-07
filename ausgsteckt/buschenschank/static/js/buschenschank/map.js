var map;

function onEachFeature(feature, layer) {
  layer.bindPopup('Loading ...');
  layer.getPopup();
  layer.bindTooltip(feature.properties.name, {closeButton: false});
  layer.on('click', function (e) {
    var popup = e.target.getPopup();
    $.ajax($('#buschenschank_maps').data('details-url').replace('000', feature.properties.pk), {success: function(data) {
        popup.setContent(data);
        popup.update();
      }
    })
  });
}

function main_map_init (mapid, options) {
  map = L.map(mapid, {
    zoom: 8, center: L.latLng(47.6, 14.0), closePopupOnClick: false
  });
  var osmUrl='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
	var osmAttrib='Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors';
	var osm = new L.TileLayer(
	  osmUrl, {
	    minZoom: 5, maxZoom: 18, attribution: osmAttrib
	  }
	);
	map.addLayer(osm);
  L.Icon.Default.imagePath = '/static/images/';
  L.control.scale().addTo(map);

  window.map = map;
  var dataurl = $('#buschenschank_maps').data('geojson-url');
  // Download GeoJSON via Ajax
  $.getJSON(dataurl, function (data) {
    var markers = L.markerClusterGroup();
    // Add GeoJSON layer
    var geoJsonLayer = L.geoJson(data, {onEachFeature: onEachFeature});
    markers.addLayer(geoJsonLayer);
  	map.addLayer(markers);
  });
  map.locate({setView : true, maxZoom: 11});
}
