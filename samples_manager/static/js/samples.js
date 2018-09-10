var activate_hidden_buttons = function() {
        $('#new_sample').hide();
        $('#print_samples').show();
        $('#assign_ids').show();
        $('#assign_dosimeters').show();
        $('#id_experiments').show();
        $('#change_experiment').show();
        $('#new_irradiation').show();
  }
var disactivate_hidden_buttons = function(){
        $('#new_sample').show();
        $('#print_samples').hide();
        $('#assign_ids').hide();
        $('#assign_dosimeters').hide();
        $('#id_experiments').hide();
        $('#change_experiment').hide();
        $('#new_irradiation').hide();
  }

$(function () {
  checked_sample_values = 0;

  $('.chkbox').change(function() {
    /*if(this.checked) {
            alert($(this).val());
        }   */ 


    if (this.checked){
        checked_sample_values = checked_sample_values + 1;
        activate_hidden_buttons();
      } 
    else{
      checked_sample_values = checked_sample_values - 1;
      if (checked_sample_values == 0){
        disactivate_hidden_buttons();
      }
    }
  });

  
var load_values = function() {
  checked_sample_values = 0;
  $("#samples-select-all").prop("checked", false);
  $('.chkbox').change(function() {
    if (this.checked){
        checked_sample_values = checked_sample_values + 1;
        activate_hidden_buttons();
      } 
    else{
      checked_sample_values = checked_sample_values - 1;
      if (checked_sample_values == 0){
        disactivate_hidden_buttons();
      }
    }
  });  

$("#samples-select-all").click(function(){
    $('.chkbox').not(this).prop('checked', this.checked);
        if (this.checked){
        checked_sample_values = checked_sample_values + 1;
        activate_hidden_buttons();
      } 
    else{
      checked_sample_values = checked_sample_values - 1;
      if (checked_sample_values == 0){
        console.log("nothing check!");
        disactivate_hidden_buttons();
      }
    }
  });
}

load_values();  


var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-sample").modal("show");
      },
      success: function (data) {
        $("#modal-sample .modal-content").html(data.html_form);
      }
    });
  };


 var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          if(data['state']=='Created')
            alert("Your sample was successfully saved!")
          else if (data['state']=='Updated')
            alert("Your sample was successfully updated!")
          else if (data['state']=='Deleted')
            alert("The sample was deleted!")
          $("#sample-table tbody").html(data.html_sample_list);  // <-- Replace the table body
          $("#modal-sample").modal("hide");  // <-- Close the modal
            /*if(data.experiment_id != -1)
            samplesloadForm(data.experiment_id);*/
        }
        else {
          $("#modal-sample .modal-content").html(data.html_form);
          if(data['state']=='not unique')
            alert("This name already exists! Please, choose a different name.");
          else if (data['state']=='layers missing')
            alert("Please, fill the layers fields!")
          else
            alert("Please, check the form and fill all the required fields!");
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
                  $("#modal-sample").modal("hide");  // <-- Close the modal
                  var text = '<html><head><title>'+data['set_id']+'</title></head><body onafterprint="self.close()"><h1 style ="text-align: center; font-size:350%; margin:0">'+data['set_id'] +'</h1>';
                  text = text+ '<h2 style = "text-align:center; margin:0">'+data['category'] +'<br>'+data['req_fluence'] +'<br>'+data['responsible'] +'<br>'+data['sample_name']+'</h2></body></html>';
                  my_window = window.open('', 'mywindow', 'status=1,width=300,height=300');
                  my_window.document.write(text);
                  my_window.document.close();
                  $("#sample-table tbody").html(data.html_sample_list);  // <-- Replace the table body
                  load_values();
              }
          });
          console.log("false")
          return false;
  }


var dymoPrintSamples = function(){
            console.log('sample print dymo');
            var val = [];
            checked_samples = [];
            $('.chkbox:checked').each(function(i){
                checked_samples[i] = $(this).val();
            });
            try
            {
            var labelXml = '<?xml version="1.0" encoding="utf-8"?>\
                                <DieCutLabel Version="8.0" Units="twips" MediaType="Default">\
                                    <PaperOrientation>Portrait</PaperOrientation>\
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
                                        <Bounds X="82" Y="144" Width="1301" Height="1210" />\
                                    </ObjectInfo>\
                            </DieCutLabel>';


                var label = dymo.label.framework.openLabelXml(labelXml);
                console.log(label);

                // create label set to print data
                var labelSetBuilder = new dymo.label.framework.LabelSetBuilder();
                var i;
                var textMarkup = '';
                for (i = 0; i <checked_samples.length; i++) { 
                    textMarkup = '<b><font family="Arial" size="18">'+checked_samples[i];
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

                $('.chkbox:checked').removeAttr('checked');
                checked_sample_values = 0;
                $('#new_sample').show();
                $('#print_samples').hide();
                $('#assign_ids').hide();
                load_values();
            }
            catch(e)
            {
                alert(e.message || e);
            }
        }

  var samplesloadForm = function (experiment_id) {
    var btn = $(this);
    link = 'experiment/'+experiment_id+'/sample/new/';
    $.ajax({
      url:link,
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-sample").modal("show");
      },
      success: function (data) {
        $("#modal-sample .modal-content").html(data.html_form);
      }
    });
  };

