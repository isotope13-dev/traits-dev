from PIL import Image
image = Image.open("picture.png")
x = image.getpixel((0,0))
byte = px[2] & 0xf
text = map(chr,filter(None,values))
extra = px[1]&0xf
