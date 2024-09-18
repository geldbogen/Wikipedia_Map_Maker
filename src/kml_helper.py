import simplekml
import pandas as pd

class KmlHelper():
    def __init__(self, place_name : str, data_frame : pd.DataFrame) -> None:
        self.place_name = place_name
        self.data_frame = data_frame.iloc[::-1]
        self.kml = simplekml.Kml()
        self.kml.document.name = 'Unbenannte Karte'
        self.tiername_to_folder_dict = dict()
        self.final_to_replace_dict  : dict[str,str] = dict()


        self.test_normal_style = simplekml.Style()
        self.test_normal_style.iconstyle.color = 'ff000000'
        self.test_normal_style.iconstyle.icon.href = 'https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png'
        self.test_normal_style.labelstyle = simplekml.LabelStyle(0)
        self.test_normal_style.iconstyle.colormode = None
        self.test_normal_style.labelstyle.colormode = None


        self.test_highlight_style = simplekml.Style()
        self.test_highlight_style.iconstyle.color = 'ff000000'
        self.test_highlight_style.iconstyle.icon.href = 'https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png'
        self.test_highlight_style.labelstyle = simplekml.LabelStyle(1)
        self.test_highlight_style.iconstyle.colormode = None
        self.test_highlight_style.labelstyle.colormode = None
        self.test_normal_style._id = 'sadascsds'
        print(self.test_normal_style._id)



        self.test_stylemap = simplekml.StyleMap(normalstyle=self.test_normal_style,highlightstyle=self.test_highlight_style)

        # create folders for toggling on and off
        for tier_name in list(set(self.data_frame['tier'].to_list())):
            my_folder = self.kml.newfolder(name = tier_name)
            self.tiername_to_folder_dict[tier_name] = my_folder
        
        # create the styles
        self.style_graves = simplekml.Style()
        self.style_graves._id = 'icon-1556-FFD600-normal'

        self.style_S = simplekml.Style()
        self.style_S._id = 'icon-1739-E65100-normal'
        self.style_S.iconstyle.icon.href = 'https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png'

        # self.style_S.labelstyle = simplekml.LabelStyle(0)

        self.style_map_S = simplekml.StyleMap(normalstyle=self.style_S,)
        self.style_map_S._id = 'icon-1739-E65100'

        self.style_A = simplekml.Style()
        self.style_A._id = 'icon-1739-7CB342-normal'
        self.style_A.iconstyle.icon.href = 'https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png'

        self.style_map_A = simplekml.StyleMap(normalstyle=self.style_A)
        self.style_map_A._id = 'icon-1739-7CB342'


        self.style_B = simplekml.Style()
        self.style_B._id = 'icon-1739-9C27B0-normal'
        self.style_B.iconstyle.icon.href = 'https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png'

        self.style_map_B = simplekml.StyleMap(normalstyle=self.style_B)


        self.style_C = simplekml.Style()
        self.style_C._id = 'icon-1739-FFEA00-normal'
        self.style_C.iconstyle.icon.href = 'https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png'

        self.style_map_C = simplekml.StyleMap(normalstyle=self.style_C)


        self.style_D = simplekml.Style()
        self.style_D._id = 'icon-1739-0288D1-normal' 
        self.style_D.iconstyle.icon.href = 'https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png'

        self.style_map_D = simplekml.StyleMap(normalstyle=self.style_D)

        self.style_atlas_obscura = simplekml.Style()
        self.style_atlas_obscura._id = 'icon-1594-000000-normal' 
        self.style_atlas_obscura.iconstyle.icon.href = 'https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png'

        self.style_map_atlas_obscura = simplekml.StyleMap(normalstyle=self.style_atlas_obscura)
        
        self.style_graves = simplekml.Style()
        self.style_graves._id = 'icon-1556-FFD600-normal' 
        self.style_graves.iconstyle.icon.href = 'https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png'

        self.style_map_graves = simplekml.StyleMap(normalstyle=self.style_graves)

        
        self.style_wikivoyage_museums = simplekml.Style()
        self.style_wikivoyage_museums._id = 'icon-1636-0288D1-normal' 
        self.style_wikivoyage_museums.iconstyle.icon.href = 'https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png'

        self.style_map_wikivoyage_museums = simplekml.StyleMap(normalstyle=self.style_wikivoyage_museums)
        
        self.style_drink_normal = simplekml.Style()
        self.style_drink_normal._id = 'icon-1517-0288D1-normal' 
        self.style_drink_normal.iconstyle.icon.href = 'https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png'

        self.style_map_drink_normal = simplekml.StyleMap(normalstyle=self.style_drink_normal)

        self.style_drink_budget = simplekml.Style()
        self.style_drink_budget._id = 'icon-1517-0F9D58-normal' 
        self.style_drink_budget.iconstyle.icon.href = 'https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png'

        self.style_map_drink_budget = simplekml.StyleMap(normalstyle=self.style_drink_budget)
        
        self.style_drink_mid_range = simplekml.Style()
        self.style_drink_mid_range._id = 'icon-1517-FFEA00-normal' 
        self.style_drink_mid_range.iconstyle.icon.href = 'https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png'

        self.style_map_drink_mid_range = simplekml.StyleMap(normalstyle=self.style_drink_mid_range)

        self.style_drink_splurge = simplekml.Style()
        self.style_drink_splurge._id = 'icon-1517-FF5252-normal' 
        self.style_drink_splurge.iconstyle.icon.href = 'https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png'

        self.style_map_drink_splurge = simplekml.StyleMap(normalstyle=self.style_drink_splurge)

        self.style_eat_normal = simplekml.Style()
        self.style_eat_normal._id = 'icon-1577-0288D1-normal' 
        self.style_eat_normal.iconstyle.icon.href = 'https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png'

        self.style_map_eat_normal = simplekml.StyleMap(normalstyle=self.style_eat_normal)

        self.style_eat_budget = simplekml.Style()
        self.style_eat_budget._id = 'icon-1577-0F9D58-normal' 
        self.style_eat_budget.iconstyle.icon.href = 'https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png'

        self.style_map_eat_budget = simplekml.StyleMap(normalstyle=self.style_eat_budget)

        self.style_eat_midrange = simplekml.Style()
        self.style_eat_midrange._id = 'icon-1577-FFEA00-normal' 
        self.style_eat_midrange.iconstyle.icon.href = 'https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png'

        self.style_map_eat_midrange = simplekml.StyleMap(normalstyle=self.style_eat_midrange)

        self.style_eat_splurge = simplekml.Style()
        self.style_eat_splurge._id = 'icon-1577-FF5252-normal' 
        self.style_eat_splurge.iconstyle.icon.href = 'https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png'

        self.style_map_eat_splurge = simplekml.StyleMap(normalstyle=self.style_eat_splurge)

        self.style_sleep_normal = simplekml.Style()
        self.style_sleep_normal._id = 'icon-1602-0288D1-normal' 
        self.style_sleep_normal.iconstyle.icon.href = 'https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png'

        self.style_map_sleep_normal = simplekml.StyleMap(normalstyle=self.style_sleep_normal)

        self.style_sleep_budget = simplekml.Style()
        self.style_sleep_budget._id = 'icon-1602-0F9D58-normal' 
        self.style_sleep_budget.iconstyle.icon.href = 'https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png'

        self.style_map_sleep_budget = simplekml.StyleMap(normalstyle=self.style_sleep_budget)

        self.style_sleep_midrange = simplekml.Style()
        self.style_sleep_midrange._id = 'icon-1602-FFEA00-normal' 
        self.style_sleep_midrange.iconstyle.icon.href = 'https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png'

        self.style_map_sleep_midrange = simplekml.StyleMap(normalstyle=self.style_sleep_midrange)

        self.style_sleep_splurge = simplekml.Style()
        self.style_sleep_splurge._id = 'icon-1602-FF5252-normal' 
        self.style_sleep_splurge.iconstyle.icon.href = 'https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png'

        self.style_map_sleep_splurge = simplekml.StyleMap(normalstyle=self.style_sleep_splurge)

        self.style_see = simplekml.Style()
        self.style_see._id = 'icon-1502-0288D1-normal' 
        self.style_see.iconstyle.icon.href = 'https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png'

        self.style_map_see = simplekml.StyleMap(normalstyle=self.style_see)

        self.style_see_parks = simplekml.Style()
        self.style_see_parks._id = 'icon-1720-0288D1-normal' 
        self.style_see_parks.iconstyle.icon.href = 'https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png'

        self.style_map_see_parks = simplekml.StyleMap(normalstyle=self.style_see_parks)

        self.style_see_landmarks = simplekml.Style()
        self.style_see_landmarks._id = 'icon-1591-0288D1-normal' 
        self.style_see_landmarks.iconstyle.icon.href = 'https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png'

        self.style_map_see_landmarks = simplekml.StyleMap(normalstyle=self.style_see_landmarks)

        self.style_see_temples = simplekml.Style()
        self.style_see_temples._id = 'icon-1706-0288D1-normal' 
        self.style_see_temples.iconstyle.icon.href = 'https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png'

        self.style_map_see_temples = simplekml.StyleMap(normalstyle=self.style_see_temples)

        self.style_see_churches = simplekml.Style()
        self.style_see_churches._id = 'icon-1670-0288D1-normal' 
        self.style_see_churches.iconstyle.icon.href = 'https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png'

        self.style_map_see_churches = simplekml.StyleMap(normalstyle=self.style_see_churches)

        self.style_by_train = simplekml.Style()
        self.style_by_train._id = 'icon-1716-0288D1-normal' 
        self.style_by_train.iconstyle.icon.href = 'https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png'

        self.style_map_by_train = simplekml.StyleMap(normalstyle=self.style_by_train)

        self.style_by_plane = simplekml.Style()
        self.style_by_plane._id = 'icon-1504-0288D1-normal' 
        self.style_by_plane.iconstyle.icon.href = 'https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png'

        self.style_map_by_plane = simplekml.StyleMap(normalstyle=self.style_by_plane)

        self.style_by_bus = simplekml.Style()
        self.style_by_bus._id = 'icon-1532-0288D1-normal' 
        self.style_by_bus.iconstyle.icon.href = 'https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png'

        self.style_map_by_bus = simplekml.StyleMap(normalstyle=self.style_by_bus)

        self.style_by_boat = simplekml.Style()
        self.style_by_boat._id = 'icon-1569-0288D1-normal' 
        self.style_by_boat.iconstyle.icon.href = 'https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png'

        self.style_map_by_boat = simplekml.StyleMap(normalstyle=self.style_by_boat)





        # create dummy point
        self.dummy_point = self.kml.newpoint()
        self.dummy_point.stylemap = self.style_map_S
        self.dummy_point.stylemap = self.style_map_A
        self.dummy_point.stylemap = self.style_map_B
        self.dummy_point.stylemap = self.style_map_C
        self.dummy_point.stylemap = self.style_map_D
        self.dummy_point.stylemap = self.style_map_atlas_obscura
        self.dummy_point.stylemap = self.style_map_wikivoyage_museums

        self.dummy_point.stylemap = self.style_map_eat_normal
        self.dummy_point.stylemap = self.style_map_eat_budget
        self.dummy_point.stylemap = self.style_map_eat_midrange
        self.dummy_point.stylemap = self.style_map_eat_splurge


        self.dummy_point.stylemap = self.style_map_drink_normal
        self.dummy_point.stylemap = self.style_map_drink_budget
        self.dummy_point.stylemap = self.style_map_drink_mid_range
        self.dummy_point.stylemap = self.style_map_drink_splurge

        self.dummy_point.stylemap = self.style_map_sleep_normal
        self.dummy_point.stylemap = self.style_map_sleep_budget
        self.dummy_point.stylemap = self.style_map_sleep_midrange
        self.dummy_point.stylemap = self.style_map_sleep_splurge

        self.dummy_point.stylemap = self.style_map_see
        self.dummy_point.stylemap = self.style_map_see_churches
        self.dummy_point.stylemap = self.style_map_see_landmarks
        self.dummy_point.stylemap = self.style_map_see_parks
        self.dummy_point.stylemap = self.style_map_see_temples

        self.dummy_point.stylemap = self.style_map_by_boat
        self.dummy_point.stylemap = self.style_map_by_bus
        self.dummy_point.stylemap = self.style_map_by_plane
        self.dummy_point.stylemap = self.style_map_by_train






        self.data_frame.apply(lambda x: self.create_styled_point(x), axis=1)
        self.kml.save(f'data/{self.place_name}/{self.place_name}.kml')


        # self.replace_kml_id_in_string('2','icon-1594-000000-normal')
        # self.replace_kml_id_in_string('6','icon-1594-000000-highlight')
        # self.replace_kml_id_in_string('10','icon-1594-000000')

        # remove first folder, in which simplekml automatically stores the files:
        # self.string_data = self.string_data.replace('<Folder id="11">','',1)
        # self.string_data = self.string_data.replace('</Folder>','',1)

    def style_the_point(self, pd_series : pd.Series) -> simplekml.StyleMap:
        match pd_series.at['tier']:
            case 'S':
                return self.style_map_S
            case 'A':
                return self.style_map_A
            case 'B':
                return self.style_map_B
            case 'C':
                return self.style_map_C
            case 'D':
                return self.style_map_D
            case 'atlas_obscura':
                return self.style_map_atlas_obscura
            case 'wikivoyage':
                match pd_series.at['thingLabel']:
                    case 'See_Museums and art galleries':
                        return self.style_map_wikivoyage_museums
                    # eat categories
                    case _ if pd_series.at['thingLabel'].startswith('Eat'):
                        match pd_series.at['thingLabel']:
                            case _ if 'Budget' in pd_series.at['thingLabel']:
                                return self.style_map_eat_budget
                            case _ if 'Mid-range' in pd_series.at['thingLabel']:
                                return self.style_map_eat_midrange
                            case _ if 'Splurge' in pd_series.at['thingLabel']:
                                return self.style_map_eat_splurge
                            case _:
                                return self.style_map_eat_normal
                    case _ if pd_series.at['thingLabel'].startswith('Sleep'):
                        match pd_series.at['thingLabel']:
                            case _ if 'Budget' in pd_series.at['thingLabel']:
                                return self.style_map_sleep_budget
                            case _ if 'Mid-range' in pd_series.at['thingLabel']:
                                return self.style_map_sleep_midrange
                            case _ if 'Splurge' in pd_series.at['thingLabel']:
                                return self.style_map_sleep_splurge
                            case _:
                                return self.style_map_sleep_normal
                    case _ if pd_series.at['thingLabel'].startswith('Get in'):
                        match pd_series.at['thingLabel']:
                            case _ if 'By plane' in pd_series.at['thingLabel']:
                                return self.style_map_by_plane
                            case _ if 'By train' in pd_series.at['thingLabel']:
                                return self.style_map_by_train
                            case _ if 'By bus' in pd_series.at['thingLabel']:
                                return self.style_map_by_bus
                            case _ if 'By boat' in pd_series.at['thingLabel']:
                                return self.style_map_by_boat
                    case _ if pd_series.at['thingLabel'].startswith('See'):
                        match pd_series.at['thingLabel']:
                            case _ if 'Churches' in pd_series.at['thingLabel']:
                                return self.style_map_see_churches
                            case _ if 'Landmarks' in pd_series.at['thingLabel']:
                                return self.style_map_see_landmarks
                            case _ if 'Parks' in pd_series.at['thingLabel']:
                                return self.style_map_see_parks
                            case _ if 'Temples' in pd_series.at['thingLabel']:
                                return self.style_map_see_temples
                            case _:
                                return self.style_map_see

        return self.style_map_D
    
    def get_description(self, pd_series : pd.Series) -> str:
        match pd_series.at['tier']:
            case 'atlas_obscura':
                description = f'''{pd_series['description']} <br> <br> {pd_series['ao_link']}'''
            case _ if 'wikivoyage' in pd_series.at['tier']:
                description = f'''
                category  : {pd_series.at['thingLabel']} <br>
                address  : {pd_series.at['address']} <br>
                url  : {pd_series.at['url']} <br>
                description  : {pd_series.at['description']} <br>
                '''
            case _:
                description = f'''\
                    category  : {pd_series.at['thingLabel']} <br>   
                    sitelinks : {pd_series.at['sitelinks']} <br>   
                    articleEN : {pd_series.at['articleEN']} <br>             
                    articleDE : {pd_series.at['articleDE']} <br>              
                    wikidata_link : {pd_series.at['item']}'''     
        return description

        # new_frame = pd.DataFrame({'category' : self.data_frame.columns.to_list(), 'value' : pd_series.to_list()})
        # print(new_frame.to_string(index=False,na_rep='',line_width=45))
        # return new_frame.to_string(index=False, na_rep='', line_width=45)
        
    def create_styled_point(self, pd_series : pd.Series):
        kml_folder : simplekml.Folder = self.tiername_to_folder_dict[pd_series.at['tier']]
        kml_point = kml_folder.newpoint(name = pd_series.at['itemLabel'], coords = [(pd_series.at['lon'], pd_series.at['lat'])], description = self.get_description(pd_series))
        kml_point.stylemap = self.style_the_point(pd_series)

        pass

    def replace_kml_id_in_string(self, old_id : str, new_id: str):
        # replace defintions
        self.string_data = self.string_data.replace(f'"{old_id}"', f'"{new_id}"')
        # replace mentions
        self.string_data = self.string_data.replace(f'#{old_id}', f'#{new_id}')

