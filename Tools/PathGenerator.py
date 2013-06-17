import string
import Image
import xml.etree.ElementTree as xml
from xml.dom import minidom
import os

paths = []

map = "maps/map_output.xml"
tree = xml.parse(map)
root = tree.getroot()
map_name = root.attrib["name"]
map_region = root.attrib["region_map"]
map_texture = root.attrib["texture_map"]

day = root.find("date/day").text
month = root.find("date/month").text
year = root.find("date/year").text

provs = []
provs_rgb = []
provs_x = []
provs_y = []
for p in root.findall("province"):
    provs.append(p.find("name").text)
    provs_rgb.append(p.find("rgb").text)
    provs_x.append(p.find("x").text)
    provs_y.append(p.find("y").text)
im = Image.open(map_region)
pix = im.load()
width,height = im.size

print provs

def get_col_from_rgb(rgb):
    col = string.split(rgb)
    return (int(col[0]),int(col[1]),int(col[2]),255)

def get_prov_from_col(col):
    found = False
    for p in range(len(provs_rgb)):
        if col == get_col_from_rgb(provs_rgb[p]):
            #print col,get_col_from_rgb(provs_rgb[p])
            found = True
            return (p+1)
    if found != True:
        print "ERROR FINDING PROVINCE FOR COLOUR: ",col

def add_path(prov_from,prov_to):
    write_path = True
    for p in range(len(paths)):
        if paths[p] == str(prov_from)+"-"+str(prov_to) or paths[p] == str(prov_to)+"-"+str(prov_from):
            write_path = False
    if write_path == True:
        print "New Path: "+str(prov_from)+"-"+str(prov_to)+"\nFrom "+provs[prov_from-1]+" to "+provs[prov_to-1]
        paths.append(str(prov_from)+"-"+str(prov_to))

for x in range(width-1):
    for y in range(height-1):
        # look right
        if pix[x,y] != (0, 0, 0, 255) and pix[x,y][3] != 0:
            if pix[x+1,y] != (0, 0, 0, 255) and pix[x+1,y][3] != 0:
                if pix[x+1,y] != pix[x,y]:
                    add_path(get_prov_from_col(pix[x,y]),get_prov_from_col(pix[x+1,y]))

def save_map():
    root = xml.Element("map")
    root.attrib["name"] = map_name
    root.attrib["region_map"] = map_region
    root.attrib["texture_map"] = map_texture
    p_count = 0

    def add_element(name,text):
        element = xml.Element(name)
        element.text = text
        return (element)

    date = xml.Element("date")
    date.append(add_element("day",day))
    date.append(add_element("month",month))
    date.append(add_element("year",year))
    root.append(date)

    for p in range(len(provs)):
        prov = xml.Element("province")
        prov.attrib["id"] = str(p+1)
        prov.append(add_element("name",provs[p]))
        prov.append(add_element("rgb",provs_rgb[p]))
        prov.append(add_element("x",provs_x[p]))
        prov.append(add_element("y",provs_y[p]))

        root.append(prov)

    e_paths = xml.Element("paths")
    for p in range(len(paths)):
        e_path = xml.Element("path")
        e_path.attrib["name"] = paths[p]
        e_paths.append(e_path)
    root.append(e_paths)


    dir = os.path.dirname(os.path.realpath(__file__))
    slash = "\ "
    slash = string.replace(slash," ","")
    dir = string.replace(dir, slash,"/")+"/"
    map = dir+"maps/map_output.xml"
    file = open(map, 'w')
    xml.ElementTree(root).write(file)
    file.close()

    dom = minidom.parse(map)
    final_xml = dom.toprettyxml()

    file = open(map, 'w')
    file.write(final_xml)
    file.close()

save_map()