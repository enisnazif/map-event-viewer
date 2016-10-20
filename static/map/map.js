//function that draws the map and localises it to chicago

var mymap = L.map('mapid').setView([41.84,-87.65], 15);
L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiZW5pc24iLCJhIjoiY2l1NXRqOWowMDAxejJ0cWoyNmNhdGwxdSJ9.6AImF4A-ZBf_VmKTHGJLOA', {
	maxZoom: 18,
	attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
		'<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
		'Imagery © <a href="http://mapbox.com">Mapbox</a>',
	id: 'mapbox.streets'
}).addTo(mymap);

//function that draws the map and localises it to chicago
//accepts a list of stations in the form (name, longitude, latitude) and plots them as markers
function draw_map_with_stations(stations)
{
	var mymap = L.map('mapid').setView([41.84,-87.65], 15);
	L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiZW5pc24iLCJhIjoiY2l1NXRqOWowMDAxejJ0cWoyNmNhdGwxdSJ9.6AImF4A-ZBf_VmKTHGJLOA', {
		maxZoom: 18,
		attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
			'<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
			'Imagery © <a href="http://mapbox.com">Mapbox</a>',
		id: 'mapbox.streets'
	}).addTo(mymap);

	for(var i = 0; i < stations.length; i++)
	{
		L.marker([stations[i][1], stations[i][2]]).addTo(mymap).bindPopup(stations[i][0]).openPopup();
	}
}
