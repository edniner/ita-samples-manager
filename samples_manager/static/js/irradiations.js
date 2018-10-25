$(function () {
  var starting_sec = function(){
            get_sec();
        }

  var get_sec = function() {
            var form = $("#sec_form");
            $.ajax({
            url: form.attr("action"),
            data:  form.serialize(),
            type: 'post',
            dataType: 'json',
            success: function (data) {
                    if (data.form_is_valid) {
                        $("#irradiation-table tbody").html(data.html_irradiation_list);  // <-- Replace the table body
                    }
                }
            });
        }
var nIntervId;
var in_beam_checked = 0;

var in_beam_checkboxes = document.querySelectorAll('.in_beam_checkbox');
for(var i = 0; i < in_beam_checkboxes.length; i++) {
            if(in_beam_checkboxes[i].checked) {
                 in_beam_checked++;
            }
        };
if(in_beam_checked!=0){
    console.log("in_beam_checked: ",in_beam_checked);
    //nIntervId = setInterval(starting_sec, 5000);
}

$('.in_beam_checkbox').change(function() {
            clearInterval(nIntervId);
            console.log("clear interval!");
            $('#in_beam_button_save').show();
            $('#back_button').hide();
            $('#irradiation_new').hide();
        });

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

  var get_sec = function() {
      var form = $("#sec_form");
      $.ajax({
      url: form.attr("action"),
      data:  form.serialize(),
      type: 'post',
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
            $("#irradiation-table tbody").html(data.html_irradiation_list);  // <-- Replace the table body
        }
        else {
         alert("data is not correct");
        }
      }
    });
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
  var form = $("#sec_form");
  $(".in_beam_checkbox").each(function() {
      if (this.defaultChecked !== this.checked) {
                var input = this;
                if (this.checked){
                  modified_url = input.value +"in/";
                  console.log(modified_url);
                  in_beam_checked++;
                }
                else{
                  modified_url = input.value +"out/";
                  console.log(modified_url);
                  in_beam_checked--;
              } 
               $.ajax({
                url: modified_url,
                data:  form.serialize(),
                type: 'post',
                dataType: 'json',
                success: function (data) {
                  if (data.form_is_valid) {
                      $("#irradiation-table tbody").html(data.html_irradiation_list);  // <-- Replace the table body
                      }
                    }
                  });
                }
    });
  if(in_beam_checked!=0){
    console.log("in beam");
    nIntervId = setInterval(starting_sec, 5000);
                  }
  $('#in_beam_button_save').hide();
  $('#back_button').show();
  $('#irradiation_new').show();
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

   $("#in_beam_button_save").on("click",checkInBeamState);

   });

