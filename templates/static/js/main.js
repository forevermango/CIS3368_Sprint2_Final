$(document).ready(function() {
  $.ajax({
      url: '/api/data',
      method: 'GET',
      success: function(response) {
          $('#message').text(response.message);
      },
      error: function(error) {
          console.log(error);
      }
  });
});
fetch('/api/cargo', {
  method: 'POST',
  headers: {
      'Content-Type': 'application/json',
  },
  body: JSON.stringify({
      Weight: 'your_weight',
      Cargotype: 'your_cargotype',
      departure: 'your_departure',
      arrival: 'your_arrival',
      shipid: 'your_shipid',
  }),
})
.then((response) => response.text())
.then((data) => console.log(data))
.catch((error) => console.error('Error:', error));

