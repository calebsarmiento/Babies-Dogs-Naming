import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import altair as alt

st.set_page_config(page_title="Babies vs Dogs")

st.write("""
# Comparing the Naming of Babies to Dogs

**By Caleb Sarmiento**

When naming a dog, one might come up with a quick list or try calling out names to the dog, to see if any cause a reaction. A parent might even let their child make the decision all by themselves. On the other hand, parents may spend days or weeks just to come up with a list of many to pick from. The baby's sex and expected personality traits often tailor the name-choosing process, as well as the trending names floating around at the time. After all that, a final decision must be made. The name-choosing process for babies differs wildly from dogs, and looking at data on baby and dog names throughout the past decade reveals this.

The way data sets compare and contrast to each other can reveal the secrets behind our name-choosing process for babies and dogs. Like for example, what names overlap? Are there baby names that are being "stolen" by the dogs? What names have died out for babies and dogs?

---

## The Data Sets

These are the two data sets that will be analyzed in this project. Play around with the sliders and see how the data of dog names and baby names differ and relate! View the charts in fullscreen mode to see the names better when viewing lots of names at once.
""")

# Sliders for first two charts.
year_col1, count_col1 = st.columns(2)
with year_col1:
	select_year = st.slider('Year', min_value=2010, max_value=2023, step=1, value=2010)
with count_col1:
	select_count = st.slider('Number of Names', min_value=1, max_value=100, step=1, value=10)

# Make dataframe of count for each dog name.
df_dog = pd.read_csv('dogdata.csv')
dog_trends = df_dog.drop(['_id', 'LicenseType', 'Breed', 'Color', 'OwnerZip', 'ExpYear'], axis=1)
dog_trends['ValidDate'] = pd.to_datetime(dog_trends['ValidDate']).dt.year
# Filter years by slider value.
dogw = dog_trends
dog_trends = dog_trends[dog_trends['ValidDate'] == select_year]
# Other reformatting
dog_trends = dog_trends['DogName'].value_counts().rename_axis('Dog Name').reset_index()# Rename and reset for nice dataframe format.
dog_trends['Dog Name'] = dog_trends['Dog Name'].str.title()

# Make dataframe of count for each human name.
df_baby = pd.read_csv('humandata.csv')
# Filter years by slider value.
baby_trends = df_baby[df_baby['Year'] == select_year]

baby_trends = baby_trends.groupby('Name', as_index=False)['Count'].sum()
baby_trends = baby_trends.sort_values(by='Count', ascending=False, ignore_index=True)

# Chart for baby_trends.
bars = baby_trends.head(select_count)
baby_trends_chart = (
	alt.Chart(bars).mark_bar().encode(
		x=alt.X('Name', title='Baby Name', axis=alt.Axis(labelAngle=-60)).sort('-y'),
		y=alt.Y('Count', scale=alt.Scale(domain=[0, 24000])), color=alt.Color('Count').scale(scheme='greenblue')
	).properties(
		title=f'Top {select_count} Baby Names for the US in {select_year}'
	)
).configure_title(
	fontSize=16
)

# Chart for dog_trends
bars = dog_trends.head(select_count)
dog_trends_chart = (
	alt.Chart(bars).mark_bar().encode(
		x=alt.X('Dog Name', axis=alt.Axis(labelAngle=-60)).sort('-y'),
		y=alt.Y('count', title='Count', scale=alt.Scale(domain=[0, 55])), color=alt.Color('count').scale(scheme='goldred')
	).properties(
		title=f'Top {select_count} Dog Names for Allegheny County in {select_year}'
	)
).configure_title(
	fontSize=16
)

# Old way of displaying the two charts.
st.altair_chart(baby_trends_chart, use_container_width=True, theme=None)
st.altair_chart(dog_trends_chart, use_container_width=True, theme=None)

