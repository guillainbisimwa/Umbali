function prepareCallback() {
    webapi.avplay.play();
}
var d = {csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value},s = document.getElementsByName("slug")[0].value;;
$.ajax({
    url: "/get/live/".concat(s).concat("/"),
    method: "POST",
    data: d,
    success: function(e) {
        webapi.avplay.open(e.hls);
    },
    statusCode: {
        404: function() {
            alert("Error #500");
            var e = $("<h2 class='text-center' style='color: white;margin-top: 20px;'></h2>");
            e.text("Veuillez vous déconnecter de l'ancien appareil pour regarder ici, contactez-nous si le problème persiste."), $("#videoLayout").append(e), "#av-player".remove()
        }
    }
})
webapi.avplay.prepareAsync(prepareCallback);
