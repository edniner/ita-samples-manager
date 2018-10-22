self.addEventListener('message', function(e) {
  // code to be run
            var form = $("#sec_form");
            $.ajax({
            url: form.attr("action"),
            data:  form.serialize(),
            type: 'post',
            dataType: 'json',
            success: function (data) {
                    if (data.form_is_valid) {
                        $("#irradiation-table tbody").html(data.html_irradiation_list);  // <-- Replace the table body
                    }
                    else {
                    alert("data is not correct");
                    }
                }
            });
})