function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function() {
    $(".saving").on("click", function ( event ) {
        var clicked_aliment = $(this).attr('id');
        $.ajax({
            method: "POST",
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            url: "/saving/",
            data: {
                aliment: clicked_aliment,
            },
            dataType : "json",
            success: function( datas )
            {
                $(".modal-body").html("Aliment : " + datas + " ajouté aux favoris !!");
                $('#exampleModal').modal('show');
            },
            error: function( errorThrown )
            {
                alert("ERROR : " + errorThrown);
            }
        });
    });
});