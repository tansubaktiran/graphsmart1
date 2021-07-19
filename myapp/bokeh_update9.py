import random
from bokeh.models.tools import Toolbar
import pandas
import numpy as np
import pandas as pd

import pandas
from bokeh.layouts import layout
from bokeh.models.glyphs import Circle
from bokeh.models.sources import ColumnDataSource
from bokeh.plotting import figure, output_file, save
from bokeh.io import curdoc, show
from numpy import source
import pandas

from bokeh.models import Range1d, PanTool, ResetTool, HoverTool, Band, Toggle
from bokeh.models.annotations import Label, LabelSet
from bokeh.models.widgets import Slider
from bokeh.layouts import gridplot
from bokeh.io import curdoc
from bokeh.transform import dodge
from math import pi



df8 = pd.DataFrame(np.random.randint(100,200,size=(80, 1)), columns=list('A'))
df = pd.DataFrame(np.random.randint(50,100,size=(80, 1)), columns=list('B'))
df2 = pd.DataFrame(np.random.randint(80,160,size=(80, 1)), columns=list('C'))
df3 = pd.DataFrame(np.random.randint(40, 120,size=(80, 1)), columns=list('D'))
df4 = pd.DataFrame(np.random.randint(60,200,size=(80, 1)), columns=list('E'))
df5 = pd.DataFrame(np.random.randint(350,400,size=(80, 1)), columns=list('F'))
df6 = pd.DataFrame(np.random.randint(400,600,size=(80, 1)), columns=list('G'))
df7 = pd.DataFrame(np.random.randint(40,100,size=(80, 1)), columns=list('H'))
df9 = pd.DataFrame(np.random.randint(4,10,size=(80, 1)), columns=list('M')) #For Motivation Column
df10 = pd.DataFrame(np.random.randint(3,10,size=(80, 1)), columns=list('P')) #For Potential Column


#I needed to declare a seperate myindex column made of strings as values of the index 
# to be able to include this column as x_range values in the CDS and bokeh plots
mylist = []
for n in range(80):
    mylist.append(str(n))
dfindex = pandas.DataFrame({"myindex": mylist})

frames = [dfindex, df8, df, df2, df3, df4, df5, df6, df7, df9, df10]
data = pd.concat(frames, axis=1)

data["PR1_DIFF"] = data["D"] - data["B"]
data["PR1_PERC"] = data["PR1_DIFF"]/data["B"]
data["PR1_PERC"] = data["PR1_PERC"].round(decimals=2)

data["PR2_DIFF"] = data["E"] - data["C"]
data["PR2_PERC"] = data["PR2_DIFF"]/data["C"]
data["PR2_PERC"] = data["PR2_PERC"].round(decimals=2)

data["OFFER_CONV"] = (data["H"]/data["G"])
data["OFFER_CONV"] = data["OFFER_CONV"].round(decimals=2)
#data["OFFER_CONV"] = data.round({"OFFER_CONV" :2})
#df.round({'dogs': 1, 'cats': 0})
data["OFFER_CONV_STR"] = data["OFFER_CONV"].astype(str)
#df['Marks'] = df['Marks'].astype(str)

data.insert(4, "B+C", (data["B"] + data["C"]))
data.insert(7, "D+E", (data["D"] + data["E"]))

data["TOTAL_DIFF"] = data["PR1_DIFF"] + data["PR2_DIFF"]

#print(data.head(10))
# Assigning two columns for drawing the plots. 
# These will be used for updating purposes in the update-functions later
data["PLOT1"] = data["D"]
data["PLOT2"] = data["B"]
data["PLOT3"] = data["E"]
data["PLOT4"] = data["C"]

data["Tot_Rev_Perc"] = (data["D+E"]-data["B+C"])/data["B+C"] #burada kaldık...12.07.2021 13:54
data["Tot_Rev_Perc"] = data["Tot_Rev_Perc"].round(decimals=2)

data["COLOR"] = ["orange" if (value<=0 and value>-.25) 
                    else "lime" if (value>0 and value<.25) 
                    else "green" if (value>=0.25 and value<.50)
                    else "red" if (value<=-.25 and value>-.50) 
                    else "darkred" if (value<=-0.50) 
                    else "darkgreen" for value in data["Tot_Rev_Perc"]]



