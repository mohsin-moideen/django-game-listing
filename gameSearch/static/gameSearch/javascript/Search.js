var availableTags = [];
$(function () {
  $('[data-toggle="tooltip"]').tooltip().show();
});
$(function() {
  $(".autocomplete").autocomplete({
    source: availableTags
  });
}
);
$( "#search" ).keyup(function( event ) {
    $('[data-toggle="tooltip"]').tooltip().show();
   $.ajax({
    url:"/accelGames/autocomplete/",
       data:{
        'search': $( "#search" ).val()
       }
  }).done(function(titles) {
      availableTags.splice(0, availableTags.length);
      for(var x in titles){
          availableTags.push(titles[x].title);
      }
  });
});

$("#searchForm").submit(function(e) {
    e.preventDefault();
});
function formSubmit(page) {
    var input = $("<input>")
               .attr("type", "hidden")
               .attr("name", "page").val(page);
    $('#searchForm').append($(input));
    var url = "/accelGames/allGames/";
    $.ajax({
           type: "GET",
           url: url,
           data: $("#searchForm").serialize(),
           success: function(data)
           {
              $(".results").remove();
              $("#result-holder").append(data);
           }
    });
}
function favourite(id) {
    var csrf_token = $("input[name=csrfmiddlewaretoken]").val();
    var url = "/accelGames/favourite/";
    $("#fav_"+id).html("<p>Added to favourites</p>");
    $.ajax({
           type: "POST",
           url: url,
           data: {
               "id" : id,
               "csrfmiddlewaretoken": csrf_token
           },
           success: function()
           {

           }
    });
}