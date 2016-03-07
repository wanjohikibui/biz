var map, featureList, bizSearch = [], parcelSearch = [], locationSearch = [];

$(window).resize(function() {
  sizeLayerControl();
});

$(document).on("click", ".feature-row", function(e) {
  $(document).off("mouseout", ".feature-row", clearHighlight);
  sidebarClick(parseInt($(this).attr("id"), 10));
});

if ( !("ontouchstart" in window) ) {
  $(document).on("mouseover", ".feature-row", function(e) {
    highlight.clearLayers().addLayer(L.circleMarker([$(this).attr("lat"), $(this).attr("lng")], highlightStyle));
  });
}

$(document).on("mouseout", ".feature-row", clearHighlight);

$("#full-extent-btn").click(function() {
  map.fitBounds(parcels.getBounds());
  $(".navbar-collapse.in").collapse("hide");
  return false;
});

$("#list-btn").click(function() {
  $('#sidebar').toggle();
  map.invalidateSize();
  return false;
});

$("#nav-btn").click(function() {
  $(".navbar-collapse").collapse("toggle");
  return false;
});

$("#sidebar-toggle-btn").click(function() {
  $("#sidebar").toggle();
  map.invalidateSize();
  return false;
});

$("#sidebar-hide-btn").click(function() {
  $('#sidebar').hide();
  map.invalidateSize();
});

function sizeLayerControl() {
  $(".leaflet-control-layers").css("max-height", $("#map").height() - 50);
}

function clearHighlight() {
  highlight.clearLayers();
}

function sidebarClick(id) {
  var layer = markerClusters.getLayer(id);
  map.setView([layer.getLatLng().lat, layer.getLatLng().lng], 17);
  layer.fire("click");
  /* Hide sidebar and go to the map on small screens */
  if (document.body.clientWidth <= 767) {
    $("#sidebar").hide();
    map.invalidateSize();
  }
}
//var bizIcon = STATIC_URL + '/permit/img/cybers.png';
var bizIcon = STATIC_URL + '/permit/img/magicshow.png';

function syncSidebar() {
  /* Empty sidebar features */
  $("#feature-list tbody").empty();
  /* Loop through theaters layer and add only features which are in the map bounds */
  business.eachLayer(function (layer) {
    if (map.hasLayer(bizLayer)) {
      if (map.getBounds().contains(layer.getLatLng())) {
        $("#feature-list tbody").append('<tr class="feature-row" id="' + L.stamp(layer) + '" lat="' + layer.getLatLng().lat + '" lng="' + layer.getLatLng().lng + '"><td style="vertical-align: middle;"><img width="16" height="18" src= '+bizIcon+'></td><td class="feature-name">' + layer.feature.properties.business_name + '</td><td style="vertical-align: middle;"><i class="fa fa-chevron-right pull-right"></i></td></tr>');
      }
    }
  });
  /* Loop through museums layer and add only features which are in the map bounds */
  /* Update list.js featureList */
  featureList = new List("features", {
    valueNames: ["feature-name"]
  });
  featureList.sort("feature-name", {
    order: "asc"
  });
}

/* Basemap Layers */
var mapquestOSM = L.tileLayer("https://{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png", {
  maxZoom: 19,
  subdomains: ["otile1-s", "otile2-s", "otile3-s", "otile4-s"],
  attribution: 'Tiles courtesy of <a href="http://www.mapquest.com/" target="_blank">MapQuest</a> <img src="https://developer.mapquest.com/content/osm/mq_logo.png">. Map data (c) <a href="http://www.openstreetmap.org/" target="_blank">OpenStreetMap</a> contributors, CC-BY-SA.'
});
var mapquestOAM = L.tileLayer("https://{s}.mqcdn.com/tiles/1.0.0/sat/{z}/{x}/{y}.jpg", {
  maxZoom: 18,
  subdomains: ["otile1-s", "otile2-s", "otile3-s", "otile4-s"],
  attribution: 'Tiles courtesy of <a href="http://www.mapquest.com/" target="_blank">MapQuest</a>. Portions Courtesy NASA/JPL-Caltech and U.S. Depart. of Agriculture, Farm Service Agency'
});
var mapquestHYB = L.layerGroup([L.tileLayer("https://{s}.mqcdn.com/tiles/1.0.0/sat/{z}/{x}/{y}.jpg", {
  maxZoom: 18,
  subdomains: ["otile1-s", "otile2-s", "otile3-s", "otile4-s"]
}), L.tileLayer("https://{s}.mqcdn.com/tiles/1.0.0/hyb/{z}/{x}/{y}.png", {
  maxZoom: 19,
  subdomains: ["otile1-s", "otile2-s", "otile3-s", "otile4-s"],
  attribution: 'Labels courtesy of <a href="http://www.mapquest.com/" target="_blank">MapQuest</a> <img src="https://developer.mapquest.com/content/osm/mq_logo.png">. Map data (c) <a href="http://www.openstreetmap.org/" target="_blank">OpenStreetMap</a> contributors, CC-BY-SA. Portions Courtesy NASA/JPL-Caltech and U.S. Depart. of Agriculture, Farm Service Agency'
})]);