#print(data.head(10))
prev_tot_offers = (data["F"]).sum()
current_tot_offers = (data["G"]).sum()
current_accepted_offers = (data["H"]).sum()
current_to_prev_offers_perc = current_tot_offers/prev_tot_offers
current_conv_rate = current_accepted_offers/current_tot_offers

current_to_prev_offers_perc = current_to_prev_offers_perc.round(decimals=2)
current_conv_rate = current_conv_rate.round(decimals=2)

#print(current_to_prev_offers_perc, current_conv_rate)



n= len(data)
m = 80
k = 80


#For creating a summary table for showing the sums - There should be a much better way to do this.
#Clean and tidy up this part
Tot_sum = data.sum()
A_sum = Tot_sum.iloc[1:8]
B_sum = Tot_sum.iloc[8:11]
A_values = A_sum.values
B_values = B_sum.values
#A_index = A_sum.index.values
#B_index = B_sum.index.values
A_index = ["Prev. Per. Sales Rev.", "Pr.1 Sales Targ.", "Pr.2 Sales Targ.", "Tot. Cur. Sales Targ.", 
"Pr.1 Sales Rev.", "Pr.2 Sales Rev.", "Tot. Cur. Sales Rev."]

B_index = ["Prev. Offer Counts", "Cur. Offer Counts", "Cur. Converted Offers"]
data_test = {'names': A_index,
        'values': A_values}
data_test2 = {'names2':B_index,
        'values2': B_values}

    
source_summary = ColumnDataSource(data_test) #Create the summary graph
source_summary2 = ColumnDataSource(data_test2) #Create the summary graph
#print(source_summary.data)

f2 = figure(x_range=source_summary.data["names"])
f2.vbar(x=dodge("names", -.05, range=f2.x_range) , top="values", width=.5, color="orangered", fill_alpha=.5,  source=source_summary)

#f.vbar(x=dodge("REGION",-0.20, range=f.x_range), top="TOTAL COLLECTED AMOUNT", 
#color="green", fill_alpha=.6,  width=.1, source=source, legend_label="Total Of Collected Amounts in Current Period")

labels7 = LabelSet(x="names", y="values", text="values", text_font_size= "6pt", angle=pi/4, x_offset=-5, y_offset=-5,  source=source_summary)
f2.add_layout(labels7)

f2.xaxis.major_label_orientation = pi/4
f2.xaxis.major_label_text_font_size = "6pt"

f3 = figure(x_range=source_summary2.data["names2"])
f3.vbar(x="names2" , top="values2", width=.5, color="lime", fill_alpha=.5,  source=source_summary2)

labels8 = LabelSet(x="names2", y="values2", text="values2", text_font_size= "6pt",  source=source_summary2)
f3.add_layout(labels8)

f3.xaxis.major_label_orientation = pi/4
f3.xaxis.major_label_text_font_size = "6pt"

#add description label
Explanation_offer_trend = "Prev. to cur. total trend offer = " + str(current_to_prev_offers_perc)
description_offer_trend=Label(x=0,y=12000,text=Explanation_offer_trend, text_font_size= "6pt", render_mode="css")
f3.add_layout(description_offer_trend)

Explanation_conversion = "Conv. Rate = " + str(current_conv_rate)
description_conversion=Label(x=0,y=10000,text=Explanation_conversion, text_font_size= "6pt", render_mode="css")
f3.add_layout(description_conversion)

#show(f2)
#Clean and tidy up this part - END OF THIS PART


source = ColumnDataSource(data)
source_display = ColumnDataSource(data)

#Create a column(apart from index values) for using in the x_range...

#Toolbar will be added to the figure!!!
f = figure(x_range=source_display.data["myindex"], toolbar_location="below")

f.xaxis.major_label_orientation = pi/6
f.xaxis.major_label_text_font_size = "6pt"

f.vbar(x=dodge("myindex", -0.10, range=f.x_range), top="PLOT1", color="blue", 
width=.4, fill_alpha=.5, legend_label="PR 1 Sales Rev", source=source_display)
f.vbar(x=dodge("myindex", 0.05, range=f.x_range), top="PLOT3", color="deepskyblue", 
width=.3, fill_alpha=.7, legend_label="PR 2 Sales Rev",  source=source_display)
f.vbar(x=dodge("myindex", 0.15, range=f.x_range), top="D+E", color="COLOR",  
width=.1, fill_alpha=.8, legend_label="Total Sales Rev", source=source_display)
#D ve E

