console.log("in the compound");
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
        $("#modal-compound").modal("show");
        console.log("show");
      },
      success: function (data) {
        console.log("success");
        $("#modal-compound .modal-content").html(data.html_form);
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
        if (data.form_is_valid) {
          $("#compound-table tbody").html(data.html_compound_list);  // <-- Replace the table body
          $("#modal-compound").modal("hide");  // <-- Close the modal
        }
        else {
          //alert("Something went wrong! Please check your data"); 
          $("#modal-compound .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };



  // Create compound
  $(".js-create-compound").click(loadForm);
  $("#modal-compound").on("submit", ".js-compound-create-form",saveForm);

   $("#dismiss-compound").click(function(){ 
     console.log("dismissing");
     $("#modal-compound").modal("hide");  // <-- Close the modal
    });

   // Update compound
  $("#compound-table").on("click", ".js-update-compound", loadForm);
  $("#modal-compound").on("submit", ".js-compound-update-form", saveForm);

    //Clone compound
  $("#compound-table").on("click", ".js-clone-compound", loadForm);

  // Delete book
  $("#compound-table").on("click", ".js-delete-compound", loadForm);
  $("#modal-compound").on("submit", ".js-compound-delete-form", saveForm);



});