// Basemap - OSM
var osm = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
  });

// map Object/Instanz >> new!!
var myMap = L.map('mapid', {
    center: [37.8, -96.99],
    zoom: 4,
    layers: [osm]
});

/*
"nan" oder "NA" >> color >> white
min Value: 0.178608124613778
max Value: 1268.24342012
*/
function getColor(d) {
    return d > 1000 ? '#800026' :
           d > 500  ? '#BD0026' :
           d > 200  ? '#E31A1C' :
           d > 100  ? '#FC4E2A' :
           d > 50   ? '#FD8D3C' :
           d > 20   ? '#FEB24C' :
           d > 10   ? '#FED976' :
                      '#FFEDA0';
}

/* colored as to the amount of 'SOCstock30' they contain */
function style(feature) {
    return {
        fillColor: getColor(feature.properties.SOCstock30),
        // fillColor: "#FFF",
        radius: 4,
        color: "#555555",
        weight: 1,
        opacity: 1,
        fillOpacity: 0.8
    };
}

/* sites as points */
var points = L.geoJSON(myPoints, {
    pointToLayer: function (feature, latlng) {
        return L.circleMarker(latlng, style(feature));
    }
});

/* create control */
var baseMaps = {
    "OSM": osm
};

var overlayMaps = {
    "SOCstock30": points
};

L.control.layers(baseMaps, overlayMaps).addTo(myMap);

/* LEGEND */
var legend = L.control({position: 'bottomright'});

legend.onAdd = function (myMap) {

    var div = L.DomUtil.create('div', 'legend'),
        grades = [0, 10, 20, 50, 100, 200, 500, 1000],
        labels = [];

    div.innerHTML += "LEGEND" + "<br />";      // title of legend

    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    }

    return div;
};
legend.addTo(myMap);


