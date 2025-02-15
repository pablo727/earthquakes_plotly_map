from pathlib import Path
import json
import plotly.express as px

# Read data as a string and convert to a Python object.
path = Path('eq_data/eq_all_month.geojson')
contents = path.read_text(encoding='utf-8')
all_eq_data = json.loads(contents)

# # Create a more readable version of the data file.
# path = Path('eq_data/readable_eq_all_month.geojson')
# readable_contents = json.dumps(all_eq_data, indent=4)
# path.write_text(readable_contents)

# Examine all earthquakes in the data set.
all_eq_dicts = all_eq_data['features']

mags = [eq_dict['properties']['mag'] for eq_dict in all_eq_dicts]

# Replace negative values with 0
mags = [mag if mag > 0 else 0 for mag in mags]

lons = [eq_dict['geometry']['coordinates'][0] for eq_dict in all_eq_dicts]
lats = [eq_dict['geometry']['coordinates'][1] for eq_dict in all_eq_dicts]
eq_titles = [eq_dict['properties']['title'] for eq_dict in all_eq_dicts]

title = all_eq_data['metadata']['title']

fig = px.scatter_geo(lat=lats, lon=lons, size=mags, title=title, 
                     color=mags, color_continuous_scale='hot',
                      labels={'color': 'Magnitude'},
                      projection='natural earth',
                      hover_name=eq_titles,
                        )

fig.update_layout(
    geo=dict(
        showland=True, landcolor="wheat",
        showocean=True, oceancolor="lightblue",
        showlakes=True, lakecolor="rgb(173, 216, 230)",
        showcountries=True, countrycolor="black",
        showcoastlines=True, coastlinecolor="black",
    )
)

# Update marker appearance: color scale, opacity and border.
fig.update_traces(
    marker=dict(
        colorscale='hot',
        line=dict(width=1, color='black'), 
        opacity=0.7
    )
)

fig.show()
fig.write_html('earthquakes_map.html')