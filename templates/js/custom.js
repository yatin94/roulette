
 var $inner = $('.inner'),
     $spin = $('#spin'),
     $reset = $('#reset'),
     $data = $('.data'),
     $mask = $('.mask'),
     maskDefault = 'Place Your Bets',
     timer = 9000;

var red = [32,19,21,25,34,27,36,30,23,5,16,1,14,9,18,7,12,3];

$reset.hide();
test = ""
$mask.text(maskDefault);
 $(document).ready(function(){
    setInterval(function(){ 
   $('#reset').click();
   $('#spin').click();
},35000);
});  
$spin.on('click',function(){
    var xamt = new XMLHttpRequest();
    xamt.onreadystatechange = function() {
      if (this.readyState==4 && this.status == 200) {
        // return Number(xamt.responseText)
        
        var  randomNumber = Number(xamt.responseText),
      color = null;
      testing(randomNumber)
      }
    }

    xamt.open('GET',"http://192.168.1.42:5060/getrand")
    xamt.send()
  });
  
  
function testing(randomNumber){
  // get a random number between 0 and 36 and apply it to the nth-child selector

  


//  var  randomNumber = numberdata,
//       color = null;
      $inner.attr('data-spinto', randomNumber).find('li:nth-child('+ randomNumber +') input').prop('checked','checked');
      // prevent repeated clicks on the spin button by hiding it
       $(this).hide();
      // disable the reset button until the ball has stopped spinning
       $reset.addClass('disabled').prop('disabled','disabled').show();
  
      $('.placeholder').remove();
  
  
  setTimeout(function() {
      $mask.text('No More Bets');
      }, timer/2);
  
  setTimeout(function() {
      $mask.text(maskDefault);
      }, timer+500);
  
 
  
  // remove the disabled attribute when the ball has stopped
  setTimeout(function() {
    $reset.removeClass('disabled').prop('disabled','');
    
    if($.inArray(randomNumber, red) !== -1){ color = 'red'} else { color = 'black'};
    if(randomNumber == 0){color = 'green'};
    
    $('.result-number').text(randomNumber);
    $('.result-color').text(color);
    $('.result').css({'background-color': ''+color+''});
    $data.addClass('reveal');
    $inner.addClass('rest');
    
    $thisResult = '<li class="previous-result color-'+ color +'"><span class="previous-number">'+ randomNumber +'</span><span class="previous-color">'+ color +'</span></li>';
     


    $('.previous-list').prepend($thisResult);
   
    
      var xamt = new XMLHttpRequest();
      xamt.onreadystatechange = function() {
        if (this.readyState==4 && this.status == 200) {
            returnobj = JSON.parse(xamt.responseText)
            document.getElementById("messagesuccessdiv").style.visibility = 'Visible' 
            document.getElementById("messagesuccess").innerHTML=returnobj.data
            document.getElementById("amouth2").innerHTML="Your Total Amount: $"+returnobj.money
            
            
        }
      }

      xamt.open('GET',"http://192.168.1.42:5060/winner")
      xamt.send()






      var tablewinner = new XMLHttpRequest();
      tablewinner.onreadystatechange = function() {
        if (this.readyState==4 && this.status == 200) {
          var a = tablewinner.responseText
          obj = JSON.parse(a);
          var tableRef = document.getElementById('mytable').getElementsByTagName('tbody')[0];
          var i;
          for (i = 1; i < obj.count+1; i++) {
            document.getElementById("mytable").deleteRow(1);
          }
          obj.data.forEach(element => {
            var newRow   = tableRef.insertRow();
            var cellname  = newRow.insertCell(0);
            var cellmoney  = newRow.insertCell(1);
            var celltotal  = newRow.insertCell(2);
            var nametext  = document.createTextNode(element[0]);
            var moneytext  = document.createTextNode(element[1]);
            var newText  = document.createTextNode(element[2]);
            cellname.appendChild(nametext);
            cellmoney.appendChild(moneytext);
            celltotal.appendChild(newText);
          }); 


        }
      }

      tablewinner.open('GET',"http://192.168.1.42:5060/getmoneytable")
      tablewinner.send()
    


    
    }, timer);
  
}


$reset.on('click',function(){
  // remove the spinto data attr so the ball 'resets'
  $inner.attr('data-spinto','').removeClass('rest');
  $(this).hide();
  $spin.show();
  $data.removeClass('reveal');
});

// so you can swipe it too
var myElement = document.getElementById('plate');
var mc = new Hammer(myElement);
mc.on("swipe", function(ev) {
  if(!$reset.hasClass('disabled')){
    if($spin.is(':visible')){
      $spin.click();  
    } else {
      $reset.click();
    }
  }  
});


function toggleSignup(){
   document.getElementById("login-toggle").style.backgroundColor="#fff";
    document.getElementById("login-toggle").style.color="#222";
    document.getElementById("signup-toggle").style.backgroundColor="#8a0000";
    document.getElementById("signup-toggle").style.color="#fff";
    document.getElementById("login-form").style.display="none";
    document.getElementById("signup-form").style.display="block";
}
 
function toggleLogin(){
    document.getElementById("login-toggle").style.backgroundColor="#8a0000";
    document.getElementById("login-toggle").style.color="#fff";
    document.getElementById("signup-toggle").style.backgroundColor="#fff";
    document.getElementById("signup-toggle").style.color="#222";
    document.getElementById("signup-form").style.display="none";
    document.getElementById("login-form").style.display="block";
}





