#encoding: utf-8
from django import forms

class UploadForm(forms.Form):
  directory = forms.CharField(label='文件夹', max_length=100, 
    help_text='文件要保存在哪一个文件夹内.注意,这个文件夹必须已存在.')
  password = forms.CharField(label='密码', max_length=100, 
    widget=forms.PasswordInput, help_text='该文件夹的上传密码')
  filename = forms.RegexField(label='文件名', max_length=30, required=False,
    regex = r'^\w[\w.-]*',
    help_text='文件被下载时使用的文件名,不能和同文件夹内的其他已存在的文件重复'\
    + '<br />只能是字母/数字/./-/_.如果留空,表示使用上传的文件名'\
    + '<br />如果要使用中文文件名,可以先修改欲上传的文件为该名字,然后这里留空',
    error_messages = {'invalid': '文件名只能是字母/数字/./-/_'})
  content_type = forms.ChoiceField(label='文件类型', required=False,
    help_text='一般选择自动检测,会根据扩展名自动判断,对于一些没有扩展名的文件,'\
            + '而且需要在线查看的,才需要自行指定类型',
    choices = [
      ('', '自动检测'),
      ('text/plain', '文本文件'),
      ('text/html', 'HTML文件'),
      ('text/xml', 'XML文件'),
      ('application/pdf', 'PDF文件'),
      ('image/*', '图片文件'),
      ('video/*', '视频文件'),
      ('audio/*', '音频文件'),
      ('application/msword', 'word文件'),
      ('application/vnd.ms-excel', 'Excel文件'),
      ('application/vnd.ms-powerpoint', 'PPT文件'),
      ('application/x-javascript', 'JAVA/javascript'),
      ('application/*zip*', '压缩包'),
      ('application/octet-stream', '其他二进制文件'),
    ])
  auto_delete = forms.CharField(label='自动删除时间', initial=0,
    help_text='单位:天.达到指定天数后,该文件会自动删除,设为0表示不自动删除')
  description = forms.CharField(label='文件描述', required=False,
    help_text='对文件的描述,可以为空', widget=forms.Textarea)
  file = forms.FileField(label='待上传文件')

class DirPasswordForm(forms.Form):
  directory = forms.CharField(label='要查看的文件夹名称', max_length=100)
  password = forms.CharField(label='请输入该文件的密码', max_length=100, 
                             widget=forms.PasswordInput)

class DeleteConfirmForm(forms.Form):
  password = forms.CharField(label='请输入文件夹的密码', max_length=100, 
                             widget=forms.PasswordInput)

