import pandas
import matplotlib.pyplot as plt


## read file and clean off NAN values
df = pandas.read_csv('data//colors.csv')
clean_df = df.dropna()

## sum up the amount of unique colors
unique_colors = clean_df['name'].nunique()
print(unique_colors)

## find the number of translucent colors and count them up
trans_colors = clean_df.groupby('is_trans').count()
print(trans_colors)

## same outcome with different method usage
trans_colors = clean_df.is_trans.value_counts()
print(trans_colors)

## reading the sets data sheet and cleaning off NAN values
sets = pandas.read_csv('data//sets.csv')
clean_sets = sets.dropna()

## sorting by 'year' and only viewing the head
first_sets = clean_sets.sort_values("year").head()
print(first_sets)

## sort by year, and see how many sets were available for sale per year
per_year_sales = clean_sets.groupby('year').count()
print(per_year_sales)
## only shows the amount of sets available for sale in 1949
first_year_sets = clean_sets[clean_sets['year'] == 1949]
print(first_year_sets)

## sort by how many parts are in each set, and then flip the highest values at the top of the list, instead of the bottom
largest_sets = clean_sets.sort_values("num_parts", ascending=False).head()
print(largest_sets)

## sorting into sets avaiable per year and then suming the amount available
sets_per_year = clean_sets.groupby('year').count()
print(sets_per_year['set_num'])

## constructing graph from the sets per year data. except it is misleading due to the lack of information in 2020
set_graph = plt.plot(sets_per_year.index, sets_per_year.set_num)

## instead, we exclude the last two rows of data because 2020 and 2021 are innacurate 
set_graph = plt.plot(sets_per_year.index[:-2], sets_per_year.set_num[:-2])

## group by how many different themes were availalble per year
themes_per_year = clean_sets.groupby('year').agg({'theme_id': pandas.Series.nunique})
print(themes_per_year)

## clean up and reorganize to minimize data presented
themes_per_year.rename(columns = {'theme_id': 'nr_themes'}, inplace = True)
print(themes_per_year)

## graph to show themes per year
theme_graph = plt.plot(themes_per_year.index[:-2], themes_per_year.nr_themes[:-2])

## get current axies
ax1 = plt.gca() ## current axis
ax2 = ax1.twinx() ## create a twin axis that shares the same x axis as the ax1

## plot both lines of data on the same graph and add in colors to distinguish wich line is which set of data
ax1.plot(sets_per_year.index[:-2], sets_per_year.set_num[:-2], color='g')
ax2.plot(themes_per_year.index[:-2], themes_per_year.nr_themes[:-2], color='b')

## add in labels to both sides of the graph that show the values they measure
ax1.set_xlabel("Year")
ax1.set_ylabel("Number of Sets", color="green")
ax2.set_ylabel("Number of Themes", color="blue")

## build a new data set of how many parts are in each set per year, and then average the value
parts_per_set = clean_sets.groupby('year').agg({'num_parts': pandas.Series.mean})
print(parts_per_set)

## create a scatter plot of the parts per set data
plt.scatter(parts_per_set.index[:-2], parts_per_set.num_parts[:-2])

## show a table of how many sets per theme exist. but it only shows the theme id, not the name of the theme
sets_per_theme = clean_sets["theme_id"].value_counts()
print(sets_per_theme[:5])


## reading the themes data sheet to identify which theme goes to which theme id
theme_df = pandas.read_csv('data//themes.csv')
print(theme_df)

## finding all of the star wars theme id's
star_wars_sets = theme_df[theme_df.name == "Star Wars"]
print(star_wars_sets)

## finding all of the droid sets by thier id in the clean sets df
droid_sets = clean_sets[clean_sets.theme_id == 18]
print(droid_sets)

## finding all of the star wars advent sets in the clean sets df
advent_sets = clean_sets[clean_sets.theme_id == 209]
print(advent_sets)

## creating a dictionary of theme_id: set count
sets_per_theme = pandas.DataFrame({'id':sets_per_theme.index, 'set_count':sets_per_theme.values})
print(sets_per_theme)

## merging the two data frames into a single dataframe, then only showing the top 3 theme id's by set count per theme_id
merged_df = pandas.merge(sets_per_theme, theme_df, on='id')
merged_df[:3]

## making a bar chart to display the top ten themes with the most sets
plt.bar(merged_df.name[:10], merged_df.set_count[:10])

## reformat the chart to be legible
plt.figure(figsize=(14,8))
plt.xticks(fontsize=14, rotation=45)
plt.yticks(fontsize=14)
plt.xlabel("Theme Name", fontsize=14)
plt.ylabel("Number of Sets", fontsize=14)
plt.bar(merged_df.name[:10], merged_df.set_count[:10])
