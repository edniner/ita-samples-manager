$(function () {

  
var load_values = function() {
  checked_values = 0;
  $("#dosimeters-select-all").prop("checked", false);
  $('input.chk').change(function() {
    if (this.checked){
        checked_values = checked_values + 1;
        $('#unchecked_segment').hide();
        $('#checked_segment').show();
      } 
    else{
      checked_values = checked_values - 1;
      if (checked_values == 0){
        $('#unchecked_segment').show();
        $('#checked_segment').hide();
      }
    }
  });  

$("#dosimeters-select-all").click(function(){
    $('.chk').not(this).prop('checked', this.checked);
    if (this.checked){
              checked_values = checked_values + 1;
              $('#unchecked_segment').hide();
              $('#checked_segment').show();
            } 
          else{
            checked_values = checked_values - 1;
            if (checked_values == 0){
              $('#unchecked_segment').show();
              $('#checked_segment').hide();
            }
          }  
});
}

load_values();  

$("#dosimeters-select-all").click(function(){
    $('.chk').not(this).prop('checked', this.checked);
    if (this.checked){
              checked_values = checked_values + 1;
              $('#unchecked_segment').hide();
              $('#checked_segment').show();
            } 
          else{
            checked_values = checked_values - 1;
            if (checked_values == 0){
              $('#unchecked_segment').show();
              $('#checked_segment').hide();
            }
          }  
}); 
  
var  generate_ids = function () {
    console.log("generate");
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-dosimeter").modal({
          closable:false,
          onApprove : function() {
			    return false;
			  }
        }).modal("show");
      },
      success: function (data) {
        $("#modal-dosimeter .scrolling.content").html(data.html_form);
      }
    });
  };