#f.circle(x= "myindex", y="B", size = 10, color="navy", fill_alpha=0.5, source=source_display) Burasını değiştirdim.

#BURADAYIIIIIIZ!!!
#f = figure(x_range=source_display.data["myindex"], toolbar_location="below")
# level parameters:  image, underlay, glyph, annotation or overlay
guide1 = f.vbar(x= "myindex", top="PLOT2", color="purple", width=.06, fill_alpha=.2, line_color=None, visible= False, level="underlay",  source=source_display)
f.add_layout(guide1)
#________________popup

f.tools=[PanTool(), ResetTool()]
hover=HoverTool(tooltips=
"""
     <div>            
            <div>
                <span style="font-size: 15px; font-weight: bold;"><b>Offer Conv. Perc.: </b>@OFFER_CONV_STR</span>
            </div>
            <div>
                <span style="font-size:10px; color: #FF0000;"><b>Last year total offer</b></span> @F<br>
                <span style="font-size: 10px; color: #696;"><b>This year total offer: </b> @G</span>
                <span style="font-size: 10px; color: #696;"><b>This year total accepted: </b> @H</span>
            </div>
        </div>
""")
f.add_tools(hover)

#________________popup


test_graph = f.circle(x=dodge("myindex", -0.15, range=f.x_range), y="PLOT2", size = 6, color="navy", 
fill_alpha=0.5, legend_label="PR1 Sales Target", source=source_display)
f.add_layout(test_graph)
test_graph2 = f.circle(x=dodge("myindex", 0.05, range=f.x_range),  y="PLOT4", size = 6, color="orangered", 
legend_label="PR2 Sales Target", fill_alpha=0.5, source=source_display)
f.add_layout(test_graph2)


label1 = LabelSet(x="myindex", y="D+E", text="Tot_Rev_Perc", text_font_size = "6pt", x_offset= 2, y_offset= -5, source=source_display)
f.add_layout(label1)

label2 = LabelSet(x="myindex", y="D+E", text="M", text_font_size = "5pt", text_color="orangered", x_offset= -4, y_offset= 5, visible=False, source=source_display)
f.add_layout(label2)
label3 = LabelSet(x="myindex", y="D+E", text="P", text_font_size = "5pt", text_color="green", x_offset= 4, y_offset= 5, visible=False, source=source_display)
f.add_layout(label3)

#f.y_range = Range1d(start=0, end=200)


f.legend.background_fill_alpha = 0.1
f.legend.margin = 2
f.legend.padding = 2
f.legend.click_policy="hide"
f.legend.location = 'top_left'
f.legend.orientation = "horizontal"
f.legend.label_text_font_size = "7pt"


myslider = Slider(title="Budget - Actual Percent Difference Slider / PR No:1", value=0.0, start=-.50, end=1.1, step=.05)

# label will be edited here
explanation1 = " Sales Experts in this category : " + str(n) + " ---percent value : " + str(n/m)
description=Label(x=0, y=-70, text=explanation1 ,render_mode="css", text_font_size="12pt", 
text_color='orangered', text_alpha=1, text_baseline='bottom', text_align='left',
background_fill_color='white', background_fill_alpha=0.2, text_line_height=40)
f.add_layout(description)
# label is edited above

def update_graph(attrname, old, new):
    global n, m
    source_display.data = {key: [val for i,val in enumerate(source.data[key])
    if source.data["Tot_Rev_Perc"][i]<=float(myslider.value)] for key in source.data} #Most important part of the function and the code.
    f.x_range.factors = source_display.data["myindex"] 
    #Also very important part of this function 
    #and the code for updating the x_range dynamically
    f.x_range.factors = source_display.data["myindex"]
    n= len(source_display.data["myindex"])
    
    #Round fonksiyonunu buraya alalım... .round(decimals=2)
    description.text = "Sales Experts in this category : " + str(n) + " ---percent value : " + str((n/m))


    #print(source_display.data["COL2"])
    
    #source.data = {key: [value for i, value in enumerate(source.data[key])
    #if source.data["COL1"][i]>=int(myslider.value)] for key in source.data}
    #burada kaldık :)
    #print(myslider.value)