/* Overlay Layers */
var highlight = L.geoJson(null);
var highlightStyle = {
  stroke: false,
  fillColor: "#00FFFF",
  fillOpacity: 0.7,
  radius: 10
};
function getStyle(feature) {
  return {
    color: 'brown',
    weight: 1.6,
  };
}
var county= L.geoJson();
var countyurl = '/county_data/'
$.getJSON(countyurl, function (data) {
    county.addData(data).setStyle(getStyle);
    //map.fitBounds(e.target.getBounds());
});

var locations = L.geoJson(null,{
  style: function getstyle(feature) {
    switch (feature.properties.division_b){
      case 'KANDUYI':
        return {
          weight: 0,
          color: 'orange',
          fillOpacity: 0.7
        };
        break;
      case 'WEBUYE':
        return {
          weight: 0,
          color: 'purple',
          fillOpacity: 0.7
        };
        break;
      case 'SIRISIA':
        return {
          weight: 0,
          color: 'brown',
          fillOpacity: 0.7
        };
        break;
      case 'TONGARENI':
        return {
          weight: 0,
          color: 'green',
          fillOpacity: 0.7
        };
        break;
      case 'KIMILILI':
        return {
          weight: 0,
          color: 'grey',
          fillOpacity: 0.7
        };
        break;

    }
  },
  onEachFeature: function (feature, layer) {
      layer.on('click', function (e) {
      var popup = "<strong>" + "Id : " + e.target.feature.properties.id + "<br>" + "Division: " + e.target.feature.properties.division_b + "<br>" + " Location : " + e.target.feature.properties.location_b +  "<br>" + "SubLocation: " + e.target.feature.properties.subloc_b + "</strong>";
      layer.bindPopup(popup).openPopup(e.latlng);
      //map.fitBounds(e.target.getBounds());
    });
    locationSearch.push({
      name: layer.feature.properties.location_b,
      source: "Locations",
      id: L.stamp(layer),
      bounds: layer.getBounds()
    });
  }
});
var dataurl = '/location_data/'
$.getJSON(dataurl, function (data) {
    locations.addData(data);
    //map.addLayer(locations);
});

/* Single marker cluster layer to hold all clusters */
var markerClusters = new L.MarkerClusterGroup({
  spiderfyOnMaxZoom: true,
  showCoverageOnHover: false,
  zoomToBoundsOnClick: true,
  disableClusteringAtZoom: 16
});

var bizurl = '/business_data/'

