function begin(){
  reload()
  document.getElementById('break').disabled = true
}

i = 0

function reload(){
  document.getElementById('svg').data = 'system.svg?' + i
  i = i + 1
  setTimeout('reload2()', 300)
  setTimeout('reload()', 1500)
}


function reload2(){
  document.getElementById('svg2').data = 'system.svg?' + i
}

function ping_page(page){
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "page", true);
  xhr.onreadystatechange = function(){};
  xhr.send(null);
}

function click_start(){
  document.getElementById('break').disabled = false
  document.getElementById('step').disabled = true
  document.getElementById('start').disabled = true
  ping_page('start.cgi')
}

function click_break(){
  document.getElementById('break').disabled = true
  document.getElementById('step').disabled = false
  document.getElementById('start').disabled = false
  ping_page('break.cgi')
}

function click_step(){
  document.getElementById('break').disabled = true
  document.getElementById('step').disabled = false
  document.getElementById('start').disabled = false
  ping_page('step.cgi')
}