n=0
def show_less_than_0(arg):
    global n
    source_display.data = {key: [val for i,val in enumerate(source.data[key])
    if source.data["Tot_Rev_Perc"][i]<0] for key in source.data} #Most important part of the function and the code.
    f.x_range.factors = source_display.data["myindex"]
    n= len(source_display.data["myindex"])
    description.text = " Sales Experts in this category : " + str(n)



def show_bw_mn25_0(arg):
    global n
    source_display.data = {key: [val for i,val in enumerate(source.data[key])
    if (source.data["Tot_Rev_Perc"][i]<0) and (source.data["Tot_Rev_Perc"][i]>=-0.25)] for key in source.data} #Most important part of the function and the code.
    f.x_range.factors = source_display.data["myindex"]
    guide1.visible = False
    #f.y_range.factors = Range1d(start=0, end=200)
    n= len(source_display.data["myindex"])
    description.text = " Sales Experts in this category : " + str(n)

def show_bw_mn50_25(arg):
    global n
    source_display.data = {key: [val for i,val in enumerate(source.data[key])
    if (source.data["Tot_Rev_Perc"][i]<-0.25) and (source.data["Tot_Rev_Perc"][i]>=-0.5) ] for key in source.data} #Most important part of the function and the code.
    f.x_range.factors = source_display.data["myindex"]
    n= len(source_display.data["myindex"])
    description.text = " Sales Experts in this category : " + str(n)

def show_less_than_mn50(arg):
    global n
    source_display.data = {key: [val for i,val in enumerate(source.data[key])
    if (source.data["Tot_Rev_Perc"][i]<-0.5) ] for key in source.data} #Most important part of the function and the code.
    f.x_range.factors = source_display.data["myindex"]
    n= len(source_display.data["myindex"])
    description.text = " Sales Experts in this category : " + str(n)

def show_more_than_zero(arg):
    global n
    source_display.data = {key: [val for i,val in enumerate(source.data[key])
    if (source.data["Tot_Rev_Perc"][i]>=0) ] for key in source.data} #Most important part of the function and the code.
    f.x_range.factors = source_display.data["myindex"]
    n= len(source_display.data["myindex"])
    description.text = " Sales Experts in this category : " + str(n)


def show_bw_0_pl25(arg):
    global n
    source_display.data = {key: [val for i,val in enumerate(source.data[key])
    if (source.data["Tot_Rev_Perc"][i]>=0) and (source.data["Tot_Rev_Perc"][i]<.25) ] for key in source.data} #Most important part of the function and the code.
    f.x_range.factors = source_display.data["myindex"]
    n= len(source_display.data["myindex"])
    description.text = " Sales Experts in this category : " + str(n)

def show_bw_pl25_50(arg):
    global n
    source_display.data = {key: [val for i,val in enumerate(source.data[key])
    if (source.data["Tot_Rev_Perc"][i]>=.25) and (source.data["Tot_Rev_Perc"][i]<.50) ] for key in source.data} #Most important part of the function and the code.
    f.x_range.factors = source_display.data["myindex"]
    n= len(source_display.data["myindex"])
    description.text = " Sales Experts in this category : " + str(n)

def show_more_than_pl50(arg):
    global n
    source_display.data = {key: [val for i,val in enumerate(source.data[key])
    if (source.data["Tot_Rev_Perc"][i]>=0.5) ] for key in source.data} #Most important part of the function and the code.
    f.x_range.factors = source_display.data["myindex"]
    n= len(source_display.data["myindex"])
    description.text = " Sales Experts in this category : " + str(n)

def show_all(arg):
    global n
    source_display.data = {key: [val for i,val in enumerate(source.data[key])
    if (source.data["Tot_Rev_Perc"][i]>=0) or (source.data["Tot_Rev_Perc"][i]<0) ] for key in source.data} #Most important part of the function and the code.
    f.x_range.factors = source_display.data["myindex"]
    n= len(source_display.data["myindex"])
    description.text = " Sales Experts in this category : " + str(n)

