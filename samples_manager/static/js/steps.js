  $(document).ready(function() {
        var ct = 0;

        $('.next1').on('click', function(e) {

            e.preventDefault();

            $('#step1').animate('fast', function() {

            if (ct > 0) {
                $('#step1').removeClass('transition visible');
                $('#step1').addClass('transition hidden');

            }
            $('#step1').css('display', 'none');

            $('#step1S').addClass('disabled');
            $('#step2S').removeClass('disabled');
            $("#step2").transition('fly right');
            $('body').css('background-color', '#06000a');
            $('#step2 button').removeClass('inverted blue');
            $('#step2 button').addClass('inverted blue');
            ct++;

            });

        });

        $('.prev1').on('click', function(e) {

            e.preventDefault();
            $('#step1S').removeClass('disabled');
            $('#step2S').addClass('disabled');

            $('#step2').animate('fast', function() {

            $('body').css('background-color', '#300032');
            $('#step2').transition('hide');
            $("#step1").transition('fly right');

            });

        });

        $('.next2').on('click', function(m) {

            m.preventDefault();

            $('#step2S').addClass('disabled');
            $('#step3S').removeClass('disabled');

            $('#step2').animate('fast', function() {

            $('body').css('background-color', '#251605');
            $('#step2').transition('hide');

            $('#step3').transition('fly right');
            });

        });

        $('.prev2').on('click', function(m) {

            m.preventDefault();
            $('#step3S').addClass('disabled');
            $('#step2S').removeClass('disabled');

            $('#step3').animate('fast', function() {

            $('body').css('background-color', '#06000a');
            $('#step3').transition('hide');

            $('#step2').transition('fly right');
            });

        });

        /*$('.submit').on('click', function(p) {
            p.preventDefault();
            $('#step3').stop();
            saveForm();
        });*/

    });