var assignids = function () {
    var r = confirm("Allocating SET-ID means that your samples are ready to be irradiated. Please, proceed only if you are sure.")
    if(r == true) {
      var btn = $(this);
      var form = $('#assign_samples_dosimeter');
      $.ajax({
        url: btn.attr("data-url"),
        data:  form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
          if (data.form_is_valid) {
            $("#sample-table tbody").html(data.html_sample_list);  // <-- Replace the table body
            $('.chkbox:checked').removeAttr('checked');
            checked_sample_values = 0;
            $('#new_sample').show();
            $('#print_samples').hide();
            $('#assign_ids').hide();
            load_values();
          }
          else {
            alert("We are sorry. Something went wrong.")
          }
        }
      });
    }
    else{
        $('.chkbox:checked').removeAttr('checked');
        checked_sample_values = 0;
        $('#new_sample').show();
        $('#print_samples').hide();
        $('#assign_ids').hide();
        load_values();
    }
    return false;

  };

  var assignids = function () {
    var r = confirm("Allocating SET-ID means that your samples are ready to be irradiated. Please, proceed only if you are sure.")
    if(r == true) {
      var btn = $(this);
      var form = $('#move_samples');
      $.ajax({
        url: btn.attr("data-url"),
        data:  form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
          if (data.form_is_valid) {
            $("#sample-table tbody").html(data.html_sample_list);  // <-- Replace the table body
            $('.chkbox:checked').removeAttr('checked');
            checked_sample_values = 0;
            load_values();
          }
          else {
            alert("We are sorry. Something went wrong.")
          }
        }
      });
    }
    else{
        $('.chkbox:checked').removeAttr('checked');
        checked_sample_values = 0;
        load_values();
    }
    return false;
  };

var move_samples = function (){
      console.log("move_samples")
      var btn = $(this);
      var form = $('#move_samples');
      $.ajax({
        url: btn.attr("data-url"),
        data:  form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
          if (data.form_is_valid) {
            $("#sample-table tbody").html(data.html_sample_list);  // <-- Replace the table body
            $('.chkbox:checked').removeAttr('checked');
            checked_sample_values = 0;
            disactivate_hidden_buttons();
            load_values();
            console.log("returning data")
          }
          else {
            alert("We are sorry. Something went wrong.")
          }
        }
      });
      return false;
}

var new_irradiation = function (){
      console.log("new_irradiation")
      var btn = $(this);
      var form = $('#move_samples');
      $.ajax({
        url: btn.attr("data-url"),
        data:  form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
          if (data.request_valid) {
            console.log("request valid")
            $('.chkbox:checked').removeAttr('checked');
            checked_sample_values = 0;
            //disactivate_hidden_buttons();
            //load_values();
            $("#modal-sample").modal("show");
            $("#modal-sample .modal-content").html(data.html_form);
          }
          else {
            alert("We are sorry. Something went wrong.")
          }
        }
      });
      return false;
}



  // Create sample
  $(".js-create-sample").click(loadForm);
  //$("#assign_dosimeters").on("submit", ".js-assign-dosimeters-form",assign_dosimeters);

  $('#assign_dosimeters').click( function() { alert('A Sample-ID will be generated for the samples that they do not have one.');});

  $("#modal-sample").on("submit", ".js-sample-create-form",saveForm);

   // Update sample
  $("#sample-table").on("click", ".js-update-sample", loadForm);
  $("#modal-sample").on("submit", ".js-sample-update-form",saveForm);

    //Clone sample
  $("#sample-table").on("click", ".js-clone-sample", loadForm);

  // Delete book
  $("#sample-table").on("click", ".js-delete-sample", loadForm);
  $("#modal-sample").on("submit", ".js-sample-delete-form", saveForm);

  // Print label
  $("#sample-table").on("click", ".js-print-sample-label", loadForm);
  $("#modal-sample").on("submit", ".js-print-sample-label-form", printLabel);
  $("#print_samples").on("click",dymoPrintSamples);
  //Assign SET_IDs
  $("#assign_ids").on("click",assignids);
  //Move samples
  $("#change_experiment").on("click",move_samples);
});
