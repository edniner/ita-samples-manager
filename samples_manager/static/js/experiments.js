$(function () {

var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-experiment").modal("show");
      },
      success: function (data) {
        $("#modal-experiment .modal-content").html(data.html_form);
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
          if(data['state']=='Created')
            alert("Your irradiation experiment was successfully saved!\nSoon, the facility coordinators will validate your request and you will be able to add samples and additional users.")
          else if (data['state']=='Updated')
            alert("Your irradiation experiment was successfully updated!")
          else if (data['state']=='Validated')
            alert("The experiment was validated. The users will be notified now. ")
          else if (data['state']=='Deleted')
            alert("The experiment was successfully deleted!")
            
          $("#experiment-table tbody").html(data.html_experiment_list);  // <-- Replace the table body
          $("#modal-experiment").modal("hide");  // <-- Close the modal
        }
        else {
          $("#modal-experiment .modal-content").html(data.html_form);
          if(data['state']=='not unique')
            alert("This title already exists! Please, choose a different title.");
          else
            alert("Please, fill all the required fields!");
          
        }
      }
    });
    return false;
  };


  /*var samplesloadForm = function (experiment_id) {
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
*/

  $(".js-assign-dosimeters").click(loadForm);
  // Create experiment
  $(".js-create-experiment").click(loadForm);
  $("#modal-experiment").on("submit", ".js-experiment-create-form",saveForm);

   // Update experiment
  $("#experiment-table").on("click", ".js-update-experiment", loadForm);
  $("#modal-experiment").on("submit", ".js-experiment-update-form", saveForm);

    //Clone experiment
  $("#experiment-table").on("click", ".js-clone-experiment", loadForm);

  // Delete book
  $("#experiment-table").on("click", ".js-delete-experiment", loadForm);
  $("#modal-experiment").on("submit", ".js-experiment-delete-form", saveForm);



});