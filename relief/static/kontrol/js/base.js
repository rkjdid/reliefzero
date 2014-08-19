var wait = true;

$(document).ready(function () {
  try {
    $('#id_page_background').spectrum({
      showInput: true,
      showInitial: true,
      preferredFormat: "hex"
    });
    initLayout();
  } catch (all) {
    alert(all + "\n\n" + "mailto: romainknezevic@gmail.com plz");
  } finally {
    wait = false;
  }
});

$(window).load(function() {
  while (wait)
    sleep(20);

  if (typeof(__waitjs) == "function")
    __waitjs();
});

// Include all elements to encapsulate
var wrapAround = [
  ".field-x",
  ".field-y",
  ".field-width",
  ".field-height"
];

function initLayout() {
  $('.dynamic-froms').find('fieldset').each(function () {
    // Ensure preview is added only once
    if ($(this).find('div.col1.preview_data').length > 0)
      return;

    var data= $('<div class="col1 preview_data">');
    var clone = $(this).clone();

    var target;
    for (var s in wrapAround) {
      target = $(clone).find(wrapAround[s]);
      $(data).append(target);
      $(clone).find(target).remove();
    }

    $(data).children().last().css('border-bottom', 'none');
    var mother = $(clone).clone().empty();
    mother.append($("<div class='preview_cont'>").append(data).append("<div class='col1 preview'>"));

    $(clone).children().each(function () {
      $(mother).append(this);
    });

    $(this).before(mother);
    $(this).remove();
    insertPreview(mother);
  });

  // Event handler for "Add new Link" button
  $('#froms-group').find('div.add-row').find('a').click(function() {
    initLayout();
  });
}

function initLink(data, imgwrap) {
  var lnk = $(imgwrap).find('div.link');
  if (lnk.length > 0)
    lnk = $(lnk).first();
  else
    lnk = createLink(data, imgwrap);

  drawLink(data, lnk);
}

function createLink(data, imgwrap) {
  var lnk = $('<div class="link">');
  $(lnk).draggable({
    containment : 'parent',
    stop : function () {updateData(data, lnk); }
  }).resizable({
       handles: 'all',
       containment : 'parent',
       stop : function () {updateData(data, lnk);}
  });

  $(lnk).css({
    'position':'absolute',
    'background':'#' + Math.floor((Math.abs(Math.sin(data[2].val()) * 16777215)) % 16777215).toString(16)
  });
  $(imgwrap).append(lnk);

  for (var d in data) {
    $(data[d]).change(function () {
      drawLink(data, lnk);
    });
  }

  // Bind mousedrag event
  var isDragging,
     x0, y0, x1, y1, rect;
  var dragArea = $(imgwrap).find('.preview_glass');
  $(dragArea)
    .mousedown(function(e0) {
      isDragging = false;
      e0.originalEvent.preventDefault();
      var poff = $(dragArea).parent().offset();
      x0 = e0.pageX - poff.left;
      y0 = e0.pageY - poff.top;
      var nlnk = $(this).siblings('.link');
      $(dragArea).add(nlnk).addClass('drag');
      var contw = $(dragArea).parent().width(),
         conth = $(dragArea).parent().height();

      $(window).mouseup(function() {
        if (!isDragging) { // abort for click, only drag
          $(window).unbind("mousemove");
          $(window).unbind("mouseup");
          $(dragArea).add(nlnk).removeClass('drag');
        }
        $(dragArea).add(nlnk).removeClass('drag');
      });

      $(window).mousemove(function(e) {
        isDragging = true;
        var poff = $(dragArea).parent().offset();
        x1 = e.pageX - poff.left;
        y1 = e.pageY - poff.top;
        rect = getRect(x0, y0, x1, y1, contw, conth);
        drawLink(rect, nlnk);

        $(window).mouseup(function() {
          updateData(data, nlnk);
          $(window).unbind("mousemove");
          $(window).unbind("mouseup");
          $(dragArea).add(nlnk).removeClass('drag');
        });
      });
  });

  return lnk;
}

