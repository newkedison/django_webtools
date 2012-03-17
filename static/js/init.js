function toggle(sub_name){
  var obj = document.getElementById(sub_name);
  if(obj)
  {
    if(obj.style.display=="none")
      obj.style.display="block";
    else
      obj.style.display="none";
  }
}
function initBar()
{
  var pic=document.getElementById('pic');
  var bars = pic.getElementsByTagName('rect');
  for(var i = 0, bar; i < bars.length; i++)
  {
    bar = bars[i];
    if(bar.getAttribute('class') == "bar")
    {
      bar.setAttribute('height', 10);
      bar.setAttribute('rx', 5);
      bar.setAttribute('ry', 5);
    }
  }
}
function initPoint()
{
  var pic=document.getElementById('pic');
  var points = pic.getElementsByTagName('polygon');
  for(var i = 0, point; i < points.length; i++)
  {
    point = points[i];
    if(point.getAttribute('class') == "milestone")
    {
      var x = point.getAttribute('x');
      var y = point.getAttribute('y');
      var s = x + "," + y + " " + (x - 3) + "," + (y - 13) + " " + (x - -3) + "," + (y - 13);
      point.setAttribute('points', s);
    }
  }
}
