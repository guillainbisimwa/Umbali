var s = document.getElementsByName('slug')[0].value;
var d = {csrfmiddlewaretoken: document.getElementsByName("csrfmiddlewaretoken")[0].value,};
var video = document.getElementById('video');
$.ajax({
    url: "/get/live/".concat(s).concat("/"),
    method: "POST",
    data: d,
    success: function(e) {
      if(Hls.isSupported()) {
          var hls = new Hls();
          hls.loadSource(e.hls);
          hls.attachMedia(video);
          hls.on(Hls.Events.MANIFEST_PARSED,function() {
              video.play();
          });
       }else if (video.canPlayType('application/vnd.apple.mpegurl')) {
          video.src = e.hls;
          video.addEventListener('loadedmetadata',function() {
            video.play();
          });
       }
    },
    statusCode: {
        404: function() {
          var e = $("<h2 class='text-center' style='color: white;margin-top: 20px;'></h2>");
          e.text("Quelque chose s'est mal passé #Erreur");
          $("#videoLayout").append(e);
          document.getElementById("video").remove();
          document.getElementById("comment_btn").remove();
        }
    }
})