def Show_tot_diff_more_than_zero(arg):
    global n
    source_display.data = {key: [val for i,val in enumerate(source.data[key])
    if (source.data["TOTAL_DIFF"][i]>=0)] for key in source.data} #Most important part of the function and the code.
    f.x_range.factors = source_display.data["myindex"]
    n= len(source_display.data["myindex"])
    description.text = " Sales Experts in this category : " + str(n)

def Show_both_diff_equal_or_positive(arg):
    global n
    source_display.data = {key: [val for i,val in enumerate(source.data[key])
    if (source.data["PR1_DIFF"][i]>=0) and (source.data["PR2_DIFF"][i]>=0)] for key in source.data} #Most important part of the function and the code.
    f.x_range.factors = source_display.data["myindex"]
    n= len(source_display.data["myindex"])
    description.text = " Sales Experts in this category : " + str(n)


def G_column_test(arg):
    #global n, f, test_graph
    #test_graph = f.circle(x= "myindex", y="G", size = 10, color="lime", fill_alpha=0.5, source=source_display)
    #f.add_layout(test_graph)
    #print(source_display.data["B"])
    source_display.data["PLOT2"] = source_display.data["G"]
    guide1.visible = True
    
    #print(source_display.data["B"])
    #source_display.data = {key: [val for i,val in enumerate(source.data[key])
    #if (source.data["PR1_PERC"][i]>=0) ] for key in source.data} #Most important part of the function and the code.
    #f.x_range.factors = source_display.data["myindex"]
    #n= len(source_display.data["myindex"])
    #description.text = " Offer values should be displayed here.. : " + str(n)


def Show_mot_and_pot(arg):
    label2.visible = not(label2.visible)
    label3.visible = not(label3.visible)


myslider.on_change('value', update_graph)
toggle1 = Toggle(label="Show realisations less than zero", button_type="warning", background="blue", active=True)
toggle1.on_click(show_less_than_0)

toggle2 = Toggle(label="Show realisations between minus 25% to 0", button_type="warning", active=True)
toggle2.on_click(show_bw_mn25_0)

toggle3 = Toggle(label="Show realisations between minus 50 - 25 %", button_type="danger", active=True)
toggle3.on_click(show_bw_mn50_25)

toggle4 = Toggle(label="Show realisations less than minus 50 %", button_type="danger", active=True)
toggle4.on_click(show_less_than_mn50)

toggle5 = Toggle(label="Show realisations more than zero", button_type="success", active=True)
toggle5.on_click(show_more_than_zero)

toggle6 = Toggle(label="Show realisations between zero and 25 %", button_type="success", active=True)
toggle6.on_click(show_bw_0_pl25)

toggle7 = Toggle(label="Show realisations between 25 and 50 %", button_type="success", active=True)
toggle7.on_click(show_bw_pl25_50)

toggle8 = Toggle(label="Show realisations more than 50 %", button_type="success", active=True)
toggle8.on_click(show_more_than_pl50)

toggle9 = Toggle(label="Show All", button_type="default", active=True)
toggle9.on_click(show_all)

toggle10 = Toggle(label="G column test", button_type="light", active=True)
toggle10.on_click(G_column_test)

toggle11 = Toggle(label="Show total difference", button_type="success", active=True)
toggle11.on_click(Show_tot_diff_more_than_zero)


toggle12 = Toggle(label="Show both pr diff as positive", button_type="success", active=True)
toggle12.on_click(Show_both_diff_equal_or_positive)

toggle13 = Toggle(label="Show Motivation and Potential Values ", button_type="light", width=50, active=True)
toggle13.on_click(Show_mot_and_pot)

# 'link'; allowed values are default, primary, success, warning, danger or light


#curdoc().add_root(f, myslider, height=300, width=1000)


f.plot_width = 800
f.plot_height = 400
f2.plot_width = 200
f2.plot_height = 400
f3.plot_width = 200
f3.plot_height = 400

lay_out = layout([[myslider], [toggle1, toggle2, toggle3, toggle4], [toggle5, toggle6, toggle7, toggle8], 
[toggle9, toggle10, toggle11, toggle12], [toggle13]])

graph_layout = gridplot([[f, f2, f3]], sizing_mode='fixed')
curdoc().add_root(graph_layout)
curdoc().add_root(lay_out)

#plot_width=700, plot_height=500,
#show(f)
