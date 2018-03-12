$(function () {
  $(".soap").click(function(event){
      console.log("Soap request");

      try {
      xmlhttp = new XMLHttpRequest();
      }
      catch(e) {
      xmlhttp = new ActiveXObject('Microsoft.XMLHTTP');
      }

      xmlhttp.open('POST', 'https://cmmsx.cern.ch/WSHub/SOAP',
    true);

      xmlhttp.onreadystatechange=function(){
        if(xmlhttp.readyState!=4)return;
        if(!xmlhttp.status||xmlhttp.status==200)
          console.log(xmlhttp.responseText);
        else
          alert("Request failed!");
        }
      xmlhttp.send('<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:wsh="http://cern.ch/cmms/infor/wshub">' +
        '<soapenv:Header/>'+
          '<soapenv:Body>'+
            '<wsh:readEquipment>'+
              '<equipmentCode>PXXISET001-CR002706</equipmentCode>'+
              '<credentials>'+
                '<password>Maurice008</password>'+
                '<username>irrad</username>'+
              '</credentials>'+
            '<sessionID></sessionID>'+
          '</wsh:readEquipment>'+
        '</soapenv:Body>'+
      '</soapenv:Envelope>'
        );
      });
});


//no soap yet