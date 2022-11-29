"""
# DVA 2022: Exercise 1: Interactive Data Visualization in Python with Bokeh and Pandas

## Summary:
In this exercise, the ultimate goal is to get familiar with Bokeh and Pandas.

We will achieve this goal, by implementing a small "Data Inspector" tool. It allows us to select
two columns of our dataset, and plots them onto the x and y axis of a dot plot using Bokeh.

Essentially your task is to read through the code in dva_ex_1_firstname_lastname.py
and fill out the TODO code blocks according to the respective task.

Have a look at the demonstration video to have a reference on how the final tool should look and behave.

TIP 1:
if you haven't done the Bokeh Tutorial, I highly recommend you do so,
(https://mybinder.org/v2/gh/bokeh/bokeh-notebooks/master?filepath=tutorial%2F00%20-%20Introduction%20and%20Setup.ipynb)
or have a look at the "Server App" applications in the Bokeh gallery https://docs.bokeh.org/en/latest/docs/gallery.html

TIP 2:
Whenever you don't know something try google "Bokeh <your question / term>" or check the Bokeh docs or
check de discourse https://discourse.bokeh.org/


## Goals
**Goal 1**: Get familiar with the basics of Pandas

You should be able to:
- Load datasets from csv using pandas
- Combining datasets based on columns
- Renaming columns
- Basic cleaning (aka dropping nans)

**Goal 2**: Learn the Bokeh Server basics:

You should be able to:
- Run a Bokeh server application with the `bokeh serve` command
- Update the content a ColumnDataSource using dictionaries
- Add interactions with Bokeh widgets and implement callback functions


## How to run the code
Tip: If you have never used python before, or the following points could
just as well be part of the intergalactic highway scheme of Prostetnic Vogon Jeltz, please
Google "how to install requirements.txt in python tutorial" and
pick the one most attractive to you.


1. If you haven't install Python https://www.python.org/downloads/
   or Conda https://anaconda.org/ (conda is up to your )

2. Open a Terminal on your machine and move to the directory of the code:

    `cd /directory/of/this/code`
3. (Optional, but an indicator for good taste) Create a new virtual environment

    `python -m venv venv`

    Activate:

    Windows: `venv\Scripts\activate.bat`

    Else: `source venv/bin/activate`


4. Install the dependencies if you haven't before:

    `pip install -r requirements.txt`

5. Now you can always start your application directly with:
   `bokeh serve --show dva_ex_1_firstname_lastname.py`

6. Abort it with Ctrl + C

## Questions?
1. Google it
2. Ask a friend
3. Post to the forum
4. Ask during the office hour
5. (Last resort) Write me a mail halter@ifi.uzh.ch

"""
import typing

import pandas as pd
from bokeh.layouts import layout
from bokeh.models import ColumnDataSource, Select, HoverTool
from bokeh.plotting import figure, curdoc,show, save,output_file

'''
######################################################################
IMPORTANT: RENAME THIS FILE to dva_ex_1_firstname_lastname.py

           The code will be tested with Bokeh==2.4.2
           so make you have the same version or install
           the requirements.txt!
######################################################################


######################################
(0.5 Points) Section 1: Preprocessing
######################################
In this first section, it is your job to prepare the datasets to be visualized.
'''



# Load the datasets
df_sleep = pd.read_csv("mammals_sleep.csv")
df_predation = pd.read_csv("mammals_predation.csv")

# TIPP: Before advancing any further, inspect the datasets, how are they structured, what are the columns?
#       You can do this by using a simple print(df_sleep) or df_sleep.info()
#       Real-world datasets typically contain mistakes, typos, NaNs and other problems we have to deal with
#       Try to spot them early!


# (0.1) In both datasets, drop all rows where the species in nan                                (please keep this line)
# TODO Here comes your code
df_sleep.dropna()
df_predation.dropna()

# (0.1) Join the datasets based on the species column to one dataset                            (please keep this line)
# TODO Here comes your code
df_predation.columns = df_predation.columns.str.lower()
df_combined = pd.merge(df_sleep,df_predation,on='species')
#df_combined.dropna()


# (0.1) Remove all species where the body_wt is larger than 1000kg from the combined dataset    (please keep this line)
df_combined.drop(df_combined[df_combined['body_wt'] > 1000].index,inplace=True)


# (0.2) Rename all columns such that they do not contain any                                    (please keep this line)
# whitespaces and uppercase letters anymore
# eg. "Peter pan" -> "peter_pan"
df_combined.columns = df_combined.columns.str.lower()
df_combined.columns = df_combined.columns.str.replace(" ","_")

