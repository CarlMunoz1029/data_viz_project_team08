'''
    Provides the template for the tooltips.
'''


def get_bubble_hover_template():
    '''
        Sets the template for the hover tooltips.
        
        Contains four labels, followed by their corresponding
        value and units where appropriate, separated by a
        colon : country, population, GDP and CO2 emissions.

        The labels' font is bold and the values are normal weight

        returns:
            The content of the tooltip
    '''
    spacing="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
    hovertemplate = spacing + "<span style='font-weight:bold'><b> Country</b></span><span style='font-weight:normal'> : %{customdata[0]} <br /></span>" +\
                    spacing + "<span style='font-weight:bold'><b> Population</b></span><span style='font-weight:normal'> : %{customdata[1]} <br /></span>" +\
                    spacing + "<span style='font-weight:bold'><b>GDP</b></span><span style='font-weight:normal'> : %{x} $ (USD)<br /></span>" +\
                    spacing + "<span style='font-weight:bold'><b>CO2 emissions</b></span><span style='font-weight:normal'> : %{y} metric tonnes<br /></span><extra></extra>"
    
    return hovertemplate