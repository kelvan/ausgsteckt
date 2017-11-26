var map;

function onEachFeature(feature, layer) {
    "use strict";
    layer.bindPopup("Loading ...");
    layer.getPopup();
    layer.bindTooltip(feature.properties.name, {closeButton: false});
    layer.on("click", function (e) {
        var popup = e.target.getPopup();
        $.ajax($("#buschenschank_maps").data("details-url").replace("000", feature.properties.pk), {success: function(data) {
            popup.setContent(data);
            popup.update();
        }});
    });
}

function main_map_init (mapid, options) {
    map = L.map(mapid, {
        zoom: 8, center: L.latLng(47.6, 14.0), closePopupOnClick: false
    });
    var osmUrl="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
    var osmAttrib="Map data © <a href=\"https://openstreetmap.org\">OpenStreetMap</a> contributors";
    var osm = new L.TileLayer(
        osmUrl, {
            minZoom: 5, maxZoom: 18, attribution: osmAttrib
        }
    );
    map.addLayer(osm);
    var basemap = L.tileLayer.provider("BasemapAT", {attribution: "Datenquelle: <a href=\"https://www.basemap.at\">basemap.at</a>"});
    var hikebike = L.tileLayer.provider("HikeBike");
    var mtbmap = L.tileLayer.provider("MtbMap");
    var opentopomap = L.tileLayer.provider("OpenTopoMap");

    var baseMaps = {
        "OpenStreetMap": osm,
        "Basemap AT": basemap,
        "HikeBike": hikebike,
        "MtbMap": mtbmap,
        "OpenTopoMap": opentopomap
    };
    var layers = L.control.layers(baseMaps).addTo(map);
    L.Icon.Default.imagePath = "/static/images/";
    map.addControl(new L.Control.Permalink({text: 'Permalink', layers: layers}));
    L.control.scale().addTo(map);

    window.map = map;
    var dataurl = $("#buschenschank_maps").data("geojson-url");
    // Download GeoJSON via Ajax
    $.getJSON(dataurl, function (data) {
        var markers = L.markerClusterGroup();
        // Add GeoJSON layer
        var geoJsonLayer = L.geoJson(data, {onEachFeature: onEachFeature});
        markers.addLayer(geoJsonLayer);
        map.addLayer(markers);
    });
    if(!window.location.hash) {
        map.locate({setView : true, maxZoom: 11});
    }
}

function small_map_init (mapid, options) {
    var zoom = $("#buschenschank_maps").data("zoom");
    var lat = $("#buschenschank_maps").data("lat");
    var lon = $("#buschenschank_maps").data("lon");
    map = L.map(mapid, {
        zoom: zoom, center: L.latLng(lat, lon), closePopupOnClick: false
    });
    var osmUrl="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
    var osmAttrib="Map data © <a href=\"https://openstreetmap.org\">OpenStreetMap</a> contributors";
    var osm = new L.TileLayer(
        osmUrl, {
            minZoom: 5, maxZoom: 18, attribution: osmAttrib
        }
    );
    map.addLayer(osm);
    L.Icon.Default.imagePath = "/static/images/";
    L.control.scale().addTo(map);

    window.map = map;
    var dataurl = $("#buschenschank_maps").data("geojson-url");
    // Download GeoJSON via Ajax
    $.getJSON(dataurl, function (data) {
        var markers = L.markerClusterGroup();
        // Add GeoJSON layer
        var geoJsonLayer = L.geoJson(data, {onEachFeature: onEachFeature});
        markers.addLayer(geoJsonLayer);
        map.addLayer(markers);
    });
}