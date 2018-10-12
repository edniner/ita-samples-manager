$(function () {

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

  var get_sec = function(timestamp) {
      console.log("get sec",timestamp);
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

var starting_sec = function(){
  // the task stops after refreshing to be thought!
  var nIntervId;
  if (document.getElementById("get_sec").value=="Get SEC"){
      document.getElementById("get_sec").value = "Stop SEC";
      timestamp = getFormattedDate();
      document.getElementById("start_timestamp").value = timestamp;
      nIntervId = setInterval(get_sec, 5000, timestamp);
      document.getElementById("get_sec").classList.add('red');
      document.getElementById("get_sec").classList.remove('orange');
      
   }
  else{ 
     document.getElementById("get_sec").value = "Get SEC";
     document.getElementById("get_sec").classList.add('orange');
     document.getElementById("get_sec").classList.remove('red');
     clearInterval(nIntervId);
   }

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
  $("#get_sec").on("click",starting_sec);

   $("#export_button").on("click", exportTableToCSV);
});