# knox-data-lake

##Problem
The City of Knoxville is at the beginning stages of their open data initiative. As more datasets become avaiable it would be nice to have a central repository for the data that is open to the public and provides a level of consistency in formatting for the data. These datasets could also be larger and updated more frequently than the currently available data. 

##Solution
A common pattern seen in private sector businesses is the concept of a data lake. The central component of a data lake is the storage platform. This is typically a cloud object store service. In addition to the storage platform there are small applications that do lightweight processing of the incoming data to change the file format or possibly do transformations of the data. This is usually accomplished with a cloud functions service.

![Logo](knox_data_lake_arch.png?sanitize=1 "Knox Data Lake Architecture")

When thinking about how to apply this concept to a publicly available data lake, one of the biggest concerns was security of the data coming in. The data could come from many sources within the city government as well as community members or third party services.

Examples: 
- A developer that has combined some of the data sources in an interesting way and wants to share the new data set.
- Third party commercial apps that collect interesting local data (Waze, Parkopedia)

To address this problem we separate the incoming data into separate object storage buckets with separate credentials. This provides a simple way to scale out the incoming data sources without having to worry about a mistake in permissions causing other users data to be compromised.

# Facade data analysis
