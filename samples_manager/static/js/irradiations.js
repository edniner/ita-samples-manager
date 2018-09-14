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
            $("#modal-irradiation .modal-content").html(data.html_form);
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
        $("#modal-irradiation").modal("show");
      },
      success: function (data) {
        $("#modal-irradiation .modal-content").html(data.html_form);
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
          $("#modal-irradiation").modal("hide");  // <-- Close the modal
          window.location.href =  form.attr("data-url");
            /*if(data.experiment_id != -1)
            samplesloadForm(data.experiment_id);*/
        }
        else {
          $("#modal-irradiation .modal-content").html(data.html_form);
          alert("Please, check the form and fill all the required fields!");
        }
      }
    });
    return false;
  };

//New irradiation
  $("#new_group_irradiation").on("click",newGroupIrradiation);
  $("#irradiation_new").on("click",loadForm);
  $("#modal-irradiation").on("submit", ".js-irradiation-form",saveForm);

// Update irradiation
  $("#irradiation-table").on("click", ".js-update-irradiation", loadForm);
  $("#modal-irradiation").on("submit", ".js-irradiation-update-form",saveForm);
});