"""
######################################
(1.5 Points) Section 2: Visualization
######################################

In this section, we will implement the actual visualization in Bokeh
The concept is as follows:

1. We have a ColumnDataSource "source" which holds our current data 
   (x-coordinates (xs), y-coordinates (ys) and the names of the species (species))
2. We have a Plot which displays the above ColumnDataSource using a circle glyph 
3. We have two Dropdown menues (called Select in Bokeh), where the user can select which column is used for the x-axis 
   or the y-axis respectively. 
4. Whenever the Selects change, we have to update the ColumnDataSource, this is done via a callback function

We begin with implementing a fetch_data function, which takes two Column names from the input table, 
and returns a new dataset with the corresponding values as x and y coordinates. 
"""


# (0.5 Points) Implement the fetch_data function according to it's docstrings                   (please keep this line)
def fetch_data(x_column_name:str, y_column_name:str):
    """
    (0.3 Points) Given two column names, this function returns a dictionary with
    - (xs): a list of x-coordinates
    - (ys): a list of y-coordinates
    - (species): a list of species names

    (0.2 Points) Ensures, the result does not contain any NaNs
    """
    # TODO Here comes your code

    df_combined_new = df_combined.dropna()

    xs = df_combined_new[x_column_name].tolist()
    ys = df_combined_new[y_column_name].tolist()
    species = df_combined_new.species.tolist()
    for n in xs:
        if n == "NaN":
            raise ValueError
    for m in ys:
        if m == "NaN":
            raise ValueError
    for k in species:
        if k == "NaN":
            raise ValueError
    return dict(xs=xs, ys=ys, species=species)


data = fetch_data("body_wt", "brain_wt")
data_1 = fetch_data("predation", "dreaming")


# (0.2 Points) Create a ColumnDataSource with the data from fetch_data()                        (please keep this line)
# You can use any columns you want as the initial values

# TODO Here comes your code
source = ColumnDataSource(fetch_data("body_wt","brain_wt"))


# (0.2 Points) Create a figure with log axes, set initial axis labels correctly based            (please keep this line)
# on the previous step
p=figure(y_axis_type="log", x_axis_type="log", title='DVA: Mammal data sleeping inspector')
p.yaxis.axis_label = "brain_wt"
p.xaxis.axis_label = "body_wt"
p.sizing_mode = "stretch_both"
p.xgrid.grid_line_color = None

# (0.1 Points) add tooltips with the species names, x and y coordinates                          (please keep this line)
# TODO Here comes your code
plot = p.add_tools(HoverTool(
    tooltips=[("Species","@species"),
        ("x", "$x"),
        ("y", "$y"),
        ]))


# (0.1 Points) Create a circle glyph and bind it to the ColumnDataSource created previously      (please keep this line)
p.circle(x = 'xs', y='ys', source = source, line_color="#3288bd", fill_color="white", line_width=3)
#show(p)

select_xaxis = Select(title="X-axis variables", options=['body_wt', 'predation'], value='')
select_yaxis = Select(title="Y-axis variables", options=['brain_wt','dreaming'], value='')


def callback(attr, old, new):
    """
    This function is called whenever the current value of the select_xaxis or select_yaxis changes.

    Here, we have to
    - (0.1 Points) update the ColumnDataSource.data with a new dictionary returned from fetch_data
    - (0.1 Points) update the axis labels according to the new columns selected.

    Tipp:   Bokeh callbacks typically have this attr, old, new signature, however, in this case you can ignore
            them and fetch the current value of the two Select menus directly by accessing doing <your_select>.value

    """
    # TODO Here comes your code
    if select_yaxis.value == 'predation':
        new_data = fetch_data('predation', 'dreaming')
        p.xaxis.axis_label = "predation"
        p.yaxis.axis_label = 'dreaming'
        # Else, update 'y' to new
    elif select_yaxis.value == 'dreaming':
        new_data = fetch_data('predation', 'exposure')
        p.yaxis.axis_label = 'dreaming'
        p.xaxis.axis_label = "predation"

    source.data = ColumnDataSource(new_data)

# (0.3) Implement two Select Widgets and connect them to the callbacks                          (please keep this line)
#       Remove "species" from the list
# Tipp: If you are unsure on how to do this, have a look at the Callbacks Section and the Select Widget here:
# https://docs.bokeh.org/en/latest/docs/user_guide/interaction/widgets.html

# TODO Here comes your code
select_yaxis.on_change('value',callback)
select_yaxis.on_change('value',callback)


# (0.1 Point) Add everything to the layout                                                      (please keep this line)
lt = layout([select_xaxis,select_yaxis], p)
    # ...
#show(lt)
#output_file("dva_ex1_image1.html")
#save(lt)

curdoc().add_root(lt)
curdoc().title = 'dva_ex1'
