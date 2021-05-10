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
                $("#exampleModal").find(".modal-body").html("Aliment : " + datas + " ajouté aux favoris !!");
                $('#exampleModal').modal('show');
            },
            error: function( errorThrown )
            {
                alert("ERROR : " + errorThrown);
            }
        });
    });
});

$(document).ready(function() {
    $(".rating").on("click", function ( event ) {
        var clicked_aliment = $(this).attr('id');
        $('#rateModal').on('shown.bs.modal', function ( event ) {
            $(".rate-btn").on("click", function ( event ) {
                var clicked_rate_btn = $(this).attr('id');
                $.ajax({
                    method: "POST",
                    headers: {'X-CSRFToken': getCookie('csrftoken')},
                    url: "/rating/",
                    data: {
                        aliment: clicked_aliment,
                        rate: clicked_rate_btn,
                    },
                    success: function ( result ) {
                        document.location.reload();
                    },
                    error: function ( datas ) {
                        alert("ERROR : " + errorThrown);
                    }
                });
            });
        });
        $('#rateModal').modal('show');
    });
});
