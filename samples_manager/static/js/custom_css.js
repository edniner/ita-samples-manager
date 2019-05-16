function createCookie(key, value, date,path) {
        var expiration = new Date(date).toUTCString();
        var cookie = escape(key) + "=" + escape(value) + ";expires=" + expiration + ";path="+ path+";";
        document.cookie = cookie;
    }      

function readCookie(name) {
    	var key = name + "=";
    	var cookies = document.cookie.split(';');
    	for (var i = 0; i < cookies.length; i++) {
    		var cookie = cookies[i];
    		while (cookie.charAt(0) === ' ') {
                cookie = cookie.substring(1, cookie.length);
            }
    		if (cookie.indexOf(key) === 0) {
                return cookie.substring(key.length, cookie.length);
            }
    	}
    	return null;
    }

function getColor(color_string){
        var hex_value1 = color_string.slice(3,9);
        hex_value = "#"+hex_value1;
        return hex_value;
}
   
    $(document).ready(function(){


    if (readCookie("body_bgk")){
            body_bgk = getColor(readCookie("body_bgk"));
            $('body.pushable > .pusher').css('background-color',body_bgk);
        }

    if (readCookie("segment_bgk")){
            segment_bgk = getColor(readCookie("segment_bgk"));
            $('div.ui.segment').css('background-color',segment_bgk);
        }

    if (readCookie("table_bgk")){
            table_bgk = getColor(readCookie("table_bgk"));
            $('table#data-table.ui.center.aligned.sortable.celled.table').css('background-color',table_bgk);
            $('#data-table th').css('background-color',table_bgk);
        }

    if (readCookie("table_font_color")){
            table_font_color = getColor(readCookie("table_font_color"));
            $('table#data-table.ui.center.aligned.sortable.celled.table').css('color',table_font_color);
            $('#data-table th').css('color',table_font_color);
            $('p').css('color',table_font_color);
            $('h1').css('color',table_font_color);
            $('h2').css('color',table_font_color);
        }

     if (readCookie("link_color")){
            link_color = getColor(readCookie("link_color"));
            $('a').css('color',link_color);
        }

    if (readCookie("font_size")){
            pix_txt = readCookie("font_size");
            $('table#data-table.ui.center.aligned.sortable.celled.table').css('font-size',pix_txt);
            $('#data-table th').css('font-size',pix_txt);
            $('p').css('font-size',pix_txt);
        }

    $("#body_bgk").change(function(){
         var selectedBGD = $(this).val();
         $('body.pushable > .pusher').css('background-color',selectedBGD);
         createCookie("body_bgk", selectedBGD, Date.UTC(2020, 5, 10), "/");
    });
    $("#segment_bgk").change(function(){
         var selectedBGD = $(this).val();
         $('div.ui.segment').css('background-color',selectedBGD);
         createCookie("segment_bgk", selectedBGD, Date.UTC(2020, 5, 10), "/");
    });
    $("#table_bgk").change(function(){
         var selectedBGD = $(this).val();
         $('table#data-table.ui.center.aligned.sortable.celled.table').css('background-color',selectedBGD);
         $('#data-table th').css('background-color',selectedBGD);
         createCookie("table_bgk", selectedBGD, Date.UTC(2020, 5, 10), "/");
    });
    $("#table_font_color").change(function(){
         var selectedBGD = $(this).val();
         $('table#data-table.ui.center.aligned.sortable.celled.table').css('color',selectedBGD);
         $('#data-table th').css('color',selectedBGD);
         $('p').css('color',selectedBGD);
         $('h1').css('color',selectedBGD);
         $('h2').css('color',selectedBGD);
         createCookie("table_font_color", selectedBGD, Date.UTC(2020, 5, 10), "/");
    });
    $("#font_size").change(function(){
         var pixels = $(this).val();
         var pix_txt = pixels + "px";
         createCookie("font_size",pix_txt, Date.UTC(2020, 5, 10), "/");
         $('table#data-table.ui.center.aligned.sortable.celled.table').css('font-size',pix_txt);
         $('#data-table th').css('font-size',pix_txt);
         $('p').css('font-size',pix_txt);
    });
    $("#link_color").change(function(){
         var selectedBGD = $(this).val();
         $('a').css('color',selectedBGD);
         createCookie("link_color", selectedBGD, Date.UTC(2020, 5, 10), "/");
    });

    var body_bgk = $('body.pushable > .pusher').css('background-color');
    var segment_bgk = $('div.ui.segment').css('background-color');
    var table_bgk = $('table#data-table.ui.center.aligned.sortable.celled.table').css('background-color');
    var table_font_color = $('table#data-table.ui.center.aligned.sortable.celled.table').css('color');
    var link_color= $('a').css('color');
    var pix_txt= $('table#data-table.ui.center.aligned.sortable.celled.table').css('font-size');
    
    var pix = pix_txt.slice(0,2);
    console.log(pix);
    $("#font_size").val(pix);
    $("#body_bgk").spectrum({
                    preferredFormat: "hex",
                    showInitial: true,
                    showInput: true,
                    showPalette: true,
                    clickoutFiresChange: true,
                    color: body_bgk
                });

                $("#segment_bgk").spectrum({
                    preferredFormat: "hex",
                    showInitial: true,
                    showInput: true,
                    showPalette: true,
                    clickoutFiresChange: true,
                    color: segment_bgk
                });
                $("#table_bgk").spectrum({
                    preferredFormat: "hex",
                    showInitial: true,
                    showInput: true,
                    showPalette: true,
                    clickoutFiresChange: true,
                    color: table_bgk
                });
                $("#table_font_color").spectrum({
                    preferredFormat: "hex",
                    showInitial: true,
                    showInput: true,
                    showPalette: true,
                    clickoutFiresChange: true,
                    color: table_font_color
                });
                $("#link_color").spectrum({
                    preferredFormat: "hex",
                    showInitial: true,
                    showInput: true,
                    showPalette: true,
                    clickoutFiresChange: true,
                    color: link_color
                });
   /* $("select.container_bgd").change(function(){
         var selectedBGD = $(this).children("option:selected").val();
         $('div.ui.container').css('background-color',selectedBGD);
    });*/

});