//Declare the map as a global variable
var map

//Draws the leaflet map and localises it based on the dataset (also adds the sidebar)
function draw_map(dataset)
{
	if(dataset == 'Divvy')
		center_coords = [41.84,-87.65]
	else if(dataset == 'New York Taxi')
		center_coords = [40.7128,-74.0059]

	map = L.map('mapid').setView(center_coords, 11);
	L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiZW5pc24iLCJhIjoiY2l1NXRqOWowMDAxejJ0cWoyNmNhdGwxdSJ9.6AImF4A-ZBf_VmKTHGJLOA', {
		maxZoom: 15,
		attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
			'<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
			'Imagery © <a href="http://mapbox.com">Mapbox</a>',
		id: 'mapbox.streets'
	}).addTo(this.map);
	sidebar = L.control.sidebar('sidebar').addTo(this.map);
}

function remove_map()
{
	map.remove();
}

//Changes the location of the map depending on the dataset
function change_dataset(dataset)
{
	if(dataset == 'Divvy')
		center_coords = [41.84,-87.65]
	else if(dataset == 'New York Taxi')
		center_coords = [40.7128,-74.0059]

	map.panTo(new L.LatLng(center_coords[0], center_coords[1]));
}

//Accepts a list of stations in the form (name, longitude, latitude) and plots them as a layer
function plot_stations(stations)
{
	for(var i = 0; i < stations.length; i++)
	{
		var stationsMarkerOptions = {
    radius: 4,
    fillColor: "#ff7800",
    color: "#000",
    weight: 1,
    opacity: 1,
    fillOpacity: 0.8
		};
		var stationsLayer = {
			"type": "Feature",
			"properties": {
					"name": stations[i][0],
			},
			"geometry": {
					"type": JSON.parse(stations[i][1]).type,
					"coordinates": JSON.parse(stations[i][1]).coordinates
			}
		};

		L.geoJSON(stationsLayer, {
    pointToLayer: function (feature, latlng) {
        return L.circleMarker(latlng, stationsMarkerOptions);
    }
	}).addTo(map).bindPopup(stationsLayer.properties.name);
	}
}

//Accepts a list of districts and plots them as a layer on the map
function plot_districts(districts)
{
	for(var i = 0; i < districts.length; i++)
	{
		var districtsLayer = {
	    "type": "Feature",
	    "properties": {
	        "name": districts[i][1]
	    },
	    "geometry": {
	        "type": JSON.parse(districts[i][2]).type,
	        "coordinates": JSON.parse(districts[i][2]).coordinates
	    }
		};

		L.geoJSON(districtsLayer).addTo(map).bindPopup(districtsLayer.properties.name);
	}
}
