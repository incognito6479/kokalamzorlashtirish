function showDataOnNewTab(event) {
        var table=event.currentTarget;
        var tableData= table.parentNode.parentNode.firstElementChild.innerText;
        // console.log(tableData);

        $.ajax({
            type: "POST",
            url : 'https://jsonplaceholder.typicode.com/users',
            data : {
                plantId : tableData,
            },
            success : function(responseText) {
                console.log(responseText.plantId);
                // document.getElementById("output").innerHTML = responseText;
            }
        });

        var  button = event.target;
        var  buttonValue=button.value;
        console.log(buttonValue);
        var w = window.open('', '_blank');
        var head = w.document.getElementsByTagName('head')[0];
        w.document.head.innerHTML = '<title>Plant_Data</title></head>';
        w.document.body.innerHTML = '<body><div id="map_canvas" style="display: block; width: 100%; height: 100%; margin: 0; padding: 0;"></div></body>';
        var loadScript = w.document.createElement('script');
        //Link to script that load google maps from hidden elements.
        loadScript.type = "text/javascript";
        loadScript.async = true;
        loadScript.src = "https://maps.googleapis.com/maps/api/js?sensor=false&callback=initialize";
        var googleMapScript = w.document.createElement('script');
        //Link to google maps js, use callback=... URL parameter to setup the calling function after google maps load.
        googleMapScript.type = "text/javascript";
        googleMapScript.async = false;
        googleMapScript.text = 'var map;';
        googleMapScript.text += 'function initialize() {';
        googleMapScript.text += '  var latlng = new google.maps.LatLng('+buttonValue+');';
        googleMapScript.text += '  var mapOptions = {';
        googleMapScript.text += '    center: latlng,';
        googleMapScript.text += '    zoom: 11, ';
        googleMapScript.text += '  };';
        googleMapScript.text += '  map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);';
        googleMapScript.text += '  var marker = new google.maps.Marker({';
        googleMapScript.text += '    position: latlng,';
        googleMapScript.text += '    map: map';
        googleMapScript.text += ' });';

        googleMapScript.text += 'marker.addListener("click", () => {';
        googleMapScript.text += 'var plantInfo=\'<div>\' +';
        googleMapScript.text += '\'<h5>Test</h5>\' +';
        googleMapScript.text += '\'</div>\';';
        googleMapScript.text += 'if (!location.name)';
        googleMapScript.text += 'location.name = "default";';
        googleMapScript.text += ' const infowindow= new google.maps.InfoWindow({';
        googleMapScript.text += ' content: plantInfo';
        googleMapScript.text += ' });';
        googleMapScript.text += ' infowindow.open(map, marker);';
        googleMapScript.text += ' });';

        googleMapScript.text += 'var geocoder = new google.maps.Geocoder;';
        googleMapScript.text += 'var infowindow = new google.maps.InfoWindow;';
        googleMapScript.text += 'geocoder.geocode({"location": latlng}, function(results, status) {';
        googleMapScript.text += ' infowindow.setContent(results[0].formatted_address);';
        googleMapScript.text += ' infowindow.open(map, marker);';
        googleMapScript.text += '});';
        googleMapScript.text += '}';
        head.appendChild(loadScript);
        head.appendChild(googleMapScript);
}