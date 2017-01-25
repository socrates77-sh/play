import xlwt
import os

f = xlwt.Workbook()  # 创建工作簿
sheet1 = f.add_sheet('worklog', cell_overwrite_ok=True)

title = ['Date', 'Person', 'Task', 'Percent%']
content = ['2017-1-21', '张文荣', '把else的位置与if处于同一缩进,for语句是python中的循环控制语句。可用来遍历某一对象，还具有一个附带的可选的else块',
           90]

alignment = xlwt.Alignment()
alignment.vert = xlwt.Alignment.VERT_CENTER
alignment.horz = xlwt.Alignment.HORZ_LEFT
alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT

style = xlwt.XFStyle()
style.alignment = alignment

for i in range(0, len(title)):
    sheet1.write(0, i, title[i], xlwt.easyxf('font: bold on'))
    sheet1.write(1, i, content[i], xlwt.easyxf('align: wrap on, horiz left, vert center'))

sheet1.col(0).width = 3000
sheet1.col(1).width = 3000
sheet1.col(2).width = 10000
sheet1.col(3).width = 3000

desk_path = os.path.join(os.path.expanduser("~"), 'Desktop')
print(desk_path)
xl_file = os.path.join(desk_path, 'worklog.xls')

try:
    f.save(xl_file)
except PermissionError:
    print('ERROR: %s is opened now' % xl_file)
    exit(1)