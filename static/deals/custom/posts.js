$(document).ready(function() {

  //Add New Post
  $( "body" ).on("submit", "#new-posts-excel", function( event ) {
    event.preventDefault();
    $("body").find("[type=submit]").attr('disabled', true);
    $("body").find(".loading").show();
    $.ajax({url: '/insert_post/',
            method: 'POST',
           data: new FormData(this),
           contentType: false,
           processData:false,
           cache: false,
            'success': function(response) {
              if(response == 'Success') {
                alert("Data Updated Successfully");
                $("form#new-posts-excel")[0].reset();
                $("body").find(".loading").hide();
                $("body").find("[type=submit]").attr('disabled', false);
              }
              else {
                alert(response);
                $("body").find(".loading").hide();
                $("body").find("[type=submit]").attr('disabled', false);
              }
            },
            'error': function (jqXHR, status, err){
              $("body").find(".loading").hide();
              alert("Network Error");
            }
          });

  });

  // Add New Row
  $("body").on("click", ".add-new-exc", function( event ) {
    event.preventDefault();
    new_row = $(this).closest('div.add-excel-col').clone();
    new_row.find('input').val('');
    $(this).find('i').removeClass('fa-plus');
    $(this).find('i').addClass('fa-minus');
    $(this).removeClass('btn-success');
    $(this).addClass('btn-danger');
    $(this).removeClass('add-new-exc');
    $(this).addClass('rem-new-exc');
    $(this).closest('div.add-excel-col').after(new_row);
  });

  // Remove Current Row
  $("body").on("click", ".rem-new-exc", function( event ) {
    event.preventDefault();
    $(this).parent().parent().remove();
  });

});
