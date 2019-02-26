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
        $("#modal-user").modal({
          closable:false,
          onApprove : function() {
			    return false;
			  }
        }).modal("show");
      },
      success: function (data) {
        console.log("success");
        $("#modal-user .scrolling.content").html(data.html_form);
        console.log(data.html_form);
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
        console.log("Success");
        console.log(data);
        if (data.form_is_valid) {
          console.log(data.html_user_list)
          if(data['state']=='Created')
            alert("The user data were successfully saved! The user should still subscribe in irrad-ps-users e-group if he/she is not a member!")
          else if (data['state']=='Deleted')
            alert("The user was deleted. He/she will not have access to the related experiments and samples anymore!")
          else if(data['state']=='Updated')
            alert("The user information were updated!")
          $("#data-table tbody").html(data.html_user_list);  // <-- Replace the table body
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
  $("#data-table").on("click", ".js-update-user", loadForm);
  $("#modal-user").on("submit", ".js-user-update-form", saveForm);

    //Clone user
  $("#data-table").on("click", ".js-clone-user", loadForm);

  // Delete book
  $("#data-table").on("click", ".js-delete-user", loadForm);
  $("#modal-user").on("submit", ".js-user-delete-form", saveForm);



});