//Declare the map as a global variable
var map
var stationLayer
var regionLayer
var eventLayer
var tripLayer

var stationLayerVisible
var regionLayerVisible
var eventLayerVisible
var tripLayerVisible

//Draws the leaflet map and localises it based on the dataset (also adds the sidebar)
function draw_map(dataset)
{
	if(dataset == 'Divvy')
		center_coords = [41.84,-87.65]
	else if(dataset == 'New York Taxi')
		center_coords = [40.68,-73.8]

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

//Accepts a list of stations in the form (name, longitude, latitude) and plots them as a layer
function plot_stations(stations)
{
	stationLayer = L.geoJSON().addTo(map);

	var stationsMarkerOptions = {
		radius: 4,
		fillColor: "#ff7800",
		color: "#000",
		weight: 1,
		opacity: 1,
		fillOpacity: 0.8
	};

	function onEachFeature(feature, layer) {
	  layer.bindPopup(feature.properties.name);
	}

	function pointToLayer(feature, latlng) {
		return L.circleMarker(latlng, stationsMarkerOptions);
	}

	for(var i = 0; i < stations.length; i++)
	{
		var stationFeature = {
			"type": "Feature",
			"properties": {
					"name": stations[i][0],
			},
			"geometry": {
					"type": JSON.parse(stations[i][1]).type,
					"coordinates": JSON.parse(stations[i][1]).coordinates
			}
		};



		stationLayer.addLayer(L.geoJSON(stationFeature, {
			onEachFeature: onEachFeature,
			pointToLayer: pointToLayer
		}))
	}

	stationLayer.addTo(map)
	stationLayerVisible = true
}

//Accepts a list of districts in the form (info, geometry) and plots them as a layer on the map
function plot_regions(regions)
{
	regionLayer = L.geoJSON().addTo(map);

	var regionPolygonOptions = {
		opacity: 0.7,
		fillOpacity: 0.3
	};

	function onEachFeature(feature, layer) {
		layer.bindPopup(feature.properties.name);
	}

	for(var i = 0; i < regions.length; i++)
	{
		var regionFeature = {
	    "type": "Feature",
	    "properties": {
	        "name": regions[i][0]
	    },
	    "geometry": {
	        "type": JSON.parse(regions[i][1]).type,
	        "coordinates": JSON.parse(regions[i][1]).coordinates
	    }
		};

		regionLayer.addLayer(L.geoJSON(regionFeature, {
			style: regionPolygonOptions,
			onEachFeature: onEachFeature
		}))
	}

	regionLayer.addTo(map)
	regionLayerVisible = true
}

function plot_events(events)
{
	eventLayer = L.geoJSON().addTo(map);
}

function plot_trips(trips)
{
	if(map.hasLayer(tripLayer))
	{
		map.removeLayer(tripLayer)
	}

	tripLayer = L.geoJSON().addTo(map);
	trips = JSON.parse(trips)
	start_points = trips.start_geom
	end_points = trips.end_geom

	var points = []

	for(var i = 0; i < Object.keys(start_points).length; i++)
	{
		var points = []
		points.push(L.latLng(JSON.parse(start_points[i]).coordinates[1],JSON.parse(start_points[i]).coordinates[0]))
		points.push(L.latLng(JSON.parse(end_points[i]).coordinates[1],JSON.parse(end_points[i]).coordinates[0]))

		tripLayer.addLayer(L.polyline(points, {color: '#00ff00'}));
	}

	tripLayer.addTo(map)
	tripLayerVisible = true
}

//Toggles the regions on or off depending on the value of the 'regions' checkbox
function toggle_regions()
{
	if(regionLayerVisible == true)
	{
		map.removeLayer(regionLayer)
		regionLayerVisible = false
	}
	else
	{
		regionLayer.addTo(map)
		regionLayer.bringToBack()
		regionLayerVisible = true
	}
}

function toggle_trips()
{
	if(tripLayerVisible == true)
	{
		map.removeLayer(tripLayer)
		tripLayerVisible = false
	}
	else
	{
		tripLayer.addTo(map)
		tripLayer.bringToFront()
		tripLayerVisible = true
	}
}

//Toggles the stations on or off depending on the value of the 'stations' checkbox
function toggle_stations()
{
	if(stationLayerVisible == true)
	{
		map.removeLayer(stationLayer)
		stationLayerVisible = false
	}
	else
	{
		stationLayer.addTo(map)
		stationLayer.bringToFront()
		stationLayerVisible = true
	}
}

function toggle_events()
{
	if(eventLayerVisible == true)
	{
		map.removeLayer(eventLayer)
		eventLayerVisible = false
	}
	else
	{
		eventLayer.addTo(map)
		eventLayer.bringToFront()
		eventLayerVisible = true
	}
}
