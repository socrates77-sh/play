__author__ = 'socrates'

from PIL import Image

import StringIO
import urllib2

url = 'http://cdn.01happy.com/wp-content/uploads/2012/09/bg.png'
file = urllib2.urlopen(url)
tmpIm = cStringIO.StringIO(file.read())
im = Image.open(tmpIm)

image = Image.open(
    r"http://ww1.sinaimg.cn/large/840c9a4fgw1f8omnxdllhj20fp0kzn0v.jpg")
image.show()

a = 0

b = 0
