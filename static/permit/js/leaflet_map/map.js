/* Define base layers */
var cycleURL='http://{s}.tile.thunderforest.com/cycle/{z}/{x}/{y}.png';
var cycleAttrib='Map data © OpenStreetMap contributors';
var OpenCycleMap = new L.TileLayer(cycleURL, {attribution: cycleAttrib}); 

var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
var osmAttrib='Map data © openstreetmap contributors';
var OpenStreetMap = new L.TileLayer(osmUrl, {attribution: osmAttrib});

var mapnikURL = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
var mapnikAttrib = "http://openstreetmap.org";
var Mapnik = new L.TileLayer(mapnikURL, {attribution: mapnikAttrib});

var MapQuestURL ='http://oatile{s}.mqcdn.com/tiles/1.0.0/sat/{z}/{x}/{y}.jpg';
var	mapquestattrib = 'Tiles Courtesy of MapQuest';
var MapQuest = new L.TileLayer(MapQuestURL,{attribution: mapquestattrib});

var Esri_WorldImageryURL = 'http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}';
var Esri_WorldImageryattrib = 'Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community';
var Esri_WorldImagery = new L.TileLayer(Esri_WorldImageryURL, {attribution: Esri_WorldImageryattrib});



/* Google map layers*/
var googlemap= "http://maps.google.com/maps/api/js?sensor=true";

/*OpenLayers*/



/* create new layer group */
var layer_business = new L.LayerGroup();
var array_markers = new Array();

/* create custom marker which will represent business in layer 'layer_business' */
customMarker = L.Marker.extend({
   options: { 
      title: 'BizTrac',
   }
});

/* define function which adds markers from array to layer group */
function AddPointsToLayer() {
    for (var i=0; i<array_markers.length; i++) {
        array_markers[i].addTo(layer_business);
    }
} 

/* Get all business from DB and add them to layer:_business */
$.ajax({
	url: '/map/get_business/',
	type: 'GET',
	success: function(response) {
        $.each(eval(response), function(key, val) {	  
        	//fields in JSON that was returned      	
        	var fields = val.fields; 

        	// parse point field to get values of latitude and longitude
        	var regExp = /\(([^)]+)\)/;
			var matches = regExp.exec(fields.geom);
			var point = matches[1];
			var lon=point.split(' ')[0];
			var lat=point.split(' ')[1];

        	//function which creates and adds new markers based on filtered values
        	marker = new customMarker([lat, lon], {
			    title: fields.business_name,
			    opacity: 1.0  
			}); 
			marker.bindPopup("<br><strong>Form:</strong>"+ fields.business_form + "<br><strong>Type:</strong>" + fields.business_type + "<br><strong>Compliance:</strong>"
				+ fields.business_compliance);
        	marker.addTo(map);
        	array_markers.push(marker);
        });

        // add markers to layer and add it to map
        AddPointsToLayer();
    }
});

/* create map object */
var map = L.map('map', {
	center: [-0.4030, 36.9654],
	zoom: 12,
	fullscreenControl: true,
	fullscreenControlOptions: {
		position: 'topleft'
	},
	layers: [OpenStreetMap, layer_business]
});

var baseLayers = {
	"OpenCycleMap": OpenCycleMap,
	"OpenStreetMap": OpenStreetMap,
	"Esri_WorldImagery": Esri_WorldImagery,
	"Mapnik": Mapnik,
	"MapQuest": MapQuest
	/* Google Maps
	"Google Hybrid": Google Hybrid,
	"Google Satellite": Google Satellite,
	"OpenLayers": OpenLayers
	*/
};

var overlays = {
	"Businesses in Nyeri": layer_business
};

L.control.layers(baseLayers, overlays).addTo(map);


/* S I D E B A R   F I L T E R */
var sidebar = L.control.sidebar('sidebar', {
    position: 'left'
});
map.addControl(sidebar);

setTimeout(function () {
    sidebar.show();
}, 300);

$('#filter_control').click(function() {
    sidebar.show();
});


/* getResult function is called every time when user filters map objects using sidebar filter */
function getResult() {
	// fetch value of all filter fields
	var selected_form = $("#select_form").val();
	var selected_type = $("#select_type").val();	
	var boolean_compliance = $("#select_compliance").val();

	// get fields where value is not 'all' so that you later filter only those fields
	var fields = new Array();

	if (selected_form !== 'all') {
		fields.push("form");
	}

	if (selected_type !== 'all') {
		fields.push("type");
	}

	if (boolean_compliance !== 'all') {
		fields.push("compliance");
	}

	/* ajax call to get all business with defined filter values */
	$.ajax({
		url: '/map/business/filter/',
		type: 'GET',
		data: "form=" + selected_form + "type=" + selected_type + "&compliance=" + boolean_compliance 
		+ "&fields=" + fields,
		success: function(response) {
			// first delete all markers from layer business
			array_markers.length=0;
	        layer_business.clearLayers();

	        $.each(eval(response), function(key, val) {	  
	        	//fields in JSON that was returned      	
	        	var fields = val.fields; 

	        	// parse point field to get values of latitude and longitude
	        	var regExp = /\(([^)]+)\)/;
				var matches = regExp.exec(fields.geom);
				var point = matches[1];
				var lon=point.split(' ')[0];
				var lat=point.split(' ')[1];

	        	//function which creates and adds new markers based on filtered values
	        	marker = new customMarker([lat, lon], {
				    title: fields.business_name,
				    opacity: 1.0  
				}); 
	        	marker.addTo(map);
	        	marker.bindPopup("<strong>Form:</strong><br>" + fields.business_form + "<br><strong>Type:</strong>"
				+ fields.business_type + "<br><strong>Compliance:</strong>"+ fields.business_compliance);
	        	array_markers.push(marker);
	        });

	        // add markers to layer and add it to map
	        AddPointsToLayer();
	    }
	});
}