/* Empty layer placeholder to add to layer control for listening when to add/remove business to markerClusters layer */
var bizLayer = L.geoJson(null);
var business = L.geoJson(null, {
  pointToLayer: function (feature, latlng) {
     switch (feature.properties.business_compliance){
        case true:
          return L.marker(latlng, {
            icon: L.icon({
              iconUrl: STATIC_URL + '/permit/img/butcheries.png',
              iconSize: [24, 28],
              iconAnchor: [12, 28],
              popupAnchor: [0, -25]
            }),
            title: feature.properties.business_name,
            riseOnHover: true
          });
          break;
        case false:
          return L.marker(latlng, {
            icon: L.icon({
              iconUrl: STATIC_URL + '/permit/img/magicshow.png',
              iconSize: [24, 28],
              iconAnchor: [12, 28],
              popupAnchor: [0, -25]
            }),
            title: feature.properties.business_name,
            riseOnHover: true
          });
          break;    

      }
  },
  onEachFeature: function (feature, layer) {
    if (feature.properties) {
      layer.on('click', function (e) {
      var popup = "<strong>" + "Name : " + e.target.feature.properties.business_name + "<br>" + "Type: " + e.target.feature.properties.business_type + "<br>" + " Class : " + e.target.feature.properties.business_class +  "<br>" + "Complied: " + e.target.feature.properties.business_compliance + "</strong>";
      layer.bindPopup(popup).openPopup(e.latlng);
      highlight.clearLayers().addLayer(L.circleMarker([feature.geometry.coordinates[1], feature.geometry.coordinates[0]], highlightStyle));

      //map.fitBounds(e.target.getBounds());
    }); 
      $("#feature-list tbody").append('<tr class="feature-row" id="' + L.stamp(layer) + '" lat="' + layer.getLatLng().lat + '" lng="' + layer.getLatLng().lng + '"><td style="vertical-align: middle;"><img width="16" height="18" src='+ bizIcon+'>' + layer.feature.properties.business_name + '</td><td style="vertical-align: middle;"><i class="fa fa-chevron-right pull-right"></i></td></tr>'); 
      bizSearch.push({
        name: layer.feature.properties.business_name,
        address: layer.feature.properties.business_type,
        source: "Business",
        id: L.stamp(layer),
        lat: layer.feature.geometry.coordinates[1],
        lng: layer.feature.geometry.coordinates[0]
      });
    }
  }
});
$.getJSON(bizurl, function (data) {
  business.addData(data);
  map.addLayer(bizLayer);
});
function parcelStyle(feature) {
  return {
    weight: 2,
    //opacity: 1,
    color: 'brown',
    dashArray: '3',
    fillOpacity: 0.3,
    fillColor: 'black'
  };
}
/* Empty layer placeholder to add to layer control for listening when to add/remove museums to markerClusters layer */
var parcelurl = '/parcel_data/'
var parcelLayer = L.geoJson(null);
var parcels = L.geoJson(null, {
  onEachFeature: function (feature, layer) {
    layer.on('click', function (e) {
      var popup = "<strong>" + "Id : " + e.target.feature.properties.id + "<br>" + "Parcel No: " + e.target.feature.properties.parcel_no + "<br>" + " Block ID : " + e.target.feature.properties.blockid +  "<br>" + "Section Code: " + e.target.feature.properties.sectcode + "</strong>";
      layer.bindPopup(popup).openPopup(e.latlng);
      //map.fitBounds(e.target.getBounds());
    });
      parcelSearch.push({
        name: layer.feature.properties.parcel_no,
        address: layer.feature.properties.blockid,
        source: "Parcels",
        id: L.stamp(layer),
        bounds: layer.getBounds()
      });
    }
});
$.getJSON(parcelurl, function (data) {
  parcels.addData(data).setStyle(parcelStyle);
  map.addLayer(parcelLayer);
});
parcelLayer.addLayer(parcels);
map = L.map("map", {
  zoom: 10,
  center: [0.5667, 34.5667],
  layers: [mapquestOSM,parcelLayer, markerClusters, highlight],
  zoomControl: false,
  attributionControl: false
});
//map.addLayer(county);
/* Layer control listeners that allow for a single markerClusters layer */
map.on("overlayadd", function(e) {
  if (e.layer === bizLayer) {
    markerClusters.addLayer(business);
    syncSidebar();
  }
});

map.on("overlayremove", function(e) {
  if (e.layer === bizLayer) {
    markerClusters.removeLayer(business);
    syncSidebar();
  }
});

/* Filter sidebar feature list to only show features in current map bounds */
map.on("moveend", function (e) {
  syncSidebar();
});

/* Clear feature highlight when map is clicked */
map.on("click", function(e) {
  highlight.clearLayers();
});

/* Attribution control */
function updateAttribution(e) {
  $.each(map._layers, function(index, layer) {
    if (layer.getAttribution) {
      $("#attribution").html((layer.getAttribution()));
    }
  });
}
map.on("layeradd", updateAttribution);
map.on("layerremove", updateAttribution);

var attributionControl = L.control({
  position: "bottomright"
});
attributionControl.onAdd = function (map) {
  var div = L.DomUtil.create("div", "leaflet-control-attribution");
  div.innerHTML = "<span class='hidden-xs'>Developed by <a href='http://wanjohikibui.blogspot.com'>wanjohikibui</a> | </span><a href='#' onclick='$(\"#attributionModal\").modal(\"show\"); return false;'>Attribution</a>";
  return div;
};
map.addControl(attributionControl);

var zoomControl = L.control.zoom({
  position: "topleft"
}).addTo(map);

/* GPS enabled geolocation control set to follow the user's location */
var locateControl = L.control.locate({
  position: "topleft",
  drawCircle: true,
  follow: true,
  setView: true,
  keepCurrentZoomLevel: true,
  markerStyle: {
    weight: 1,
    opacity: 0.8,
    fillOpacity: 0.8
  },
  circleStyle: {
    weight: 1,
    clickable: false
  },
  icon: "fa fa-location-arrow",
  metric: false,
  strings: {
    title: "My location",
    popup: "You are within {distance} {unit} from this point",
    outsideMapBoundsMsg: "You seem located outside the boundaries of the map"
  },
  locateOptions: {
    maxZoom: 18,
    watch: true,
    enableHighAccuracy: true,
    maximumAge: 10000,
    timeout: 10000
  }
}).addTo(map);

/* Larger screens get expanded layer control and visible sidebar */
if (document.body.clientWidth <= 767) {
  var isCollapsed = true;
} else {
  var isCollapsed = false;
}

var baseLayers = {
  "Street Map": mapquestOSM,
  "Aerial Imagery": mapquestOAM,
  "Imagery with Streets": mapquestHYB
};

