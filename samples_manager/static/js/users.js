$(function () {
console.log("inside");
var loadForm = function () {
  console.log("loading form");
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-user").modal("show");
        console.log("show");
      },
      success: function (data) {
        console.log("success");
        $("#modal-user .modal-content").html(data.html_form);
        console.log(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    console.log("Inside save form");
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        console.log("Success");
        console.log(data);
        if (data.form_is_valid) {
          console.log(data.html_user_list)
          $("#user-table tbody").html(data.html_user_list);  // <-- Replace the table body
          $("#modal-user").modal("hide");  // <-- Close the modal
        }
        else {
          //alert("Something went wrong! Please check your data"); 
          $("#modal-user .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

  // Create user
  $(".js-create-user").click(loadForm);
  $("#modal-user").on("submit", ".js-user-create-form",saveForm);

   // Update user
  $("#user-table").on("click", ".js-update-user", loadForm);
  $("#modal-user").on("submit", ".js-user-update-form", saveForm);

    //Clone user
  $("#user-table").on("click", ".js-clone-user", loadForm);

  // Delete book
  $("#user-table").on("click", ".js-delete-user", loadForm);
  $("#modal-user").on("submit", ".js-user-delete-form", saveForm);



});