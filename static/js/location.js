getLocation();

var options = {
  enableHighAccuracy: true,
  timeout: 5000,
  maximumAge: 0
};

function success(position){
    var pos = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
    };
    console.log("Current location successfully found:\n", pos);

    $.ajax({
    type: 'POST',
    url: '/location',
    data: JSON.stringify({'latitude': pos.lat, 'longitude': pos.lng}),
    contentType: "application/json",
    success: function () {
        window.location.href = '/results'
    }
    });
}

function error(err) {
  console.warn(`ERROR(${err.code}): ${err.message}`);
}

function getLocation(){
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(success, error, options);
    } else {
        console.warn("Geolocation not enabled in this browser. Can't find geolocation.");
    }
}