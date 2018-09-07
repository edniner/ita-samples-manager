$(function () {

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

//New irradiation
  $("#new_irradiation").on("click",new_irradiation);
  $("#modal-sample").on("submit", ".js-assign-dosimeters-form",saveForm);
});