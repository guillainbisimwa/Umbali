var video = document.getElementById("video"),
    d = {
        csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value
    },
    s = document.getElementsByName("slug")[0].value;
if (video.canPlayType("application/vnd.apple.mpegurl")) {
    $.ajax({
        url: "/get/live/".concat(s).concat("/"),
        method: "POST",
        data: d,
        success: function(e) {
            video.src = e.hls, video.addEventListener("loadedmetadata", function() {
                video.play()
            })
        },
        statusCode: {
            404: function() {
                alert("Error #500");
                var e = $("<h2 class='text-center' style='color: white;margin-top: 20px;'></h2>");
                e.text("Veuillez vous déconnecter de l'ancien appareil pour regarder ici, contactez-nous si le problème persiste."), $("#videoLayout").append(e), "#video".remove()
            }
        }
    })
} else if (Hls.isSupported()) {
    var hls = new Hls;
    hls.attachMedia(video), hls.on(Hls.Events.MEDIA_ATTACHED, function() {
        $.ajax({
            url: "/get/live/".concat(s).concat("/"),
            method: "POST",
            data: d,
            success: function(e) {
                hls.loadSource(e.hls);
                video.play()
            },
            statusCode: {
                404: function() {
                    var e = $("<h2 class='text-center' style='color: white;margin-top: 20px;'></h2>");
                    e.text("Veuillez vous déconnecter de l'ancien appareil pour regarder ici, contactez-nous si le problème persiste."), $("#videoLayout").append(e), document.getElementById("video").remove()
                }
            }
        }), hls.on(Hls.Events.MANIFEST_PARSED, function(e, t) {
            console.log("manifest loaded, found " + t.levels.length + " quality level")
        })
    })
} else {
    var msg = "Navigateur non supporté, Veuillez utiliser la dernière version de Firefox, Google Chrome, Safari, Microsoft Edge.",
        txt = $("<h4 class='text-center' style='color: white;margin-top: 20px;'></h4>");
    txt.text(msg), $("#videoLayout").append(txt)
}
