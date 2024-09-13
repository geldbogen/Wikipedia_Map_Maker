import simplekml
import pandas as pd

class KmlHelper():
    def __init__(self, place_name : str, data_frame : pd.DataFrame) -> None:
        self.place_name = place_name
        self.data_frame = data_frame
        self.kml = simplekml.Kml()
        self.kml.document.name = 'Unbenannte Karte'
        self.tiername_to_folder_dict = dict()


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



        self.test_stylemap = simplekml.StyleMap(normalstyle=self.test_normal_style,highlightstyle=self.test_highlight_style)

        # create folders for toggling on and off
        for tier_name in list(set(self.data_frame['tier'].to_list())):
            my_folder = self.kml.newfolder(name = tier_name)
            self.tiername_to_folder_dict[tier_name] = my_folder
        
        # create the styles
        self.style_S = simplekml.IconStyle()
        self.style_S.color = 'ff9900'
        self.style_S.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'
        self.style_A = simplekml.IconStyle()
        self.style_A.color = '009900' 

        self.style_B = simplekml.IconStyle()
        self.style_B.color = '6600cc'
        self.style_C = simplekml.IconStyle()
        self.style_C.color = 'ffff00'
        self.style_C.icon.href ='http://maps.google.com/mapfiles/kml/shapes/target.png'
        self.style_D = simplekml.IconStyle()
        self.style_D.color = '0066ff' 


        self.data_frame.apply(lambda x: self.create_styled_point(x), axis=1)
        self.kml.save(f'data/{self.place_name}/{self.place_name}.kml')

        with open(f'data/{self.place_name}/{self.place_name}.kml', 'r') as f:
            self.string_data = f.read()

        self.replace_kml_id_in_string('2','icon-1594-000000-normal')
        self.replace_kml_id_in_string('6','icon-1594-000000-highlight')
        self.replace_kml_id_in_string('10','icon-1594-000000')

        # remove first folder, in which simplekml automatically stores the files:
        self.string_data = self.string_data.replace('<Folder id="11">','',1)
        self.string_data = self.string_data.replace('</Folder>','',1)

        with open(f'data/{self.place_name}/{self.place_name}.kml', 'w') as f:
            f.write(self.string_data)



    def get_style(self, pd_series : pd.Series) -> simplekml.IconStyle:
        match pd_series.at['tier']:
            case 'S':
                return self.style_S
            case 'A':
                return self.style_A
            case 'B':
                return self.style_B
            case 'C':
                return self.style_C
            case 'D':
                return self.style_D
        return self.style_D
    
    def get_description(self, pd_series : pd.Series) -> str:
        match pd_series.at['tier']:
            case 'atlas_obscura':
                description = f'''{pd_series['description']} <br> <br> {pd_series['link']}'''
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
        # kml_point.iconstyle = self.get_style(pd_series)
        kml_point.style = self.test_normal_style
    pass

    def replace_kml_id_in_string(self, old_id : str, new_id: str):
        # replace defintions
        self.string_data = self.string_data.replace(f'"{old_id}"', f'"{new_id}"')
        # replace mentions
        self.string_data = self.string_data.replace(f'#{old_id}', f'#{new_id}')

