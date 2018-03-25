$(document).ready(function() {

  /*$.fn.render_index_post_html = function(resp) {
    var file_data = ''
    $.get($(location).attr('protocol') + '//' +$(location).attr('host') + '/index_single_post/', function(data){
      data = data.replace('\n', '<br/>');
      file_data = data;
    });
  }*/

  $(window).on('load', function() {
    $.ajax({url: '/display_posts/',
            method: 'POST',
           data: {'csrfmiddlewaretoken': $("[name='csrfmiddlewaretoken']").val()},
            'success': function(response) {
              //resp = $.parseJSON(response);
              //$.fn.render_index_post_html(resp);
              $('div.latest-deals').find('.container').append(response);
            }});
  });





});