var groupedOverlays = {
  "Layers": {
    "Locations": locations,
    "Parcels": parcelLayer,
    "County":county
  },
  "Business Section": {
    "<img src= '+bizIcon+' width='24' height='28'>&nbsp;Businesses": bizLayer
    
  }
};

var layerControl = L.control.groupedLayers(baseLayers, groupedOverlays, {
  collapsed: isCollapsed
}).addTo(map);

/* Highlight search box text on click */
$("#searchbox").click(function () {
  $(this).select();
});

/* Prevent hitting enter from refreshing the page */
$("#searchbox").keypress(function (e) {
  if (e.which == 13) {
    e.preventDefault();
  }
});
$("#printBtn").click(function(){
  $('#map').print();
});
$("#featureModal").on("hidden.bs.modal", function (e) {
  $(document).on("mouseout", ".feature-row", clearHighlight);
});

/* Typeahead search functionality */
$(document).one("ajaxStop", function () {
  $("#loading").hide();
  sizeLayerControl();
  /* Fit map to boroughs bounds */
  map.fitBounds(parcels.getBounds());
  featureList = new List("features", {valueNames: ["feature-name"]});
  featureList.sort("feature-name", {order:"asc"});

  var parcelBH = new Bloodhound({
    name: "Parcels",
    datumTokenizer: function (d) {
      return Bloodhound.tokenizers.whitespace(d.name);
    },
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    local: parcelSearch,
    limit: 10
  });

  var locationsBH = new Bloodhound({
    name: "Locations",
    datumTokenizer: function (d) {
      return Bloodhound.tokenizers.whitespace(d.name);
    },
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    local: locationSearch,
    limit: 10
  });
  var bizBH = new Bloodhound({
    name: "Business",
    datumTokenizer: function (d) {
      return Bloodhound.tokenizers.whitespace(d.name);
    },
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    local: bizSearch,
    limit: 10
  });
  locationsBH.initialize();
  bizBH.initialize();
  parcelBH.initialize();

  /* instantiate the typeahead UI */
  $("#searchbox").typeahead({
    minLength: 3,
    highlight: true,
    hint: true
  }, {
    name: "Locations",
    displayKey: "name",
    source: locationsBH.ttAdapter(),
    templates: {
      header: "<h4 class='typeahead-header'>Locations</h4>"
    }
  }, {
    name: "Parcels",
    displayKey: "name",
    source: parcelBH.ttAdapter(),
    templates: {
      header: "<h4 class='typeahead-header'>Parcels</h4>",
      suggestion: Handlebars.compile(["{{name}}<br>&nbsp;<small>{{address}}</small>"].join(""))
    }
  }, {
    name: "Bussiness",
    displayKey: "name",
    source: bizBH.ttAdapter(),
    templates: {
      header:'<h4 class="typeahead-header"><img width="16" height="18" src= '+bizIcon+'>&nbsp;Business</h4>',
      suggestion: Handlebars.compile(["{{name}}<br>&nbsp;<small>{{address}}</small>"].join(""))
    }
  }).on("typeahead:selected", function (obj, datum) {
    if (datum.source === "Locations") {
      map.fitBounds(datum.bounds);
    }
    if (datum.source === "Bussiness") {
      if (!map.hasLayer(bizLayer)) {
        map.addLayer(bizLayer);
        map.fitBounds(datum.bounds);
      }
      map.setView([datum.lat, datum.lng], 17);
      if (map._layers[datum.id]) {
        map._layers[datum.id].fire("click");
      }
    }
    if (datum.source === "Parcels") {
      if (!map.hasLayer(parcelLayer)) {
        map.addLayer(parcelLayer);
        //map.fitBounds(datum.bounds);
      }
      map.setView([datum.lat, datum.lng], 17);
      if (map._layers[datum.id]) {
        map._layers[datum.id].fire("click");
      }
    }
    if ($(".navbar-collapse").height() > 50) {
      $(".navbar-collapse").collapse("hide");
    }
  }).on("typeahead:opened", function () {
    $(".navbar-collapse.in").css("max-height", $(document).height() - $(".navbar-header").height());
    $(".navbar-collapse.in").css("height", $(document).height() - $(".navbar-header").height());
  }).on("typeahead:closed", function () {
    $(".navbar-collapse.in").css("max-height", "");
    $(".navbar-collapse.in").css("height", "");
  });
  $(".twitter-typeahead").css("position", "static");
  $(".twitter-typeahead").css("display", "block");
});

// Leaflet patch to make layer control scrollable on touch browsers
var container = $(".leaflet-control-layers")[0];
if (!L.Browser.touch) {
  L.DomEvent
  .disableClickPropagation(container)
  .disableScrollPropagation(container);
} else {
  L.DomEvent.disableClickPropagation(container);
}
