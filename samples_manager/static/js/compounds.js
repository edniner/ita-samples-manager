console.log("in the compound");
$(function () {
console.log("inside");
var loadFormCompound = function () {
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

  var loadForm = function () {
  console.log("loading form");
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#admin-modal-compound").modal("show");
        console.log("show");
      },
      success: function (data) {
        console.log("success");
        $("#admin-modal-compound .modal-content").html(data.html_form);
      }
    });
  };

var saveFormCompound = function () {
    var form = $(this);
    console.log("Inside save form");
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#modal-compound").modal("hide");  // <-- Close the modal
          $('.select_element').append($('<option>', {
              value: data['compound_id'],
              text: data['compound_name']
          }));
        }
        else {
          if(data['state']=='sum not ok'){
             alert("The sum of weight fractions should be 100!"); 
            }
          else if (data['state']=='no ok'){
            alert("Please, fill at least one element"); 
          }
          else{
             alert("Somenthing went wrong! Please, check your data."); 
          }
         $("#modal-compound .modal-content").html(data.html_form);
        }
      }
    });
    return false;
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
          $("#admin-modal-compound").modal("hide");  // <-- Close the modal
        }
        else {
          if(data['state']=='sum not ok'){
             alert("The sum of weight fractions should be 100!"); 
            }
          else if (data['state']=='no data'){
            alert("Please, fill at least one element"); 
          }
          else{
             alert("Somenthing went wrong! Please, check your data."); 
          }
          $("#admin-modal-compound .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };



  // Create compound
  $(".js-create-compound").click(loadFormCompound);
  $(".js-create-admin-compound").click(loadForm);
  $("#modal-compound").on("submit", ".js-compound-create-form",saveFormCompound);
  $("#admin-modal-compound").on("submit", ".js-compound-create-form",saveForm);

   // Update compound
  $("#compound-table").on("click", ".js-update-compound", loadFormCompound);
  $("#modal-compound").on("submit", ".js-compound-update-form", saveFormCompound);

    //Clone compound
  $("#compound-table").on("click", ".js-clone-compound", loadFormCompound);

  // Delete book
  $("#compound-table").on("click", ".js-delete-compound", loadFormCompound);
  $("#modal-compound").on("submit", ".js-compound-delete-form", saveFormCompound);



});