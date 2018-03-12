$(function () {

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

  var saveForm = function () {
    console.log("In the save form");
    var form = $(this);
    console.log(form);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        console.log("Success");
        console.log(data);
        if (data.form_is_valid) {
          $("#dosimeter-table tbody").html(data.html_dosimeter_list);  // <-- Replace the table body
          $("#modal-dosimeter").modal("hide");  // <-- Close the modal
        }
        else {
          alert("Something went wrong!");  // <-- This is just a placeholder for now for testing
          $("#modal-dosimeter .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

  // Create dosimeter
  $(".js-create-dosimeter").click(loadForm);
  $("#modal-dosimeter").on("submit", ".js-dosimeter-create-form",saveForm );

   // Update dosimeter
  $("#dosimeter-table").on("click", ".js-update-dosimeter", loadForm);
  $("#modal-dosimeter").on("submit", ".js-dosimeter-update-form", saveForm);

    //Clone dosimeter
  $("#dosimeter-table").on("click", ".js-clone-dosimeter", loadForm);

  // Delete book
  $("#dosimeter-table").on("click", ".js-delete-dosimeter", loadForm);
  $("#modal-dosimeter").on("submit", ".js-dosimeter-delete-form", saveForm);



});