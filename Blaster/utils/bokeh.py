# Standard library imports
from math import pi

# Third-party imports
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.palettes import Category10
from bokeh.transform import cumsum
from bokeh.models import HoverTool

from django.db.models.query import QuerySet

import pandas as pd


def seqlen_graph(selected_hits: QuerySet) -> tuple[str, str]:
    """Generates sequence length bar chart

    Generates a Bokeh bar chart of sequence lengths for selected hits.

    Takes a QuerySet of hit objects, extracts their unique 
    accession and sequence lengths, and creates a bar graph
    displaying each hit's length.
    Toolbar only contains the save tool (and hover tool by default),
    as the graph is not interactive.

    Unique accessions have been made and used as the x-axis 
    labels to avoid confusion as there are duplicate accessions.

    :param selected_hits: QuerySet of hit objects
        selected by the user
    :type selected_hits: QuerySet
    :return: A tuple containing the script and div
        elements for embedding the Bokeh plot in the HTML template.
    :rtype: tuple[str, str]
    """

    # Get the unique accessions and lengths of the selected hits
    unique_accessions, lengths = [], []
    for hit in selected_hits:
        unique_accessions.append(hit.unique_accession)
        lengths.append(len(hit.subject_seq))

    # Create a new plot
    plot = figure(title="Sequence length per hit",
                  x_axis_label="Hit accessions",
                  y_axis_label="Sequence length",
                  x_range=unique_accessions,
                  toolbar_location="above",
                  tools="save",
                  width=1000,
                  height=400)
    plot.xaxis.major_label_orientation = 'vertical'

    source = ColumnDataSource(data=dict(x=unique_accessions, 
                                        y=lengths, 
                                        accession=unique_accessions, 
                                        length=lengths))

    # Add vertical bars to the plot 
    plot.vbar(x='x', top='y', width=0.75, source=source, color='#297373')

    # Add tooltips
    tooltips = [
        ("Accession", "@accession"),
        ("Sequence Length", "@length")
    ]
    plot.add_tools(HoverTool(tooltips=tooltips))

    # Generate HTML elements
    script, div = components(plot)

    return script, div


def perc_identity_graph(selected_hits: QuerySet) -> tuple[str, str]:
    """ Generates percentage identity bar chart

    Generates a Bokeh bar chart of percentage identities 
    for selected hits.

    Takes a QuerySet of hit objects, extracts their unique 
    accession and percentage identities, and creates a bar graph
    displaying each hit's percentage identity with the query sequence.
    Toolbar only contains the save tool (and hover tool by default),
    as the graph is not interactive.
    
    Unique accessions have been made and used as the x-axis 
    labels to avoid confusion as there are duplicate accessions.

    :param selected_hits: QuerySet of hit objects
        selected by the user
    :type selected_hits: QuerySet
    :return: A tuple containing the script and div
        elements for embedding the Bokeh plot in the HTML template.
    :rtype: tuple[str, str]

    """
    # Get unique accessions and percentage identities
    unique_accessions, perc_identity = [], []
    for hit in selected_hits:
        unique_accessions.append(hit.unique_accession)
        perc_identity.append(hit.percentage_identity)

    # Create a new plot
    plot = figure(title="Percentage identity per hit",
                  x_axis_label="Hit accessions",
                  y_axis_label="Percentage identity",
                  x_range=unique_accessions,
                  toolbar_location="above",
                  tools = "save",
                  width=1000,
                  height=400
                  )
    plot.xaxis.major_label_orientation = 'vertical'

    source = ColumnDataSource(data=dict(x=unique_accessions, 
                                        y=perc_identity, 
                                        accession=unique_accessions, 
                                        identity=perc_identity))

    # Add vertical bars to the plot 
    plot.vbar(x='x', top='y', width=0.75, source=source, color='#297373')

    # Add tooltips
    tooltips = [
        ("Accession", "@accession"),
        ("Percentage Identity", "@identity")
    ]
    plot.add_tools(HoverTool(tooltips=tooltips))

    # Generate HTML elements
    script, div = components(plot)

    return script, div


