$(function () {

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
          //alert("Something went wrong!");  // <-- This is just a placeholder for now for testing
          $("#modal-sample .modal-content").html(data.html_form);
          alert("Please, check the form and fill all the required fields!");
        }
      }
    });
    return false;
  };

    var printLabel = function (){
          alert("To print an IRRAD label you need to have a DYMO LabelWriter. Ctrl+P to print the label.")
          var btn = $(this);
          $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            success: function (data) {
                  console.log(data);
                  var text = '<html><head><title>'+data['set_id']+'</title></head><body"><h1 style ="text-align: center; font-size:300%;">'+data['set_id'] +'</h1><h2 style ="text-align: center;">'+data['req_fluence'] +'</h2><h2 style ="text-align: center;">'+data['category'] +'</h2></body></html>';
                  my_window = window.open('', 'mywindow', 'status=1,width=300,height=300');
                  my_window.document.write(text);
                  my_window.document.close();
                  $("#sample-table tbody").html(data.html_sample_list);  // <-- Replace the table body
              }
          });
          console.log("false")
          return false;
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



  // Create sample
  $(".js-create-sample").click(loadForm);
  $("#modal-sample").on("submit", ".js-sample-create-form",saveForm);

   // Update sample
  $("#sample-table").on("click", ".js-update-sample", loadForm);
  $("#modal-sample").on("submit", ".js-sample-update-form",saveForm);

    //Clone sample
  $("#sample-table").on("click", ".js-clone-sample", loadForm);

  // Delete book
  $("#sample-table").on("click", ".js-delete-sample", loadForm);
  $("#modal-sample").on("submit", ".js-sample-delete-form", saveForm);

  $("#sample-table").on("click", ".js-print-sample-label", printLabel);



});