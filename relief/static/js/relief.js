function initPage() {
  catchIE();
  $(window).resize(setSize);
  setSize();
  $('body').removeClass("waitjs");
}

$(window).ready(function () {
  if (! smooth_loading) {
    initPage();
  }
});

$(window).load(function () {
  if (smooth_loading) {
    initPage();
  }
});

function catchIE() {
  if (BrowserDetect.browser == "Explorer") {
    $("html").addClass("ie");
  }
}

function setSize() {
  var t = $('div#cont'),
      page = $('section#page'),
      nw = img_width,
      nh = img_height,
      wantedratio = nw / nh,
      actualratio = ($(window).width() * zoom_width) / ($(window).height() * zoom_height),
      full_width = $(window).width() * (zoom_width / 100),
      full_height = $(window).height() * (zoom_height / 100);

  $(page).width((zoom_width).toString() + '%').height((zoom_height).toString() + '%');

  if (wantedratio >= actualratio) { // portrait $(window)
    $(t).width('100%').height(full_width / wantedratio);

    if (zoom_height <= 100) {
      $(t).css('margin-top', ((full_height) - $(t).height()) / 2);
    }
    else if (zoom_height > 100) {
      $(page).height(full_width / wantedratio);
      $(t).css('margin-top', 0);
      // To keep only first 100% of page visible and at bottom of the page, this is the margin-top value needed.
      //$(t).css('margin-top', $(window).height() - (full_width / wantedratio) / (zoom_height / 100));
    }
  }
  else { // paysage $(window)
    $(t).height('100%').width(full_height * wantedratio).css('margin-top', '');;

    if (zoom_width > 100) {
      $(page).width(full_height * wantedratio);
      $(t).css('margin-left', 0);
    }
  }
}
