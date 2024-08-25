import simplekml
import pandas as pd

class KmlHelper():
    def __init__(self, data_frame : pd.DataFrame) -> None:
        self.data_frame = data_frame
        self.kml = simplekml.Kml()
        self.tiername_to_folder_dict = dict()

        # create folders for toggling on and off
        for tier_name in list(set(self.data_frame['tier'].to_list())):
            my_folder = self.kml.newfolder(name = tier_name)
            self.tiername_to_folder_dict[tier_name] = my_folder
        
        # create the styles
        self.style_S = simplekml.Style()
        self.style_S.iconstyle.color = '#ff9900'
        self.style_S.iconstyle.href = ''
        self.style_A = simplekml.Style()
        self.style_A.iconstyle.color = '#009900' 
        self.style_B = simplekml.Style()
        self.style_B.iconstyle.color = '#6600cc'
        self.style_C = simplekml.Style()
        self.style_C.iconstyle.color = '#ffff00'
        self.style_D = simplekml.Style()
        self.style_D.iconstyle.color = '#0066ff' 


        self.data_frame.apply(lambda x: self.create_styled_point(x),axis=1)
        self.kml.save('mumbai.kml')



        
    def get_style(self, pd_series : pd.Series) -> simplekml.Style:
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
                description = f'''{pd_series['ao_description']} <br> <br> {pd_series['ao_link']}'''
            case _:
                description = f'''\
                    category  : {pd_series.at['thingLabel']} <br>   \
                    sitelinks : {pd_series.at['sitelinks']} <br>   \
                    articleEN : {pd_series.at['articleEN']} <br>             \
                    articleDE : {pd_series.at['articleDE']} <br>              \
                    wikidata_link : {pd_series.at['item']}'''     
        return description

        # new_frame = pd.DataFrame({'category' : self.data_frame.columns.to_list(), 'value' : pd_series.to_list()})
        # print(new_frame.to_string(index=False,na_rep='',line_width=45))
        # return new_frame.to_string(index=False, na_rep='', line_width=45)
        
    def create_styled_point(self, pd_series : pd.Series):
        kml_folder : simplekml.Folder = self.tiername_to_folder_dict[pd_series.at['tier']]
        kml_point = kml_folder.newpoint(name = pd_series.at['itemLabel'], coords = [(pd_series.at['lon'], pd_series.at['lat'])], description = self.get_description(pd_series))
        kml_point.style = self.get_style(pd_series)
    pass

