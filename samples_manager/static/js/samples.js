$(function () {

var loadForm = function () {
    var btn = $(this);
    console.log("samples loadForm")
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
          $("#sample-table tbody").html(data.html_sample_list);  // <-- Replace the table body
          $("#modal-sample").modal("hide");  // <-- Close the modal
            /*if(data.experiment_id != -1)
            samplesloadForm(data.experiment_id);*/
        }
        else {
          //alert("Something went wrong!");  // <-- This is just a placeholder for now for testing
          $("#modal-sample .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

  var samplesloadForm = function (experiment_id) {
    var btn = $(this);
    console.log("samples loadForm");
    link = 'experiment/'+experiment_id+'/sample/new/';
    console.log(link);
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



});