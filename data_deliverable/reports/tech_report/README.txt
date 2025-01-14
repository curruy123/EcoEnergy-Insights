Data is already clenaed becuase they are solely numbers but there are some columns that are not populated for some rows, but we can't delete the rows because other countries do have data in them.

For each of our three data sets, we have at least 800 data points available. This includes the continent over a wide range of years and their respective metric that we would be 
looking at (CO2 emission, energy, or TFP). In terms of our sample size for the relationship between energy and TFP, we decided to look at all of the continents. Among all of the continents, we have 
specific data like energy per capita that we want to look at, but we were also considering using GDP, as this can also reflect a countries energy level. However, this would require us to also identify a positive 
relationship between energy level as well as GDP. We have all of the data for CO2 emissions, energy level per capita, and TFP for all of the continents that we will be observing. This data also includes multiple decades. 
We definitely have enough data to analyze in this sense. 

- The identifying attributes on the TFP data sheet is each regions total TFP score which will tell us how productive the agriculture is in the region. 
For the continent energy data set, we have columns that will allow us to identify what specific regions are using to consume energy for their people, whether they are renewable or fossil fuels
The last identifying point is from thr CO2 data sheet, which will have all the information about each regions emissions.

- We got the data from OurWorldInData and the US Department of Agriculture. OurWorldInData tends to be pretty reliable based on research, but of course, you could argue that 
the USDA could biased because since it is a faction of the US Government. The US government has its allies and opponents so it ould skew dat ain some way and we will defintely consider this.

- We collected through research online looking for csv's that had data on our desired categories.
- The sample we are providing is just taking on from these sheets of data and combing the emissions, energy consumption and 
agriculture productivity together to one file to later make inferences and other uses out of it. The sample overall may have some baised towards regions with more 
information in the data, but this bias could paint the region in good or bad light depending on the results of the research.

When collecting our data, we obviously wanted to collect our data from a reputable website that would provide reliable data. 
We also wanted to make sure that the data that was being provided wasn’t a chart or graph, but a dataset that 
we could download and parse through. When searching for our energy dataset, we also came across some datasets that we had to pay for. 
We made sure to avoid these, but there was a possibility that these datasets could have provided more comprehensive information on our data. However, 
we still believe that our current data is sufficient and will provide us with the necessary data that we need.


Peck's Section:
The data has been cleaned, outside of needing to lowercase and make a uniform style of all categorical values in our dataset.
All of our datasets contain the data we need in order to complete the project we proposed, the only 
concerns(which is within our control) are scope of our hypotheses and how we will decide to answer it via data 
visualization techniques
- We checked for the cleanliness of our data by checking for empty and null values within our dataset that we may not use.
Although the scope of our project is still relatively undefined, we plan on checking for statistics on a continent by 
continent basis. Our TFP datasrt provided a lot more substantial info such as total crop output, total animal output, 
and other specifities that may help us decide what route of quesitons we would like to answer with our graphs and our 
data joining. One mechanism we used is as said before, dropping all null values from our dataset. It was important to do
this because since the carbon dioxide data and energy data set revolved around continents that were available in the TFP 
dataset since there was a wide array of countries from different sub regions. There are duplictaes but this is due to 
the diffeerence in data values being represented by each year. It is important to keep the duplicates because while we are
still trying to clarify the questions we want to answer with our hypotheses, it will be important to see what values
for each year are held in each of the datasets
- There may be data we need throw away as we said before, there is a substantial amount of data not only for each 
contient, but also countries within each continent and because we are still trying to narrow down what we want, we may 
need to throw away data that might inflate the values for their respective countries because we may count them more
than once. We also took out data prior to 1993 because it had null values and we decided to prioritize looking at data
from the last 30 years.

Challenges:
There were some challenges and observaitosn that we have made since we have collected our data in terms of scalability 
and the interval of time we will be looking at. Because our datasets span a long nmber of years, the context of our 
hypothesis matters in the sense we have to decide taking a historic approach at the data or more contemporary outlook.
For example, because we aren't in a world where the Soviet Union is still present, we took all data relating to it out. 
Additionally, some of the data were merged together, as all of the data from West Asia, Central Asia, and North Africa
were all combined under one country as 'CWANA' and data for South America was under 'LAC'.  I had to parse the data in order to create corresponding columns for the
known continents. A lot of our comments in our code explicity goes into this process. Our
next steps are to figure this out, as well as decide to look at which variables within our TFP dataset to analyze closely
as it spans many different aspects of agriculture and what are "meaningful values". Also, to reassess how we may join 
tables and what future quweries we may have to make

