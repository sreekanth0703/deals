$(document).ready(function() {

  //Login Submit Code
  $( "body" ).on("submit", "#login_check", function( event ) {
    //$('.loading').removeClass('display-none');
    event.preventDefault();
    var values = $(this).serializeArray();
    var this_data = $(this);
    $.ajax({url: '/member_login/',
            method: 'POST',
           data: values,
            'success': function(response) {
              response = $.parseJSON(response);
              if(response.status == 0) {
                $("#login_check")[0].reset();
                alert(response.message);
              }
              else {
                window.location.replace(window.location.origin + '/home/')
              }
            }});

  });

  //Logout Code
  $( "body" ).on("click", ".log-out", function( event ) { 
    event.preventDefault();
    $.ajax({url: '/logout/',
            method: 'GET',
            'success': function(response) {
                window.location.replace(window.location.origin + '/login/')
            }});

  });

});