def query_coverage_graph(selected_hits: QuerySet) -> tuple[str, str]:
    """
    Generates a Bokeh bar chart of query coverage for selected hits.

    Takes a QuerySet of hit objects, extracts their unique 
    accession and query coverages, and creates a bar graph
    displaying the query coverage of each hit.
    Toolbar only contains the save tool (and hover tool by default),
    as the graph is not interactive.

    Unique accessions have been made and used as the x-axis 
    labels to avoid confusion as there are duplicate accessions.

    :param selected_hits: QuerySet of hit objects
        selected by the user
    :type selected_hits: QuerySet
    :return: A tuple containing the script and div
        elements for embedding the Bokeh plot in the HTML template.
    :rtype: tuple[str, str]
        
    """
    # Get unique accessions and query coverages
    unique_accessions, query_coverage = [], []
    for hit in selected_hits:
        unique_accessions.append(hit.unique_accession)
        query_coverage.append(hit.query_coverage)

    # Create a new plot
    plot = figure(title="Query coverage per hit",
                  x_axis_label="Hit accessions",
                  y_axis_label="Query coverage",
                  x_range=unique_accessions,
                  toolbar_location="above",
                  tools = "save",
                  width=1000,
                  height=400
                  )
    plot.xaxis.major_label_orientation = 'vertical'

    source = ColumnDataSource(data=dict(x=unique_accessions, 
                                        y=query_coverage,
                                        accession=unique_accessions, 
                                        coverage=query_coverage))

    # Add vertical bars to the plot 
    plot.vbar(x='x', top='y', width=0.75, source=source, color='#297373')

    # Add tooltips
    tooltips = [
        ("Accession", "@accession"),
        ("Query Coverage", "@coverage")
    ]
    plot.add_tools(HoverTool(tooltips=tooltips))

    # Generate HTML elements
    script, div = components(plot)

    return script, div


def e_value_graph(selected_hits: QuerySet) -> tuple[str, str]:
    """ Generates E-value significance categories pie chart

    Generates a Bokeh pie chart of E-value significance categories for
    the selected hits in the QuerySet. The categories are divided into
    four categories. The chart shows the distribution of hits in each
    category.
    Toolbar only contains the save tool (and hover tool by default),
    as the graph is not interactive.

    Unique accessions have been made and used as labels to 
    avoid confusion as there are duplicate accessions.

    :param selected_hits: QuerySet of hit objects
        selected by the user
    :type selected_hits: QuerySet
    :return: A tuple containing the script and div
        elements for embedding the Bokeh plot in the HTML template.
    :rtype: tuple[str, str]
        
    """
    e_values_categories, accessions = {
        'Extremely significant': 0,
        'Very significant': 0,
        'Moderately significant': 0,
        'Not significant': 0
    }, {
        'Extremely': [],
        'Very': [],
        'Moderately': [],
        'Not': []
    }
    
    # Classify each hit
    for hit in selected_hits:
        e_value = float(hit.e_value)
        if e_value < 1e-50:
            e_values_categories['Extremely significant'] += 1
            accessions['Extremely'].append(hit.unique_accession)
        elif e_value < 1e-20:
            e_values_categories['Very significant'] += 1
            accessions['Very'].append(hit.unique_accession)
        elif e_value < 1e-5:
            e_values_categories['Moderately significant'] += 1
            accessions['Moderately'].append(hit.unique_accession)
        else:
            e_values_categories['Not significant'] += 1
            accessions['Not'].append(hit.unique_accession)
    
    # Prepare data for plotting
    data = pd.DataFrame({
        'category': list(e_values_categories.keys()),
        'value': list(e_values_categories.values()),
        'accessions': ['<br>'.join(accs) for accs in accessions.values()]
    })
    data['angle'] = data['value'] / data['value'].sum() * 2 * pi
    data['color'] = Category10[len(e_values_categories)]

    source = ColumnDataSource(data)

    # Create the plot
    plot = figure(title="E-value significance categories",
                  toolbar_location="above",
                  tools="save",
                  tooltips=[("Category", "@category"),
                            ("Count", "@value"),
                            ("Accessions", "@accessions{safe}")],
                  x_range=(-0.5, 1.0),
                  width=650,
                  height=400
                  )

    plot.wedge(x=0, y=1, radius=0.4,
               start_angle=cumsum('angle', include_zero=True),
               end_angle=cumsum('angle'),
               line_color="white", 
               fill_color='color', 
               legend_field='category', 
               source=source
               )

    plot.axis.axis_label = None
    plot.axis.visible = False
    plot.grid.grid_line_color = None

    script, div = components(plot)
    return script, div