function getRect(x0, y0, x1, y1, contw, conth) {
  if (x1 < 0)
    x1 = 0;
  if (y1 < 0)
    y1 = 0;

  var w = x1 - x0,
     h = y1 - y0,
     x, y;

  if (w < 0) {
    w = -w; x = x1;
  } else x = x0;

  if (h < 0) {
    h = -h; y = y1;
  } else y = y0;

  x = (x / contw) * 100;
  y = (y / conth) * 100;
  w = (w / contw) * 100;
  h = (h / conth) * 100;

  if ((x + w) > 100)
    w = 100 - x;
  if ((y + h) > 100)
    h = 100 - y;

  return [x, y, w, h];
}


function drawLink(data, lnk) {
  if (typeof(data[0].val) == "function") {
    $(lnk).css({
      'left': $(data[0]).val() + '%',
      'top': $(data[1]).val() + '%',
      'width':$(data[2]).val() + '%',
      'height':$(data[3]).val() + '%'
    });
  } else {
    $(lnk).css({
      'left': data[0] + '%',
      'top':  data[1] + '%',
      'width':data[2] + '%',
      'height':data[3] + '%'
    });
  }
}

function updateData(data, lnk) {
  var x = $(lnk).position().left,
     y = $(lnk).position().top,
     w = $(lnk).width(),
     h = $(lnk).height();

  var cont = $(lnk).parent();

  x = (x / $(cont).width()) * 100;
  y = (y / $(cont).height()) * 100;
  w = (w / $(cont).width()) * 100;
  h = (h / $(cont).height()) * 100;

  $(data[0]).val(x.toFixed(2));
  $(data[1]).val(y.toFixed(2));
  $(data[2]).val(w.toFixed(2));
  $(data[3]).val(h.toFixed(2));

  drawLink(data, lnk);
}

function getData(mother) {
  return [
    $(mother).find('.field-x').find('input').first(),
    $(mother).find('.field-y').find('input').first(),
    $(mother).find('.field-width').find('input').first(),
    $(mother).find('.field-height').find('input').first()
  ];
}

function insertPreview(mother) {
  var href = $(getPreview()).first().attr('href');
  var cont = $(mother).find($(".preview.col1"));

  var img = new Image();
  img.onload = function () {
    var wrap = $('<div class="preview_img">').append(img).append('<div class="preview_glass">');

    var h = 340,
       w = $(cont).parent().width()/2;

    $(cont).parent().attr({
      'data-width': w,
      'data-height': h
    });

    $(wrap).height(h + "px");
    $(wrap).width(w + "px");
    $(cont).append(wrap);

    setSize($(img), $(wrap), $(cont).width(), $(cont).height());
    $(window).resize(function () {
      var h = 340,
       w = $(cont).parent().width()/2;

      if ((h == $(cont).parent().attr('data-height')) && (w == $(cont).parent().attr('data-width')))
        return;
      else {
        $(cont).parent().attr({
      'data-width': w,
      'data-height': h
    });
      }

      $(wrap).height(h + "px");
      $(wrap).width(w + "px");
      setSize($(img), $(wrap), $(cont).width(), $(cont).height());
    });
    initLink(getData(mother), $(wrap));
  };

  img.src = href;
}

function getPreview() {
  return $(".file-upload").find('a');
}

function setSize(img, cont, w, h) {
  $(cont).height(h);
  $(cont).width(w);
  var k = $(img),
      t = $(cont),
      nw = $(k).naturalWidth(),
      nh = $(k).naturalHeight(),
      wantedratio = nw / nh,
      actualratio = w / h;

  $(k).width('100%').height('100%');

  if (wantedratio >= actualratio) {
    $(t).height(w / wantedratio).width(w);
    $(k).height('');
  }
  else {
    $(t).height(h).width(h * wantedratio);
    $(k).width('');
  }
}
