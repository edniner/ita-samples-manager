$(function () {

var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-box").modal("show");
      },
      success: function (data) {
        $("#modal-box .modal-content").html(data.html_form);
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
          $("#data-table tbody").html(data.html_box_list);  // <-- Replace the table body
          $("#modal-box").modal("hide");  // <-- Close the modal
        }
        else {
          alert("Something went wrong!");  // <-- This is just a placeholder for now for testing
          $("#modal-box .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

  // Create box
  $(".js-create-box").click(loadForm);
  $("#modal-box").on("submit", ".js-box-create-form",saveForm );

   // Update box
  $("#data-table").on("click", ".js-update-box", loadForm);
  $("#modal-box").on("submit", ".js-box-update-form", saveForm);

    //Clone box
  $("#data-table").on("click", ".js-clone-box", loadForm);

  // Delete book
  $("#data-table").on("click", ".js-delete-box", loadForm);
  $("#modal-box").on("submit", ".js-box-delete-form", saveForm);



});