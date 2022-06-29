function initMap() {

    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 6,
        center: { lat: 41.6674552, lng: 62.2413207 },
    });

    map.data.loadGeoJson(
        'https://dshk.uz/static/uzb.json'
    );
    map.data.setStyle(function() {
        return (
            {  fillColor: generateRandomColor(),
            strokeWeight: 1,
            zIndex: 1}
            );
        function generateRandomColor() {
            var letters = '0123456789ABCDEF';
            var color = '#';
            for (var i = 0; i < 6; i++) {
                color += letters[Math.floor(Math.random() * 16)];
            }
            return color;
        }
    });

    const markers = locations.map((location, i) => {
        return new google.maps.Marker({
            position: location,

        });
    });

    new MarkerClusterer(map, markers, {
        imagePath:
            "https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m",
    });


    const plants = {lat: 40.9753455, lng: 63.4556948};
    const contentString =
        '<div id="content">' +
        '<div id="siteNotice">' +
        "</div>" +
        '<h1 id="firstHeading" class="firstHeading">Plant_name</h1>' +
        '<div id="bodyContent">' +
        "<p><b>Uluru</b>, also referred to as <b>Ayers Rock</b>, is a large " +
        "sandstone rock formation in the southern part of the " +
        "Northern Territory, central Australia. It lies 335&#160;km (208&#160;mi) " +
        "south west of the nearest large town, Alice Springs; 450&#160;km " +
        "(280&#160;mi) by road. Kata Tjuta and Uluru are the two major " +
        "features of the Uluru - Kata Tjuta National Park. Uluru is " +
        "sacred to the Pitjantjatjara and Yankunytjatjara, the " +
        "Aboriginal people of the area. It has many springs, waterholes, " +
        "rock caves and ancient paintings. Uluru is listed as a World " +
        "Heritage Site.</p>" +
        "</div>" +
        "</div>";
    const infowindow = new google.maps.InfoWindow({
        content: contentString,
    });

    const marker = new google.maps.Marker({
        position: plants,
        map,
        title: "City name",
    });
    marker.addListener("click", () => {
        infowindow.open(map, marker);
    });
}

//daraxt ekilgan locationlar
const locations = [
    { lat: 39.9953455, lng: 64.3556948 },
    { lat: 41.3022312, lng: 69.4006981 },
    { lat: 41.2467509, lng: 69.1594451 },
    { lat: 41.2029645, lng: 69.1004188 },
    { lat: 41.1865098, lng: 69.1729599 },
    { lat: 41.0189961, lng: 69.2080205 },
    { lat: 40.8493533, lng: 69.0716543 },
    { lat: 40.6904208, lng: 68.8560815 },
    { lat: 39.8919679, lng: 65.5616048 },
    { lat: 40.6489632, lng: 65.1650192 },
    { lat: 40.6989632, lng: 65.1750192 },
    { lat: 41.6989632, lng: 64.1750192 },
    { lat: 41.5989632, lng: 64.1550192 },

];

initMap();

