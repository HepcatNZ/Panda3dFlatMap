import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
import xml.etree.ElementTree as xml
from xml.dom import minidom
import string
import glob
import os
import sys
import Image
from panda3d.core import Filename



class MapEditor:
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file("MapEditor.glade")

        self.window = self.builder.get_object("window")
        self.window.connect('destroy', lambda w: gtk.main_quit())
        self.window.show()

        self.win_map = self.builder.get_object("window_map")
        self.fix_map = self.builder.get_object("fixed_map")
        self.win_map_scroll = self.builder.get_object("scrolledwindow2")
        self.win_map.connect('destroy', lambda w: gtk.main_quit())
        self.win_map.show()
        self.win_map.add_events(gtk.gdk.POINTER_MOTION_MASK)
        self.win_map.connect("motion-notify-event", self.mouse_motion)
        self.win_map.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.win_map.connect("button-press-event", self.mouse_click)

        self.window.move(0,0)
        self.win_map.move(820,0)

        self.import_widgets(self.builder)

    def import_widgets(self,builder):
        self.btn_map_save = builder.get_object("btn_map_save")
        self.btn_map_save.connect("clicked",self.save_map)

        self.lbl_mouse_info = builder.get_object("lbl_mouse")

        self.txt_map_name = builder.get_object("entry_map_name")
        self.txt_prov_name = builder.get_object("entry_prov_name")
        self.txt_prov_name.connect("changed",self.set_prov_name)

        self.adj_day = builder.get_object("adj_day")
        self.adj_month = builder.get_object("adj_month")
        self.adj_year = builder.get_object("adj_year")

        self.cmbo_maps = builder.get_object("cmbo_maps")
        self.cmbo_maps.connect("changed",self.load_map)
        self.ls_maps = builder.get_object("ls_maps")

        self.app_path = os.path.dirname(os.path.realpath(__file__))
        os.chdir(self.app_path+"/maps")

        self.maps = []
        self.ls_maps.clear()
        self.ls_maps.append(["<None>"])
        self.tv_maps = builder.get_object("tv_maps")
        self.cmbo_maps.set_active(0)
        for files in glob.glob("*.xml"):
            self.ls_maps.append([files])
            self.maps.append(files)
            print files

        self.tv_provs = builder.get_object("tv_provinces")
        #self.tv_provs.connect("changed",self.load_map)
        self.ls_provs = builder.get_object("ls_provinces")
        self.ts_provs = self.tv_provs.get_selection()
        self.ts_provs.connect("changed", self.refresh_details)

        self.img_map = builder.get_object("image_map")

    def set_prov_name(self,widget):
        self.provs[self.selected_prov] = self.txt_prov_name.get_text()
        self.ls_provs.set_value(self.iter, 0, str(self.selected_prov+1)+": "+self.provs[self.selected_prov])


    def load_map(self,widget):
        if self.cmbo_maps.get_active() > 0:
            self.map = self.app_path+"/maps/"+self.maps[self.cmbo_maps.get_active()-1]
            tree = xml.parse(self.map)
            root = tree.getroot()
            self.txt_map_name.set_text(root.attrib["name"])

            self.map_region = root.attrib["region_map"]
            self.map_texture = root.attrib["texture_map"]

            self.adj_day.set_value(int(root.find("date/day").text))
            self.adj_month.set_value(int(root.find("date/month").text))
            self.adj_year.set_value(int(root.find("date/year").text))

            self.ls_provs.clear()
            self.provs = []
            self.provs_x = []
            self.provs_y = []
            self.provs_rgb = []
            for p in root.findall("province"):
                self.provs.append(p.find("name").text)
                self.ls_provs.append([p.get("id")+": "+p.find("name").text])
                self.provs_rgb.append(p.find("rgb").text)
                self.provs_x.append(p.find("x").text)
                self.provs_y.append(p.find("y").text)

            im = Image.open(self.app_path+"/"+root.get("region_map"))
            self.pix = im.load()
            self.width,self.height = im.size
            #self.img_map.set_size_request(width, height)
            #self.img_map.set_from_file(self.app_path+"/"+root.get("texture_map"))
            #print self.app_path+"/"+root.get("texture_map")

            self.img_map.set_size_request(self.width, self.height)
            self.img_map.set_from_file(self.app_path+"/"+root.get("region_map"))
            print self.app_path+"/"+root.get("region_map")

    def get_col_from_rgb(self,rgb):
        col = string.split(rgb)
        return (int(col[0]),int(col[1]),int(col[2]),255)

    def get_prov_from_col(self,colour):
        found = False
        for p in range(len(self.provs)):
            if self.get_col_from_rgb(self.provs_rgb[p]) == colour:
                found = True
                return p
        if found == False:
            print "##ERROR FINDING PROV FROM COL "+str(colour)+"##"

    def mouse_click(self,window,event):
        if self.cmbo_maps.get_active() != 0:
            self.mouse_x = event.x+self.win_map_scroll.get_hadjustment().get_value()
            self.mouse_y = event.y+self.win_map_scroll.get_vadjustment().get_value()
            if (event.x > self.img_map.allocation.x and event.x < self.img_map.allocation.x+self.width):
                if (event.y > self.img_map.allocation.y and event.y < self.img_map.allocation.y+self.height):
                    alpha = self.pix[self.mouse_x,self.mouse_y][3]
                    if self.pix[self.mouse_x,self.mouse_y] == (0,0,0,255):
                        self.selected_prov = self.get_prov_from_col(self.pix[self.mouse_x+1,self.mouse_y])
                        if self.selected_prov != -1:
                            self.tv_provs.set_cursor(self.selected_prov)
                    elif alpha == 255:
                        self.selected_prov = self.get_prov_from_col(self.pix[self.mouse_x,self.mouse_y])
                        if self.selected_prov != -1:
                            self.tv_provs.set_cursor(self.selected_prov)

    def refresh_details(self,event):
        #self.txt_prov_name.set_text()
        (model,pathlist) = self.ts_provs.get_selected_rows()
        for path in pathlist:
            self.iter = model.get_iter(path)
            value = model.get_value(self.iter,0)
            print path,value
            prov_id = str(path)
            prov_id = string.replace(prov_id,"(","")
            prov_id = string.replace(prov_id,",","")
            prov_id = string.replace(prov_id,")","")
            prov_id = int(prov_id)
            self.selected_prov = prov_id
            self.txt_prov_name.set_text(self.provs[prov_id])


    def mouse_motion(self,window,event):
        if self.cmbo_maps.get_active() != 0:
            self.mouse_x = event.x+self.win_map_scroll.get_hadjustment().get_value()
            self.mouse_y = event.y+self.win_map_scroll.get_vadjustment().get_value()
            if (event.x > self.img_map.allocation.x and event.x < self.img_map.allocation.x+self.width):
                if (event.y > self.img_map.allocation.y and event.y < self.img_map.allocation.y+self.height):
                    alpha = self.pix[self.mouse_x,self.mouse_y][3]
                    if self.pix[self.mouse_x,self.mouse_y] == (0,0,0,255):
                        self.lbl_mouse_info.set_text("Mouse X: "+str(self.mouse_x)+"\nMouse Y: "+str(self.mouse_y)+"\nColour: "+str(self.pix[self.mouse_x+1,self.mouse_y])+"\nAlpha: "+str(alpha))
                    elif alpha == 255:
                        self.lbl_mouse_info.set_text("Mouse X: "+str(self.mouse_x)+"\nMouse Y: "+str(self.mouse_y)+"\nColour: "+str(self.pix[self.mouse_x,self.mouse_y])+"\nAlpha: "+str(alpha))
                    else:
                        self.lbl_mouse_info.set_text("Mouse X: "+str(self.mouse_x)+"\nMouse Y: "+str(self.mouse_y))
                    self.fix_map.move(self.lbl_mouse_info,int(round(self.mouse_x)),int(round(self.mouse_y)))

    def save_map(self,widget):
        root = xml.Element("map")
        root.attrib["name"] = self.txt_map_name.get_text()
        root.attrib["region_map"] = self.map_region
        root.attrib["texture_map"] = self.map_texture
        p_count = 0

        def add_element(name,text):
            element = xml.Element(name)
            element.text = text
            return (element)

        date = xml.Element("date")
        date.append(add_element("day",str(int(self.adj_day.get_value()))))
        date.append(add_element("month",str(int(self.adj_month.get_value()))))
        date.append(add_element("year",str(int(self.adj_year.get_value()))))
        root.append(date)

        for p in range(len(self.provs)):
            prov = xml.Element("province")
            prov.attrib["id"] = str(p+1)
            prov.append(add_element("name",self.provs[p]))
            prov.append(add_element("rgb",self.provs_rgb[p]))
            prov.append(add_element("x",self.provs_x[p]))
            prov.append(add_element("y",self.provs_y[p]))
            root.append(prov)

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

if __name__ == "__main__":
    app = MapEditor()
    gtk.main()