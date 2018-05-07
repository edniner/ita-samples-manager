$(function () {

  checked_values = 0;

  $('.chk').change(function() {
    /*if(this.checked) {
            alert($(this).val());
        }   */
    if (this.checked){
        checked_values = checked_values + 1;
        $('#new_dos').hide();
        $('#print_dos').show();
        $('#generate_dos').hide();
      } 
    else{
      checked_values = checked_values - 1;
      if (checked_values == 0){
        $('#new_dos').show();
        $('#print_dos').hide();
        $('#generate_dos').show();
      }
    }
  });
  
var  generate_ids = function () {
    console.log("generate");
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
          alert("Something went wrong!"); 
          $("#modal-dosimeter .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

  var printLabel = function (){
          var form = $(this);
          $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                  $("#modal-dosimeter").modal("hide");  // <-- Close the modal
                  var text = '<html><head><title>'+data['dos_id']+'</title></head><body onafterprint="self.close()"><h1 style ="text-align: center; font-size:350%; margin:0">'+data['dos_id'] + '<h1 style ="text-align: center; margin:0">'+data['dos_type'] +'</h1>';
                  text = text+ '<h2 style = "text-align:center; margin:0">IRRAD</h2></body></html>';
                  my_window = window.open('', 'mywindow', 'status=1,width=350,height=300');
                  my_window.document.write(text);
                  my_window.document.close();
                  $("#dosimeter-table tbody").html(data.html_dosimeter_list);  // <-- Replace the table body
              }
          });
          console.log("false")
          return false;
  }

  // Create dosimeter
  $(".js-create-dosimeter").click(loadForm);

  $("#generate_dos").click(generate_ids);
  $("#modal-dosimeter").on("submit", ".js-generate-ids-form", saveForm);

  $("#modal-dosimeter").on("submit", ".js-dosimeter-create-form",saveForm );

   // Update dosimeter
  $("#dosimeter-table").on("click", ".js-update-dosimeter", loadForm);
  $("#modal-dosimeter").on("submit", ".js-dosimeter-update-form", saveForm);

    //Clone dosimeter
  $("#dosimeter-table").on("click", ".js-clone-dosimeter", loadForm);

  // Delete dosimeter
  $("#dosimeter-table").on("click", ".js-delete-dosimeter", loadForm);
  $("#modal-dosimeter").on("submit", ".js-dosimeter-delete-form", saveForm);

  // Print label
  $("#dosimeter-table").on("click", ".js-print-dosimeter-label", loadForm);
  $("#modal-dosimeter").on("submit", ".js-print-dosimeter-label-form", printLabel);

  

});