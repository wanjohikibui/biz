var map = L.map('map').setView([0.5667, 34.5667], 14);
              
        mapLink ='<a href="http://openstreetmap.org">OpenStreetMap</a>';
        L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; ' + mapLink,
          maxZoom:32,
          }).addTo(map);

        function onMapClick(e) {
          var lat = e.latlng.lat;
          var lng = e.latlng.lng;

          // Every time when user click on map we want to delete previous marker and create new marker on the new position where the user clicked      
          if (typeof marker != 'undefined') {
              map.removeLayer(marker);  // delete previous marker
              marker = L.marker([lat, lng]).addTo(map);  // add new marker
          }
          else {
              marker = L.marker([lat, lng]).addTo(map);  // add new marker
          }
          
          // we want to pass value of longitued and latitude to input field with id 'coordinates'
          // note that we set that field as hidden because we don't want user to type the coordinates there. We want him to set marker on map 
          $('#coordinates').val(lng + ',' + lat) 
          //alert('coordinates:' + lng + ',' + lat)         
        }

        // call the onMapClick function when user click on map
        map.on('click', onMapClick);