st.write("""
#### Finding The Data

The data sets can be found on their host websites through these hyperlinks: [BabyNames](https://catalog.data.gov/dataset/baby-names-from-social-security-card-applications-national-data), [DogNames](https://data.wprdc.org/dataset/allegheny-county-dog-licenses)

First, I found the dog license data set on the WPRDC website. From there, I started wondering, "How do dog names correlate with the dog's breed?" I started browsing the open data from the US Government to try to find a data set of dog licenses nationwide to have a larger data sample, but to my dismay, I was left with my data set that only contains dogs registered in Allegheny County. This is due to the National Dog Database being unavailable to the general public, as stated by [the Department of Internal Affairs.](https://www.dia.govt.nz/diawebsite.nsf/wpg_URL/Resource-material-Dog-Control-National-Dog-Database?OpenDocument) Tragic.

Eventually, I stumbled across a data set containing baby names from social security card applications. It's nationwide and includes applications from 1880 onward, which is honestly really incredible. I then started thinking about the two data sets. Dog names and baby names... I was no longer wondering about the correlation between dog breeds and their names, but now thinking about how baby names compare to dog names. And thus, my journey began on these two data sets.

Visualizing these data sets in creative ways will hopefully reveal how uniqueness amongst baby names compares to uniqueness in dog names. If I had to consider any potential harm these visualizations could cause, I would imagine certain people feeling negative about their name perhaps being too doglike... maybe?

In the above bar graphs, the baby and dog name data is for the currently set year from the slider. Human name data is nationwide for the US. **Dog name data is from Allegheny County only.** These two facts influenced how I decided what questions to answer with the data sets, as I couldn't answer questions like, "Are dogs likely to pick up more human names 

#### Dealing With The Data

The baby name data set was very extensive. The dog name data set only started in 2010, so right away, I decided I needed to remove the baby name entries from before 2010. Before doing this, I realized I had to deal with how the baby name data set was formated. It was spread across multiple **.txt** files, each for a single year's worth of data. I had all the years from 1880 to 2023 in .txt files! I deleted all the .txt files from before 2010 and luckily, the .txt files were all in the CSV format, so I only had to rename the file extensions to load them into a python script that merged the rest together. With the two data sets containing the same span of years, I removed the irrelevant data, and the data sets were ready to visualize.

---
""")

st.header("Name Relevance Over Time")

st.write("""
Enter your name, or someone elses, and see how popular it is over time, for babies and dogs! You should be able to click and type in a name or browse the list.

Try this out:
* Choosing the name 'Charlie' shows the interesting way that the Female population of a name can overtake the male population of it.
* Choosing the name 'Luna' shows how names can rise in occurance around the same time for dogs and babies.
""")

# Line graph of individual baby names and their count over time.
input_name = st.selectbox('Enter name:', df_baby['Name'].unique(),).title()
baby_year = df_baby[df_baby['Name'] == input_name]
baby_year = baby_year.sort_values(by='Year', ignore_index=True)
#baby_year['Year'] = pd.to_datetime(baby_year['Year'], format='%Y')
#st.dataframe(baby_year)
line = alt.Chart(baby_year).mark_line(point=alt.OverlayMarkDef(filled=False, fill="white")).encode(
	x='Year',
	y='Count',
	color='Sex'
)
st.altair_chart(line, use_container_width=True)

input_dog_name = st.selectbox('Enter name:', df_dog['DogName'].str.title().unique(), index=87)
# Line graph of individual dog names and their count over time.
dog_year = df_dog.drop(['_id', 'LicenseType', 'Breed', 'Color', 'OwnerZip', 'ExpYear'], axis=1)
dog_year['ValidDate'] = pd.to_datetime(dog_year['ValidDate']).dt.year
dog_year['DogName'] = dog_year['DogName'].str.title()
dog_year.groupby(['DogName'])['ValidDate'].nunique()
dog_count = dog_year.groupby('ValidDate')['DogName'].value_counts()
dog_count = dog_count.reset_index()
dog_count = dog_count[dog_count['DogName'] == input_dog_name].sort_values(by='ValidDate', ignore_index=False)
#st.dataframe(dog_count)
line = alt.Chart(dog_count).mark_line(point=alt.OverlayMarkDef(filled=False, fill="white")).encode(
	x=alt.X('ValidDate', title='Year'),
	y=alt.Y('count', title='Count'),
	color='DogName'
)
st.altair_chart(line, use_container_width=True)

