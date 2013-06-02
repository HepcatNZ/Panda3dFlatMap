import Image
import xml.etree.ElementTree as xml
from xml.dom import minidom
import string

map_image = "maps/regions.png"
map_terrain = "maps/texture.jpg"
im = Image.open(map_image)
pix = im.load()
width,height = im.size
aspect = width/height
print "Map Size:",width,"X",height

print "Setting attributes"

root = xml.Element("map")
root.attrib["name"] = "Unnamed World"
root.attrib["region_map"] = map_image
root.attrib["texture_map"] = map_terrain
p_count = 0



def add_element(name,text):
    element = xml.Element(name)
    element.text = text
    return (element)

date = xml.Element("date")
date.append(add_element("day","1"))
date.append(add_element("month","1"))
date.append(add_element("year","1"))
root.append(date)

print "Finding Provinces..."

for x in range(width):
    for y in range(height):
        if pix[x,y] == (0,0,0,255):
            p_rgb = str(pix[x+1,y])
            p_rgb = string.replace(p_rgb,"(","")
            p_rgb = string.replace(p_rgb,", 255)","")
            p_rgb = string.replace(p_rgb,",","")
            p_x = str(x)
            p_y = str(y)
            p_count += 1

            prov = xml.Element("province")
            prov.attrib["id"] = str(p_count)
            prov.append(add_element("name","Prov"+str(p_count)))
            prov.append(add_element("rgb",p_rgb))
            prov.append(add_element("x",p_x))
            prov.append(add_element("y",p_y))
            root.append(prov)

print p_count,"provinces created!"

map = "maps/map_output.xml"
file = open(map, 'w')
xml.ElementTree(root).write(file)
file.close()

dom = minidom.parse(map)
final_xml = dom.toprettyxml()

file = open(map, 'w')
file.write(final_xml)
file.close()

print "Saved as",map



#root.append(prov)