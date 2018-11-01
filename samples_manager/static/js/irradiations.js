$(function () {
  var starting_sec = function(){
            get_sec();
        }

var nIntervId = null;
var in_beam_checked = 0;
var detected_change = false;

var in_beam_checkboxes = document.querySelectorAll('.in_beam_checkbox');
for(var i = 0; i < in_beam_checkboxes.length; i++) {
            if(in_beam_checkboxes[i].checked) {
                 in_beam_checked++;
            }
        };
if(0<in_beam_checked){
    console.log("in_beam_checked: ",in_beam_checked);
    nIntervId = setInterval(starting_sec, 5000);
}


var newGroupIrradiation = function (){
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
            $("#modal-irradiation").modal("show");
            $("#modal-irradiation .scrolling.content").html(data.html_form);
          }
          else {
            alert("We are sorry. Something went wrong.")
          }
        }
      });
      return false;
}

var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-irradiation").modal({
          closable:false,
          allowMultiple: true,
          onApprove : function() {
			    return false;
			  }
        }).modal("show");
      },
      success: function (data) {
        $("#modal-irradiation .scrolling.content").html(data.html_form);
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
          $("#irradiation-table tbody").html(data.html_irradiation_list);  // <-- Replace the table body
          $("#modal-irradiation").modal("hide");  // <-- Close the modals
          console.log(form.attr("data-url"));
          window.location.href =  form.attr("data-url");
            /*if(data.experiment_id != -1)
            samplesloadForm(data.experiment_id);*/
        }
        else {
          $("#modal-irradiation .scrolling.content").html(data.html_form);
          alert("Please, check the form and fill all the required fields!");
        }
      }
    });
    return false;
  };

/* var get_sec = function() {
      var form = $("#sec_form");
      $.ajax({
      url: form.attr("action"),
      data:  form.serialize(),
      type: 'post',
      dataType: 'json',
      success: function (data) {
        if (detected_change == false) {
          if (data.form_is_valid) {
              $("#irradiation-table tbody").html(data.html_irradiation_list);  // <-- Replace the table body
          }
          else {
          alert("data is not correct");
          }
        }
        else{
          console.log("detected_change",detected_change);
        }
      }
    });
  }*/

    var get_sec = function() {
            var form = $("#sec_form");
            if (detected_change == false) { 
              $.ajax({
              url: form.attr("action"),
              data:  form.serialize(),
              type: 'post',
              dataType: 'json',
              success: function (data) {
                if (detected_change == false) { 
                      if (data.form_is_valid) {
                          $("#irradiation-table tbody").html(data.html_irradiation_list);  // <-- Replace the table body
                          console.log("replacing data html_irradiation_list!");
                      }
                }
                else{
                    console.log("ignore answer data!");
                }
                  }
              });
            }
            else{
                console.log("detected_change!");
              }
        }

function getFormattedDate() {
    var date = new Date();
    var str = date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate() + " " +  date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds();
    return str;
}

 var downloadCSV = function(csv, filename) {
    var csvFile;
    var downloadLink;

    // CSV file
    csvFile = new Blob([csv], {type: "text/csv"});

    // Download link
    downloadLink = document.createElement("a");

    // File name
    downloadLink.download = filename;

    // Create a link to the file
    downloadLink.href = window.URL.createObjectURL(csvFile);

    // Hide download link
    downloadLink.style.display = "none";

    // Add the link to DOM
    document.body.appendChild(downloadLink);

    // Click download link
    downloadLink.click();
}

 var exportTableToCSV = function() {
    var csv = [];
    var filename = 'dosimetry_results.csv';
    var rows = document.querySelectorAll("table tr");
    
    for (var i = 0; i < rows.length; i++) {
        var row = [], cols = rows[i].querySelectorAll("td, th");
        
        for (var j = 0; j < cols.length; j++) 
            row.push(cols[j].innerText);
        
        csv.push(row.join(","));        
    }

    // Download CSV file
    downloadCSV(csv.join("\n"), filename);
}

var checkInBeamState = function(){
  console.log("check in beam state");
  var form = $("#sec_form");
  var btn = $("#in_beam_button_save");
    $.ajax({
              url: btn.attr("data-url"),
              data:  form.serialize(),
              type: 'post',
              dataType: 'json',
              success: function (data) {
                      console.log("spiting data!");
                      if (data.form_is_valid) {
                          console.log("data changed successfully");
                          $('#in_beam_button_save').hide();
                          $('#cancel_button').hide();
                          $('#select_table_form').show();
                          $('#back_button').show();
                          $('#irradiation_new_div').show();
                          in_beam_checked = data['in_beam_checked']
                          if(0<in_beam_checked){
                            console.log("in_beam_checked!=0 setting interval");
                            console.log(in_beam_checked);
                            nIntervId = setInterval(starting_sec, 5000);
                                          }
                          else{
                            console.log("in beam checked");
                            console.log(in_beam_checked);
                            clearInterval(nIntervId);
                          }
                          detected_change = false;
                          }
                      }
            });
}

var cancelButton = function(){
            var form = $("#sec_form");
            $.ajax({
              url: form.attr("action"),
              data:  form.serialize(),
              type: 'post',
              dataType: 'json',
              success: function (data) {
                      if (data.form_is_valid) {
                          $("#irradiation-table tbody").html(data.html_irradiation_list);  // <-- Replace the table body
                          console.log("replacing data html_irradiation_list!");
                          if (0<data["in_beam_checked"]){
                            setInterval(nIntervId);
                          }
                          else{
                            clearInterval(nIntervId);
                          }
                          $('#in_beam_button_save').hide();
                          $('#cancel_button').hide();
                          $('#select_table_form').show();
                          $('#back_button').show();
                          $('#irradiation_new_div').show();
                      }
                  }
              });
}


//New irradiation
  $("#new_group_irradiation").on("click",newGroupIrradiation);
  $("#irradiation_new").on("click",loadForm);
  $("#modal-irradiation").on("submit", ".js-irradiation-form",saveForm);

// Update irradiation
  $("#irradiation-table").on("click", ".js-update-irradiation", loadForm);
  $("#modal-irradiation").on("submit", ".js-irradiation-update-form",saveForm);

// delete irradiation
  $("#irradiation-table").on("click", ".js-delete-irradiation", loadForm);
  $("#modal-irradiation").on("submit", ".js-irradiation-delete-form", saveForm);

  //update irradiation status
  $("#irradiation-table").on("click", ".js-change-irradiation-status", loadForm);
  $("#modal-irradiation").on("submit", ".js-irradiation-update-form", saveForm);

  // get sec
  //$("#get_sec").on("click",starting_sec);

   $("#export_button").on("click", exportTableToCSV);

   $("body").on("click","#in_beam_button_save",checkInBeamState);
   $("body").on("click","#cancel_button",cancelButton);

   $("body").on("change", ".in_beam_checkbox", function(){
      console.log("triggering in change clear interval!");
      detected_change = true;
      clearInterval(nIntervId);
      $('#in_beam_button_save').show();
      $('#cancel_button').show();
      $('#select_table_form').hide();
      $('#back_button').hide();
      $('#irradiation_new_div').hide();
  });
  
});

document.addEventListener('touchstart', handler, {passive: true});
