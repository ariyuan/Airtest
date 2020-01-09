Based on airtest by Netease

Added two features:

1. Support offset arguments for touch function plus to the original position, enable it to click on the position outside of the picture

  example:

  touch(Template('xxx.png'), x_offset=10, y_offset=10)

2. Support to add more than one image to help recognize a single object

  example:

  touch([Template('image1.png'), Template('image2.png')])





