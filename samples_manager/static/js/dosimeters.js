$(function () {

  checked_values = 0;
  var text1 = "text1";
  var text2 = "text2";
  var printButton = document.getElementById('printButton');

  $('.chk').change(function() {
    /*if(this.checked) {
            alert($(this).val());
        }   */ 
    if (this.checked){
        checked_values = checked_values + 1;
        $('#new_dos').hide();
        $('#print_dos').show();
        $('#generate_dos').hide();
      } 
    else{
      checked_values = checked_values - 1;
      if (checked_values == 0){
        $('#new_dos').show();
        $('#print_dos').hide();
        $('#generate_dos').show();
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
        $("#modal-dosimeter").modal("show");
      },
      success: function (data) {
        $("#modal-dosimeter .modal-content").html(data.html_form);
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
        $("#modal-dosimeter").modal("show");
      },
      success: function (data) {
        $("#modal-dosimeter .modal-content").html(data.html_form);
      }
    });
  };

  var dymoPrint = function(){
            var val = [];
            checked_dosimeters = [] 
            $('.chk:checked').each(function(i){
                checked_dosimeters[i] = $(this).val();
            });
            console.log(checked_dosimeters);
            try
            {
            console.log("dymo print");
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

                // create label set to print data
                var labelSetBuilder = new dymo.label.framework.LabelSetBuilder();

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
                    throw "No DYMO printers are installed. Install DYMO printers.";

                var printerName = "DYMO LabelWriter 450 Turbo";
                
                if (printerName == "")
                    throw "No LabelWriter printers found. Install LabelWriter printer";

                // finally print the label with default print params
                label.print(printerName, "", labelSetBuilder);
                $('.chk:checked').removeAttr('checked');
                checked_values = 0;
                $('#new_dos').show();
                $('#print_dos').hide();
                $('#generate_dos').show();
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
        if (data.form_is_valid) {
          alert("data is valid");
          $("#dosimeter-table tbody").html(data.html_dosimeter_list);  // <-- Replace the table body
          $("#modal-dosimeter").modal("hide");  // <-- Close the modal
        }
        else {
          alert("Something went wrong!"); 
          $("#modal-dosimeter .modal-content").html(data.html_form);
        }
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
                  $("#dosimeter-table tbody").html(data.html_dosimeter_list);  // <-- Replace the table body
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
  $("#dosimeter-table").on("click", ".js-update-dosimeter", loadForm);
  $("#modal-dosimeter").on("submit", ".js-dosimeter-update-form", saveForm);

    //Clone dosimeter
  $("#dosimeter-table").on("click", ".js-clone-dosimeter", loadForm);

  // Delete dosimeter
  $("#dosimeter-table").on("click", ".js-delete-dosimeter", loadForm);
  $("#modal-dosimeter").on("submit", ".js-dosimeter-delete-form", saveForm);

  // Print label
  $("#dosimeter-table").on("click", ".js-print-dosimeter-label", loadForm);
  $("#modal-dosimeter").on("submit", ".js-print-dosimeter-label-form", printLabel);
  $("#print_dos").click(dymoPrint);
  
});
