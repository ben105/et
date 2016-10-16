Polymer({

	is: 'calgrove-map',
	properties: {
		places: {
			type: Array,
			value: function() {
				return [];
			},
			notify: true
		}
	},
	handleResponse: function(e) {
		var gmap = document.querySelector('google-map');
		self.places = e.detail.response;
		self.places.forEach(function(place) {
			var marker = document.createElement('google-map-marker');
          		marker.setAttribute('latitude', place.lat);
          		marker.setAttribute('longitude', place.lon);
          		marker.setAttribute('title', place.count);
          		marker.innerHTML = place.count;
			Polymer.dom(gmap).appendChild(marker);
		});
	},
	ready: function() {
		

		setInterval(function(){
			var xhr = document.getElementById('XhrIO');
			xhr.generateRequest();
		}, 50000)
	}	
});
