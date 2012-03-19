function set_obj_display(obj, is_display)
{
  if(obj)
  {
    if(is_display)
      obj.style.display = "block";
    else
      obj.style.display = "none";
  }
}

Array.prototype.indexOf = function(item, i){ //判断Array的原型是否已作indexOf方法的扩展
  i || (i = 0); //初始化起步查询的下标，比较奇特的写法。
  var length = this.length;
  if (i < 0) i = length + i; // 如i为负数，则从数组末端开始。
  for (; i < length; i++)
    if (this[i] === item) return i;  // 使用全等于(===)判断符
  return -1;
};

function toggle(parent_name){
  var bars = document.getElementsByTagName('g');
  var is_show = true;
  var found_bars_name = Array(parent_name);
  for(var i = 0, bar; i < bars.length; i++)
  {
    bar = bars[i];
    var old_show = (bar.style.display != "none");
    var bar_parent = bar.getAttribute('parent_name');
    var bar_name = bar.getAttribute('id');
    if(found_bars_name.length == 1)
    {
      if(bar_parent == parent_name)
      {
        is_show = !old_show;
        found_bars_name.push(bar_name);
        set_obj_display(bar, is_show)
      }
      else
      {
        set_obj_display(bar, old_show);
      }
    }
    else
    {
      var index = found_bars_name.indexOf(bar_parent, 0);
      if(index == -1)
      {
        set_obj_display(bar, old_show);
      }
      else
      {
        set_obj_display(bar, is_show);
        if(found_bars_name.indexOf(bar_name, 0) == -1)
        {
          found_bars_name.push(bar_name);
        }
      }
    }
  }
  var start_y = 10;
  var step_y = 30;
  for(var i = 0, y = start_y, bar; i < bars.length; i++)
  {
    bar = bars[i];
    if(bar.style.display != "none")
    {
      bar.setAttribute("y", y);
      y += step_y;
    }
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
