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
        self.builder.add_from_file("ScenarioEditor.glade")

        self.window = self.builder.get_object("window")
        self.window.connect('destroy', lambda w: gtk.main_quit())
        self.window.show()

        self.import_widgets(self.builder)

    def import_widgets(self,builder):
        self.user_changing = True
        self.maps = []

        #SCENARIO TAB
        self.adj_day = builder.get_object("adj_day")
        self.adj_month = builder.get_object("adj_month")
        self.adj_year = builder.get_object("adj_year")
        self.cmbo_scen = builder.get_object("cmbo_map")
        self.lbl_map_name = builder.get_object("lbl_map_name")
        self.cmbo_scen.connect("changed",self.load_map)
        self.txt_scen_name = builder.get_object("txt_scen_name")

        #MAPS TAB
        self.cmbo_maps = builder.get_object("cmbo_map")
        self.lbl_map_name = builder.get_object("lbl_map_name")
        self.cmbo_maps.connect("changed",self.load_map)
        self.ls_maps = builder.get_object("ls_maps")
        self.ls_map_provs = builder.get_object("ls_map_provinces")

        self.ls_maps.clear()
        self.ls_maps.append(["<None>"])
        #self.tv_maps = builder.get_object("tv_maps")
        self.cmbo_maps.set_active(0)

        self.app_path = os.path.dirname(os.path.realpath(__file__))
        os.chdir(self.app_path+"/maps")
        for files in glob.glob("*.xml"):
            self.ls_maps.append([files])
            self.maps.append(files)
            print files

        #NATION TAB
        self.tv_nations = builder.get_object("tv_nations")
        self.ls_nations = builder.get_object("ls_nations")
        self.ts_nations = self.tv_nations.get_selection()
        self.tv_nations.set_cursor(0)
        self.ts_nations.connect("changed", self.update_nations)

        self.cmbo_nation_capital = builder.get_object("cmbo_nation_capital")
        self.txt_nation_colour = builder.get_object("txt_nation_colour")
        self.txt_nation_name = builder.get_object("txt_nation_name")
        self.btn_nation_create = builder.get_object("btn_nation_new")
        self.btn_nation_create.connect("clicked", self.nation_create)
        self.adj_nation_coin = builder.get_object("adj_nation_coin")
        self.adj_nation_men = builder.get_object("adj_nation_manpower")

        #PROVINCES TAB
        self.ls_scen_provs = builder.get_object("ls_scen_provinces")
        self.tv_scen_provs = builder.get_object("tv_scen_provinces")
        self.ts_scen_provs = self.tv_scen_provs.get_selection()
        self.ts_scen_provs.connect("changed", self.update_scen_provs)

        self.ls_prov_nation = builder.get_object("ls_prov_nation")
        self.txt_prov_name = builder.get_object("txt_prov_name")
        self.adj_prov_coin = builder.get_object("adj_prov_coin")
        self.adj_prov_men = builder.get_object("adj_prov_men")
        self.cmbo_prov_owner = builder.get_object("cmbo_prov_owner")
        self.cmbo_prov_owner.connect("changed",self.change_scen_provs)
        self.txt_prov_name.connect("changed",self.change_scen_provs)
        self.adj_prov_coin.connect("value-changed",self.change_scen_provs)
        self.adj_prov_men.connect("value-changed",self.change_scen_provs)

        #ARMY TAB
        self.ls_armies = builder.get_object("ls_armies")
        self.tv_armies = builder.get_object("tv_armies")
        self.ts_armies = self.tv_armies.get_selection()
        self.tv_armies.set_cursor(0)
        self.ts_armies.connect("changed", self.update_armies)

        self.ls_army_provinces = builder.get_object("ls_army_provinces")
        self.txt_army_name = builder.get_object("txt_army_name")
        self.cmbo_army_view_prov = builder.get_object("cmbo_army_view_prov")
        self.cmbo_army_prov = builder.get_object("cmbo_army_prov")
        self.cmbo_army_home = builder.get_object("cmbo_army_home")
        self.adj_army_inf = builder.get_object("adj_inf")
        self.adj_army_arch = builder.get_object("adj_arch")
        self.adj_army_cav = builder.get_object("adj_cav")
        self.btn_army_new = builder.get_object("btn_army_create")
        self.btn_army_new.connect("clicked", self.army_create)

        #SAVE TAB
        self.btn_scen_save = builder.get_object("btn_scen_save")
        self.txt_filename = builder.get_object("txt_filename")
        self.btn_scen_save.connect("clicked",self.save_scenario)

    def update_scen_provs(self,event):
        (model,pathlist) = self.ts_scen_provs.get_selected_rows()
        for path in pathlist:
            self.iter = model.get_iter(path)
            value = model.get_value(self.iter,0)
            prov_id = str(path)
            prov_id = string.replace(prov_id,"(","")
            prov_id = string.replace(prov_id,",","")
            prov_id = string.replace(prov_id,")","")
            prov_id = int(prov_id)
            self.selected_prov = prov_id+1
            self.user_changing = False
            self.txt_prov_name.set_text(self.provinces[prov_id+1][0])
            self.user_changing = False
            self.adj_prov_coin.set_value(self.provinces[prov_id+1][5])
            self.user_changing = False
            self.adj_prov_men.set_value(self.provinces[prov_id+1][6])
            self.user_changing = False
            self.cmbo_prov_owner.set_active(self.provinces[prov_id+1][7])
            self.user_changing = True

    def update_nations(self,event):
        (model,pathlist) = self.ts_nations.get_selected_rows()
        for path in pathlist:
            self.iter = model.get_iter(path)
            value = model.get_value(self.iter,0)
            nation_id = str(path)
            nation_id = string.replace(nation_id,"(","")
            nation_id = string.replace(nation_id,",","")
            nation_id = string.replace(nation_id,")","")
            nation_id = int(nation_id)
            self.nation_selected = nation_id+1
            if (nation_id != 0):
                self.btn_nation_create.set_sensitive(False)
                self.user_changing = False
                self.txt_nation_name.set_text(self.nations[nation_id][0])
                self.user_changing = False
                self.txt_nation_colour.set_text(self.nations[nation_id][1])
                self.user_changing = False
                self.cmbo_nation_capital.set_active(self.nations[nation_id][2]-1)
                self.user_changing = False
                self.adj_nation_coin.set_value(self.nations[nation_id][3])
                self.user_changing = False
                self.adj_nation_men.set_value(self.nations[nation_id][4])
                self.user_changing = True
            else:
                self.btn_nation_create.set_sensitive(True)
                self.user_changing = False
                self.txt_nation_name.set_text("")
                self.user_changing = False
                self.cmbo_nation_capital.set_active(0)
                self.user_changing = False
                self.adj_nation_coin.set_value(0)
                self.user_changing = False
                self.adj_nation_men.set_value(0)
                self.user_changing = False
                self.txt_nation_colour.set_text("")
                self.user_changing = True

    def army_create(self,widget):
        position = str(self.tv_armies.get_cursor()[0])
        position = string.replace(position,")","")
        position = string.replace(position,",","")
        position = string.replace(position,"(","")
        position = int(position)
        if position == 0:
            army_id = len(self.armies)+1
            # self.armies[ARMY ID]:[(0)NAME,(1)HOME,(2)LOCATION,(3)INFANTRY,(4)ARCHERS,(5)CAVALRY]
            self.armies[army_id] = [self.txt_army_name.get_text(),self.cmbo_army_home.get_active(),self.cmbo_army_prov.get_active(),self.adj_army_inf.get_value(),self.adj_army_arch.get_value(),self.adj_army_cav.get_value()]
            print self.armies
            self.ls_armies.append([str(army_id)+": "+self.txt_army_name.get_text()])

    def update_armies(self,event):
        (model,pathlist) = self.ts_armies.get_selected_rows()
        for path in pathlist:
            self.iter = model.get_iter(path)
            value = model.get_value(self.iter,0)
            army_id = str(path)
            army_id = string.replace(army_id,"(","")
            army_id = string.replace(army_id,",","")
            army_id = string.replace(army_id,")","")
            army_id = int(army_id)
            self.army_selected = army_id+1
            if (army_id != 0):
                self.btn_army_new.set_sensitive(False)
                self.user_changing = False
                self.txt_army_name.set_text(self.armies[army_id][0])
                self.user_changing = False
                self.cmbo_army_home.set_active(self.armies[army_id][1])
                self.user_changing = False
                self.cmbo_army_prov.set_active(self.armies[army_id][2])
                self.user_changing = False
                self.adj_army_inf.set_value(self.armies[army_id][3])
                self.user_changing = False
                self.adj_army_arch.set_value(self.armies[army_id][4])
                self.user_changing = False
                self.adj_army_cav.set_value(self.armies[army_id][5])
                self.user_changing = True
            else:
                self.btn_army_new.set_sensitive(True)
                self.user_changing = False
                self.txt_army_name.set_text("")
                self.user_changing = False
                self.cmbo_army_home.set_active(0)
                self.user_changing = False
                self.cmbo_army_prov.set_active(0)
                self.user_changing = False
                self.adj_army_inf.set_value(0)
                self.user_changing = False
                self.adj_army_arch.set_value(0)
                self.user_changing = False
                self.adj_army_cav.set_value(0)
                self.user_changing = True

    def nation_create(self,widget):
        position = str(self.tv_nations.get_cursor()[0])
        position = string.replace(position,")","")
        position = string.replace(position,",","")
        position = string.replace(position,"(","")
        position = int(position)
        if position == 0:
            nation_id = len(self.nations)+1
            # self.nations[NATION ID]:[(0)NAME,(1)RGB,(2)CAPITAL,(3)COIN,(4)MEN,(5)[PROVINCES]]
            self.nations[nation_id] = [self.txt_nation_name.get_text(),self.txt_nation_colour.get_text(),self.cmbo_nation_capital.get_active()+1,self.adj_nation_coin.get_value(),self.adj_nation_men.get_value(),[]]
            print self.nations
            self.ls_nations.append([str(nation_id)+": "+self.txt_nation_name.get_text()])
            self.ls_prov_nation.append([str(nation_id)+": "+self.txt_nation_name.get_text()])


    def change_scen_provs(self,widget):
        if self.user_changing == True:
            self.provinces[self.selected_prov][0] = self.txt_prov_name.get_text()
            self.ls_scen_provs.set_value(self.iter, 0, str(self.selected_prov)+": "+self.provinces[self.selected_prov][0])
            self.provinces[self.selected_prov][5] = self.adj_prov_coin.get_value()
            self.provinces[self.selected_prov][6] = self.adj_prov_men.get_value()
            self.provinces[self.selected_prov][7] = self.cmbo_prov_owner.get_active()

    def change_armies(self,widget):
        if self.user_changing == True:
            self.armies[self.selected_army][0] = self.txt_prov_name.get_text()
            self.ls_armies.set_value(self.iter, 0, str(self.selected_army)+": "+self.armies[self.selected_army][0])
            self.armies[self.selected_army][1] = self.cmbo_army_home.get_active()+1
            self.armies[self.selected_army][2] = self.cmbo_army_prov.get_active()+1
            print self.cmbo_army_home.get_active()+1,self.cmbo_army_prov.get_active()+1
            self.armies[self.selected_army][3] = self.adj_inf.get_value()
            self.armies[self.selected_army][4] = self.adj_arch.get_value()
            self.armies[self.selected_army][5] = self.adj_cav.get_value()

            #self.armies[self.selected_army][7] = self.cmbo_prov_owner.get_active()

    def load_map(self,widget):
        if self.cmbo_maps.get_active() > 0:
            self.user_changing == False
            self.map = self.app_path+"/maps/"+self.maps[self.cmbo_maps.get_active()-1]
            tree = xml.parse(self.map)
            root = tree.getroot()
            self.lbl_map_name.set_text("Map Name: "+root.attrib["name"])

            self.map_region = root.attrib["region_map"]
            self.map_texture = root.attrib["texture_map"]

            self.adj_day.set_value(int(root.find("date/day").text))
            self.adj_month.set_value(int(root.find("date/month").text))
            self.adj_year.set_value(int(root.find("date/year").text))

            self.ls_map_provs.clear()
            self.ls_scen_provs.clear()
            self.provinces = {}
            self.nations = {}
            self.armies = {}
            for p in root.findall("province"):
                # self.provinces[PROVINCE ID]:[(0)NAME,(1)RGB,(2)X,(3)Y,(4)IMAGE,(5)COIN,(6)MEN,(7)NATION,(8)PATHS]
                self.provinces[int(p.attrib["id"])] = [p.find("name").text,p.find("rgb").text,int(p.find("x").text),int(p.find("y").text),None,1.0,1.0,0,[]]
                self.ls_map_provs.append([p.get("id")+": "+p.find("name").text])
                self.ls_scen_provs.append([p.get("id")+": "+p.find("name").text])
                paths = []
                self.all_paths = []
                for pth in root.findall("paths/path"):
                    self.all_paths.append(pth.attrib["name"])
                    pth_check = pth.attrib["name"]
                    pth_provs = string.replace(pth_check,"-"," ")
                    pth_provs = string.split(pth_provs)
                    if pth_provs[0] == p.attrib["id"]:
                        paths.append(int(pth_provs[1]))
                    elif pth_provs[1] == p.attrib["id"]:
                        paths.append(int(pth_provs[0]))
                self.provinces[int(p.attrib["id"])][8] = paths
                print self.provinces

            self.cmbo_nation_capital.set_active(0)
            self.tv_scen_provs.set_cursor(0)
        else:
            self.lbl_map_name.set_text("Map Name: ")

            self.map_region = ""
            self.map_texture = ""

            self.adj_day.set_value(1)
            self.adj_month.set_value(1)
            self.adj_year.set_value(1)

            self.ls_map_provs.clear()
            self.ls_scen_provs.clear()
            self.provinces = {}
            self.nations = {}
            self.armies = {}

    def save_scenario(self,widget):
        root = xml.Element("scenario")
        root.attrib["name"] = self.txt_scen_name.get_text()
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

        for n in range(len(self.nations)):
            # self.nations[NATION ID]:[(0)NAME,(1)RGB,(2)CAPITAL,(3)COIN,(4)MEN,(5)[PROVINCES],(6)FLAG]
            nation = xml.Element("nation")
            nation.attrib["id"] = str(n+1)
            nation.append(add_element("name",self.nations[n+1][0]))
            nation.append(add_element("rgb",self.nations[n+1][1]))
            nation.append(add_element("flag",None))
            nation.append(add_element("capital",str(self.nations[n+1][2])))
            nation.append(add_element("coin",str(int(self.nations[n+1][3]))))
            nation.append(add_element("men",str(int(self.nations[n+1][4]))))
            root.append(nation)

        for p in range(len(self.provinces)):
            prov = xml.Element("province")
            prov.attrib["id"] = str(p+1)
            prov.attrib["owner"] = str(self.provinces[p+1][7])
            prov.append(add_element("name",self.provinces[p+1][0]))
            prov.append(add_element("rgb",self.provinces[p+1][1]))
            prov.append(add_element("x",str(self.provinces[p+1][2])))
            prov.append(add_element("y",str(self.provinces[p+1][3])))
            prov.append(add_element("image",self.provinces[p+1][4]))
            prov.append(add_element("coin",str(self.provinces[p+1][5])))
            prov.append(add_element("men",str(self.provinces[p+1][6])))
            root.append(prov)

        for a in range(len(self.armies)):
            # self.nations[NATION ID]:[(0)NAME,(1)RGB,(2)CAPITAL,(3)COIN,(4)MEN,(5)[PROVINCES]]
            army = xml.Element("army")
            army.attrib["id"] = str(a+1)
            army.append(add_element("name",self.armies[a+1][0]))
            army.append(add_element("home",str(self.armies[a+1][1]+1)))
            army.append(add_element("location",str(self.armies[a+1][2]+1)))
            army.append(add_element("infantry",str(int(self.armies[a+1][3]))))
            army.append(add_element("archers",str(int(self.armies[a+1][4]))))
            army.append(add_element("cavalry",str(int(self.armies[a+1][5]))))
            root.append(army)

        e_paths = xml.Element("paths")
        for p in range(len(self.all_paths)):
            e_path = xml.Element("path")
            e_path.attrib["name"] = self.all_paths[p]
            e_paths.append(e_path)
        root.append(e_paths)

        dir = os.path.dirname(os.path.realpath(__file__))
        slash = "\ "
        slash = string.replace(slash," ","")
        dir = string.replace(dir, slash,"/")+"/"
        map = dir+"scenarios/"+self.txt_filename.get_text()+".xml"
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