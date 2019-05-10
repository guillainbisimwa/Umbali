var is_connected = setInterval(function() {
    var e = document.getElementsByName("slug")[0].value;
    $.ajax({
        url: "/get/live/".concat(e).concat("/"),
        method: "GET",
        statusCode: {
            404: function() {
                var e = $("<h2 class='text-center' style='color: white;margin-top: 20px;'></h2>");
                e.text("Veuillez vous déconnecter de l'ancien appareil pour regarder ici, contactez-nous si le problème persiste.");
                $("#videoLayout").append(e);
                document.getElementById("video").remove();
                document.getElementById("comment_btn").remove();
            }
        }
    })
}, 90000);