var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-dosimeter").modal({
          closable:false,
          onApprove : function() {
			    return false;
			  }
        }).modal("show");
      },
      success: function (data) {
        $("#modal-dosimeter .scrolling.content").html(data.html_form);
      }
    });
  };

  var dymoPrint = function(){
            console.log("dymo print");
            var val = [];
            checked_dosimeters = []; 
            $('.chk:checked').each(function(i){
                checked_dosimeters[i] = $(this).val();
            });
            console.log(checked_dosimeters);
            try
            {
            var labelXml = '<?xml version="1.0" encoding="utf-8"?>\
                                <DieCutLabel Version="8.0" Units="twips" MediaType="Default">\
                                    <PaperOrientation>Landscape</PaperOrientation>\
                                    <Id>Small30332</Id>\
                                    <IsOutlined>false</IsOutlined>\
                                    <PaperName>30332 1 in x 1 in</PaperName>\
                                    <DrawCommands>\
                                        <RoundRectangle X="0" Y="0" Width="1440" Height="1440" Rx="180" Ry="180" />\
                                    </DrawCommands>\
                                    <ObjectInfo>\
                                        <TextObject>\
                                            <Name>Text</Name>\
                                            <ForeColor Alpha="255" Red="0" Green="0" Blue="0" />\
                                            <BackColor Alpha="0" Red="255" Green="255" Blue="255" />\
                                            <LinkedObjectName />\
                                            <Rotation>Rotation0</Rotation>\
                                            <IsMirrored>False</IsMirrored>\
                                            <IsVariable>True</IsVariable>\
                                            <GroupID>-1</GroupID>\
                                            <IsOutlined>False</IsOutlined>\
                                            <HorizontalAlignment>Center</HorizontalAlignment>\
                                            <VerticalAlignment>Middle</VerticalAlignment>\
                                            <TextFitMode>ShrinkToFit</TextFitMode>\
                                            <UseFullFontHeight>True</UseFullFontHeight>\
                                            <Verticalized>False</Verticalized>\
                                            <StyledText/>\
                                            </TextObject>\
                                        <Bounds X="144" Y="57" Width="1207.55907325383" Height="1298.26773603346" />\
                                    </ObjectInfo>\
                            </DieCutLabel>';

                var label = dymo.label.framework.openLabelXml(labelXml);
                console.log(label);
                // create label set to print data
                var labelSetBuilder = new dymo.label.framework.LabelSetBuilder();
                console.log(labelSetBuilder);
                var i;
                var textMarkup = '';
                for (i = 0; i <checked_dosimeters.length; i++) { 
                    textMarkup = '<b>'+checked_dosimeters[i]+'<br/>';
                    textMarkup += 'IRRAD';
                    console.log(textMarkup);
                    var record = labelSetBuilder.addRecord();
                    record.setTextMarkup('Text', textMarkup);
                }
                
                // select printer to print on
                // for simplicity sake just use the first LabelWriter printer
                var printers = dymo.label.framework.getPrinters();
                
                if (printers.length == 0)
                    alert("No DYMO printers are installed. Install DYMO printers.");
                else{
                      var printerName = "IRRAD SM Label Printer";
                      if (printerName == "")
                          throw "No LabelWriter printers found. Install LabelWriter printer";
                      
                      // finally print the label with default print params
                      if (printers[0].isConnected){
                        console.log("in the print");
                        label.print(printerName, "", labelSetBuilder);
                        }
                      else
                        alert('No Dymo printer connected!')
                }
                $('.chk:checked').removeAttr('checked');
                $('#unchecked_segment').show();
                $('#checked_segment').hide();
                checked_values = 0;
                load_values();    
            }
            catch(e)
            {
                alert(e.message || e);
            }
        }


  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        console.log("data returned successfully");
        if (data.form_is_valid) {
          $("#data-table tbody").html(data.html_dosimeter_list);  // <-- Replace the table body
          $("#modal-dosimeter").modal("hide");  // <-- Close the modal
          checked_values = 0;
          $('#unchecked_segment').show();
          $('#checked_segment').hide();
        }
        else {
          alert("Something went wrong!"); 
          $("#modal-dosimeter .modal-content").html(data.html_form);
        }
        load_values();
      }
    });
    return false;
  };

  var printLabel = function (){
          var form = $(this);
          $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                  $("#modal-dosimeter").modal("hide");  // <-- Close the modal
                  var text = '<html><head><title>'+data['dos_id']+'</title></head><body onafterprint="self.close()"><h1 style ="text-align: center; font-size:350%; margin:0">'+data['dos_id'] + '<h1 style ="text-align: center; margin:0">'+data['dos_type'] +'</h1>';
                  text = text+ '<h2 style = "text-align:center; margin:0">IRRAD</h2></body></html>';
                  my_window = window.open('', 'mywindow', 'status=1,width=350,height=300');
                  my_window.document.write(text);
                  my_window.document.close();
                  $("#data-table tbody").html(data.html_dosimeter_list);  // <-- Replace the table body
                  load_values();
              }
          });
          return false;
  }

  // Create dosimeter
  $(".js-create-dosimeter").click(loadForm);

  $("#generate_dos").click(generate_ids);
  $("#modal-dosimeter").on("submit", ".js-generate-ids-form", saveForm);

  $("#modal-dosimeter").on("submit", ".js-dosimeter-create-form",saveForm );

   // Update dosimeter
  $("#data-table").on("click", ".js-update-dosimeter", loadForm);
  $("#modal-dosimeter").on("submit", ".js-dosimeter-update-form", saveForm);

    //Clone dosimeter
  $("#data-table").on("click", ".js-clone-dosimeter", loadForm);

  // Delete dosimeter
  $("#data-table").on("click", ".js-delete-dosimeter", loadForm);
  $("#modal-dosimeter").on("submit", ".js-dosimeter-delete-form", saveForm);

  // Print label
  $("#data-table").on("click", ".js-print-dosimeter-label", loadForm);
  $("#modal-dosimeter").on("submit", ".js-print-dosimeter-label-form", printLabel);
  $("#print_dos").click(dymoPrint);
      
});