st.write("""
---
## Dog Name Twins!

This chart shows how many dogs there are for baby names (over all time). The slider lets you show all 892 baby names that also show up in the dog name data set.

""")

slider_twin = st.slider('Number of Names', min_value=1, max_value=len(dog_trends), step=1, value=10, key=444)

# Get dataframe with just baby names that occur in dog names.
dogw = dogw['DogName'].value_counts().rename_axis('Dog Name').reset_index()# Rename and reset for nice dataframe format.
dogw['Dog Name'] = dog_trends['Dog Name'].str.title()
dog_twin = dogw[dogw['Dog Name'].isin(baby_trends['Name'])]

# Chart for dog_twin
bars = dog_twin.head(slider_twin)
#st.dataframe(dog_twin)
dog_twin_chart = (
	alt.Chart(bars).mark_bar().encode(
		x=alt.X('Dog Name', axis=alt.Axis(labelAngle=-60)).sort('-y'),
		y=alt.Y('count', title='Count', scale=alt.Scale(domain=[0, 600])), color=alt.Color('count').scale(scheme='yellowgreen')
	).properties(

	)
).configure_axis(
	labelFontSize=12
)
st.altair_chart(dog_twin_chart, use_container_width=True, theme=None)

st.markdown("Alternatively, you can do a lookup here on the same data set for any specific name.")

name_twin_input = st.selectbox('Enter Name:', dog_twin['Dog Name'])
dog_twin = dog_twin[dog_twin['Dog Name'] == name_twin_input]
dog_twin = dog_twin.sort_values('Dog Name', ignore_index=True)
st.dataframe(dog_twin, use_container_width=True, height=32)

st.write("---")
st.title('Reflection')
st.write("""
I decided to plot most of my data on bar graphs and line graphs. This was the most effective way to visualize the data. One really engaging aspect is the ability to look up specific names and see their trends. It's very fun to look up your own name and see what the data has to tell about it. Names are very closely tied to identity, so it makes sense for this information to be intruiging to look at. The design decision to have the graphs only capable of displaying a certain number of values at a time was a design choice that fell short. I believe a graph that could be scrolled along the x-axis would improve the readability of these large data sets. I had some failed attempts at doing this with the Altair library's interactive elements.

Were I to have another round of iteration on this project, I would explain further how each data visualization builds upon the previous. Essentially, I would focus on refining the narrative to be more concise. I'd want to write reflections for each data visualization to highlight exactly what was gained from creating them. As it is, this data story deals with a data set that only represents the name data for a single county in a single state. Comparing that with a data set of baby names that span over the entire country is rather occluding to the bigger story that dog names tell at a nationwide level. Perhaps a more compelling story could be told if the human names were isolated to Allegheny County as well, but that is impossible given the baby name data set used in this project, as no location information was included. Despite the shortcomings in this project, I have learned a lot.

What I enjoyed the most in the process of creating this page was learning how to visualize data with the specific tools that come with the Streamlit library as well as Python and Pandas. Seeing my vision come to life was truly inspiring. It excites me to see what is possible with open source libraries/frameworks, and makes me look forward to creating more on my own with my newly gained knowledge.

---
""")

st.title('References')
st.write("""
	Social Security Administration. *Baby Names from Social Security Card Applications - National Data* Data.Gov https://catalog.data.gov/dataset/baby-names-from-social-security-card-applications-national-data
	
	Allegheny County. *Allegheny County Dog Licenses* - Western Pennsylvania Regional Data Center https://data.wprdc.org/dataset/allegheny-county-dog-licenses
""")