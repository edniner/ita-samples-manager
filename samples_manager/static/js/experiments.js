$(function () {
console.log("experiments");
var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-experiment").modal({
          closable:false,
          onApprove : function() {
			    return false;
			  }
        }).modal("show");
      },
      success: function (data) {
        $("#modal-experiment .scrolling.content").html(data.html_form);
      }
    });
  };
var loadFormDetails = function () {
    console.log("loading form details");
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-experiment-details").modal({
          closable:false,
          onApprove : function() {
			    return false;
			  }
        }).modal("show");
      },
      success: function (data) {
        $("#modal-experiment-details .scrolling.content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    console.log("saving form!!!!!");
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        console.log("successsssss");
        if (data.form_is_valid) {
          if(data['state']=='Created')
            alert("Your irradiation experiment was successfully saved!\nSoon, the facility coordinators will validate your request and you will be able to add samples and additional users.")
          else if (data['state']=='Updated')
            alert("Your irradiation experiment was successfully updated!")
          else if (data['state']=='Validated')
            alert("The experiment was validated. The users will be notified now. ")
          else if (data['state']=='Deleted')
            alert("The experiment was successfully deleted!")
          $("#data-table tbody").html(data.html_experiment_list);  // <-- Replace the table body
          $("#modal-experiment").modal("hide");  // <-- Close the modal
        }
        else {
           $("#modal-experiment .scrolling.content").html(data.html_form);
          if(data['state']=='not unique')
            alert("This title already exists! Please, choose a different title.");
          else
            alert("Please, fill all the required fields!");
        }
      }
    });
    return false;
  };

   var saveFormInDetails = function () {
     console.log("saving");
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        console.log("succe");
        if (data.form_is_valid) {
          alert("Your irradiation experiment was successfully updated!");
          $("#experiment-details").html(data.html_experiment);  // <-- Replace the table body
          $("#modal-experiment-details").modal("hide");  // <-- Close the modal
          return false;
        }
        else {
           $("#modal-experiment-details .scrolling.content").html(data.html_form);
        }
      }
    });
    return false;
   }

  $(".js-assign-dosimeters").click(loadForm);
  // Create experiment
  $(".js-create-experiment").click(loadForm);
  $("#modal-experiment").on("submit", ".js-experiment-create-form",saveForm);

   // Update experiment
  $("#data-table").on("click", ".js-update-experiment", loadForm);
  $("#modal-experiment").on("submit", ".js-experiment-update-form", saveForm);

  $("#experiment-details").on("click", ".js-update-experiment-details", loadFormDetails);
  $("#modal-experiment-details").on("submit", ".js-experiment-comment-update-form", saveFormInDetails);

  //Clone experiment
  $("#data-table").on("click", ".js-clone-experiment", loadForm);

  // Delete book
  $("#data-table").on("click", ".js-delete-experiment", loadForm);
  $("#modal-experiment").on("submit", ".js-experiment-delete-form", saveForm);



});