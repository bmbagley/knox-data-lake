# knox-data-lake
2019 Knoxville Hackathon Team

## Problem
The City of Knoxville is at the beginning stages of their open data initiative. As more datasets become avaiable it would be nice to have a central repository for the data that is open to the public and provides a level of consistency in formatting for the data. These datasets could also be larger and updated more frequently than the currently available data. 

## Solution
A common pattern seen in private sector businesses is the concept of a data lake. The central component of a data lake is the storage platform. This is typically a cloud object store service. In addition to the storage platform there are small applications that do lightweight processing of the incoming data to change the file format or possibly do transformations of the data. This is usually accomplished with a cloud functions service.

![Logo](knox_data_lake_arch.png?sanitize=1 "Knox Data Lake Architecture")

When thinking about how to apply this concept to a publicly available data lake, one of the biggest concerns was security of the data coming in. The data could come from many sources within the city government as well as community members or third party services.

Examples: 
- A developer that has combined some of the data sources in an interesting way and wants to share the new data set.
- Third party commercial apps that collect interesting local data (Waze, Parkopedia)

To address this problem we separate the incoming data into separate object storage buckets with separate credentials. This provides a simple way to scale out the incoming data sources without having to worry about a mistake in permissions causing other users data to be compromised.

## Facade data analysis
The data set available for the facade grant is limited in scope and requires the ingestion of multiple other data sources to augment.

<details><summary>facade_grant_recipients.csv</summary>
<p>
 | FUND SOURCE | ADDRESS | BUSINESS | STATUS | FAĂADE PROGRAM AMOUNT | FUNDS AVAILABLE |
 |--------------------------|----------------------------------|------------------------------|------------------------|-----------------------|-----------------|
 | General Funds | 1200/1210 N Central | Knoxvill Preservation | Completed (01/05/2009) | 78,246.00 | 521,754.00 |
 | General Funds | 200 W. Jackson Ave | David Dewhirst | Completed (07/22/2009) | 50,000.00 | 471,754.00 |
 | General Funds | 415 W. Depot | Jack O'Hanlon | Completed (07/22/2009) | 36,435.20 | 435,318.80 |
 | General Funds | 2461 M.L.K. | Ira Grimes | Completed (02/11/2010) | 49,858.73 | 385,460.07 |
 | General Funds | 3404 M.L.K. | David Andrews | Completed (04/15/2010) | 49,364.00 | 336,096.07 |
 | General Funds | 109 Bertrand | E. TN Mechanical | Completed (09/02/2010) | 38,543.00 | 297,553.07 |
 | General Funds | 1831 McCalla | E. TN Mechanical | Completed (09/02/2010) | 45,857.00 | 251,696.07 |
 | General Funds | 3911 M.L.K. | Charles Holland | Completed (05/06/2010) | 40,672.00 | 211,024.07 |
 | General Funds | 726 Chickamauga | The Parlor, LLC | Completed (08/05/2011) | 30,217.92 | 180,806.15 |
 | General Funds | 106 Ogle Ave | Delta Group, LLC | Completed (10/17/2011) | 50,000.00 | 130,806.15 |
 | General Funds | 2120 Magnolia | Tony Shin | Completed (5/30/2012) | 48,355.20 | 82,450.95 |
 | General Funds | 3610 Magnolia Ave | Gary White/Mark Bigelow | Completed (5/17/2012) | 50,000.00 | 32,450.95 |
 | General Funds | 2444 M.L.K. | Charles Frazier | Completed (5/22/2012) | 46,940.00 | -14,489.05 |
 | General Funds | 120 W. Okalhoma | Teresa Winters | Completed (5/23/2012) | 15,006.00 | -29,495.05 |
 | General Funds | 119 Central Street | Nancy Voith | Completed (11/11/2014) | 50,000.00 | 0.00 |
 | General Funds | 525 N. Gay Street | Hatcher Hill | Completed (9/1/2013) | 50,000.00 | 0.00 |
 | General Funds | 211 Jessamine | Bittle & Sons | Completed 4/30/14 | 50,000.00 | 0.00 |
 | General Funds | 104 E. Fifth | Fifth Avenue Partners | Completed 11/11/2014 | 50,000.00 | 0.00 |
 | General Funds | 1116 Sixth Avenue | Christopher Pease | Completed 5/7/2014 | 50,000.00 | 0.00 |
 | General Funds | 618 N. Broadway | Twofold Purchase | Completed 4/16/2014 | 49,417.00 | 0.00 |
 | General Funds | 1115 Sixth Avenue | Christopher Pease | Completed 8/17/2015 | 50,000.00 | 0.00 |
 | General Funds | 2501 N. Central Street | Keith Windows | Completed 10/31/2015 | 28,225.00 | 0.00 |
 | General Funds | 923 N. Central Street | Dale Mackey/Shawn Poynter | Completed 11/12/2015 | 48,981.00 | 0.00 |
 | General Funds | 318 N. Gay Street | Regas Building, LLC | Completed 12/21/2015 | 50,000.00 | 0.00 |
 | General Funds | 412 Gay Street (3 Bldgs) | Hatcher Hill | Completed 12/13/2015 | 150,000.00 | 0.00 |
 | General Funds | 1104 McCalla Avenue | Twofold Purchase | Completed 1/31/2016 | 50,000.00 | 0.00 |
 | General Funds | 1601 Western Avenue | Hatcher Hill | Completed 4/30/2016 | 50,000.00 | 0.00 |
 | General Funds | 210 W. Magnolia Avenue | Bridge Properties | Completed 4/30/2016 | 50,000.00 | 0.00 |
 | General Funds | 201/203 Depot Avenue (2 Bldgs) | Depot Development | Completed 5/31/2016 | 100,000.00 | 0.00 |
 | General Funds | 1138 N. Broadway | Fourfold Purchase | Completed 5/31/2016 | 34,100.00 | 0.00 |
 | General Funds | 108-114 E. Jackson (3 Bldgs) | Old City Amigos | Completed 6/30/2016 | 100,000.00 | 0.00 |
 | General Funds | 1120 Sevier Avenue | Brett Honeycutt | Completed 8/31/2016 | 50,000.00 | 0.00 |
 | General Funds | 213 E. Fourth Avenue | Knox 213 LLC | Completed 9/30/2016 | 50,000.00 | 0.00 |
 | General Funds | 1147 Sevier Avenue | Zach & Hao Land | Completed 9/30/2017 | 41,790.00 | 0.00 |
 | General Funds | 835 N. Central Street | 835 Central LLC | Completed 8/30/2017 | 50,000.00 | 0.00 |
 | General Funds | 700 Sevier Avenue | Greg Cates/Peter Medlyn | Completed 1/31/2017 | 50,000.00 | 0.00 |
 | General Funds | 2423 N. Central Street | John Sanders | Completed 7/30/2017 | 50,000.00 | 0.00 |
 | General Funds | 902 N. Central Avenue | Jordan Wilkerson | Completed 11/30/17 | 50,000.00 | 0.00 |
 | General Funds | 745 & 751 N. Broadway | SMJT, LLC | Completed 9/1/2018 | 76,000.00 | 0.00 |
 | General Funds | 730 N. Broadway | Jim and Lori Klonaris | Completed 3/31/2018 | 100,000.00 | 0.00 |
 | General Funds | 113-119 S. Gay Street | Courtland Group | Under Construction | 50,000.00 | 0.00 |
 | General Funds | 2300 E. Magnolia | Park City Improvement LLC | Completed 10/28/2018 | 50,000.00 | 0.00 |
 | General Funds | 119 W. Fifth Avenue | Mark Hickman | Completed 7/25/2018 | 50,000.00 | 0.00 |
 | General Funds | 800 N. Broadway | Matt Reed/Lloyd Montgomery | Completed 8/7/2018 | 50,000.00 | 0.00 |
 | General Funds | 1300 McCalla | Derek White | Completed 8/20/2018 | 50,000.00 | 0.00 |
 | General Funds | 2320 N. Central | Byron Williamson | Completed 8/28/2018 | 50,000.00 | 0.00 |
 | General Funds | 2411 N. Central | Loch and Key Holdings | Completed 5/30/2018 | 50,000.00 | 0.00 |
 | General Funds | 2417 N. Central | Elst Brewing | Under Construction | 50,000.00 | 0.00 |
 | General Funds | 930 N. Broadway | Broadway Carpets | Completed 11/16/2018 | 50,000.00 | 0.00 |
 | General Funds | 1717 N. Broadway | Semeco Enterprises, LLC | Under Construction | 50,000.00 | 0.00 |
 | General Funds | 2200 & 2202 MLK | Cherokee Health | Under Construction | 100,000.00 | 0.00 |
 | General Funds | 1731 Western Avenue | Hatcher Hill Properties | Under Construction | 100,000.00 | 0.00 |
 | CDBG Funds | 2200 M.L.K. (2 Bldgs) | Hardy Bldgs | Completed (02/14/2006) | 135,689.63 | 0.00 |
 | CDBG Funds | 2446 M.L.K. | Kim Cannon | Completed (04/05/2006) | 32,795.40 | 0.00 |
 | CDBG Funds | 301 N. Central | Dewhirst Const | Completed (01/19/2007) | 50,000.00 | 0.00 |
 | CDBG Funds | 501 Arthur St | Michael Elliott | Completed (08/17/2007) | 50,000.00 | 0.00 |
 | CDBG Funds | 3920 M.L.K. | Josh Jordan | Completed (12/08/2008) | 15,385.00 | 0.00 |
 | CDBG Funds | 3930 M.L.K. | Terri-Cade Hill | Completed (04/21/2009) | 55,840.00 | 0.00 |
 | CDBG Funds | 500 Arthur St | Peter J. Biasella | Completed (07/21/2010) | 46,706.00 | 0.00 |
 | CDBG Funds | 1537 Western Ave | James Hodge | Completed (11/05/2010) | 41,352.00 | 0.00 |
 | CDBG Funds | 1551 Western Ave | Betty Martin | Completed (07/08/2011) | 56,161.00 | 0.00 |
 | CDBG Funds | 2117 Middlebrook Pk | SpdRcr | Completed (01/10/2012) | 42,500.00 | 0.00 |
 | CDBG Funds | 2350 E. Magnolia Ave | T. Scott Jones | Completed (12/05/2011) | 50,000.00 | 0.00 |
 | CDBG Funds | 529 N Gay St | William D. Harris | Completed (10/19/2012 | 41,022.00 | 0.00 |
 | CDBG Funds | 412/416 W. Jackson (2 Bldgs) | Heinz/Dewhirst | Completed (11/16/2012) | 100,000.00 | 0.00 |
 | CDBG Funds | 1320 N. Broadway | Patrick McInturff | Completed 8/14/2014 | 50,000.00 | 0.00 |
 | CDBG Funds | 2018 Davenport Road | Elizabeth McWhirter | Completed 7/14/2015 | 50,000.00 | 0.00 |
 | CDBG Funds | 605 Sevier Avenue | David Glass | Completed 7/10/2015 | 52,197.00 | 0.00 |
 | CDBG Funds | 308/312/410 W. Jackson (3 Bldgs) | David Dewhirst | Completed (05/04/2011) | 150,000.00 | 0.00 |
 | CDBG Funds | 800 Tyson | Patricia Smith | Completed 6/1/2015 | 48,000.00 | 0.00 |
 | CDBG Funds | 1828 McCalla Avenue | Gwendolyn Harshaw | Completed 4/22/2015 | 50,000.00 | 0.00 |
 | CDBG Funds | 2411 Magnolia Avenue | Knox County Education Assoc. | Completed 7/29/2015 | 35,648.00 | 0.00 |
 | CDBG Funds | 309 Central Street | Depot Development | Completed 8/17/2015 | 50,000.00 | 0.00 |
 | CDBG Funds | 505 Cooper Street | Taie Li | Completed 10/21/2015 | 46,236.00 | 0.00 |
 | CDBG Funds | 714 N. Broadway | Bobby Copeland | Completed 12/30/2014 | 50,000.00 | 0.00 |
 | CDBG Funds | 1123 N. Central | David Belcher | Completed 3/31/2016 | 47,170.00 | 0.00 |
 | CDBG Funds | 3814 MLK | Jervis Brown | Completed 10/28/2016 | 50,000.00 | 0.00 |
 | CDBG Funds | 3701 Sevierville Pike | Brian Hann, Jason Stephens | Completed 3/31/2017 | 50,000.00 | 0.00 |
 | CDBG Funds | 629 Broadway | Stone Street Group | Completed 1/31/2018 | 50,000.00 | 0.00 |
 | CDBG Funds | 3900 MLK | Ignite Solutions LLC | Under Construction | 50,000.00 | 0.00 |
 | CDBG Funds | 1700 N. Central Street | Andrew Edens | Completed 7/9/2018 | 50,000.00 | 0.00 |
 | Magnolia Warehouse Funds | 1725 E. Magnolia | Faye & Frances Levert | Completed 5/15/2016 | 53,545.00 | 0.00 |
 | Magnolia Warehouse Funds | 103 Jessamine (3 Bldgs) | Gray Holdges Electric | Completed 2/24/2014 | 157,455.00 | 0.00 |
 | Magnolia Warehouse Funds | 106 E. Depot (2 Bldgs) | Dewhirts/Heinz | Completed 2/26/2014 | 150,000.00 | 0.00 |
 | Magnolia Warehouse Funds | 711 Hall of Fame | Richard Kelley | Completed 7/30/2013 | 50,000.00 | 0.00 |
 | EZ Funds | Facade Misc Expenses | 0 | 0 | 305.00 | 0.00 |
 | EZ Funds | 700 N. Broadway | High Oaks Const | Completed (11/01/2006) | 50,000.00 | 0.00 |
 | EZ Funds | 8, 10, & 12 Emory | Duane Grieve #2 | Completed (05/08/2007) | 11,409.00 | 0.00 |
 | EZ Funds | 119 Jennings St | Ironwood Studio | Completed (09/14/2007) | 39,564.18 | 0.00 |
 | EZ Funds | 8, 10, & 12 Emory (3 Bldgs) | Duane Grieve #1 | Completed (10/30/2007) | 51,000.00 | 0.00 |
 | EZ Funds | 754 N. Broadway | James F Glasscock | Completed (01/02/2008) | 50,000.00 | 0.00 |
 | EZ Funds | 846 N. Central | 846 N. Central, LLC | Completed (04/30/2008) | 50,000.00 | 0.00 |
 | EZ Funds | 18 Emory Pl | G O M P Properties | Completed (05/14/2008) | 99,828.00 | 0.00 |
 | EZ Funds | 103 Bearden Pl | Mary Jo Bolin Madden | Completed (05/27/2008) | 19,828.94 | 0.00 |
 | EZ Funds | 912 N. Central | N Central Village | Completed (07/10/2008) | 50,000.00 | 0.00 |
 | EZ Funds | 127 Jennings St | Harley M. Lusk | Completed (08/08/2008) | 26,786.40 | 0.00 |
 | EZ Funds | 608 N. Broadway | Harbâs Carpet  | Completed (10/02/2008) | 59,112.94 | 0.00 |
 | EZ Funds | 615 N. Broadway | C&B Properties | Completed (11/18/2008) | 50,000.00 | 0.00 |
 | EZ Funds | 623 N. Central (7 Bldgs) | James Monday | Completed (03/13/2009) | 307,218.00 | 0.00 |
 | EZ Funds | 922 N. Central | Neal Green | Completed (03/19/2009) | 50,000.00 | 0.00 |
 | EZ Funds | 212 W. Magnolia | ROP, LLC | Completed (07/22/2009) | 41,697.36 | 0.00 |
 | EZ Funds | 724 N Broadway | Jim Claiborne | Completed (07/23/2009) | 50,000.00 | 0.00 |
 | EZ Funds | 1121 N. Central St. | Albert Harb | Completed (10/28/2009) | 36,536.81 | 0.00 |
 | EZ Funds | 736 N. Broadway | Khalid A. Hijer | Completed (11/17/2009) | 49,600.00 | 0.00 |
 | EZ Funds | 2634 E. Magnolia | Lakeridge Rentals | Completed (12/30/2009) | 64,959.55 | 0.00 |
 | EZ Funds | 741 N. Broadway | Paramount Cleaners | Completed (03/11/2010) | 77,200.00 | 0.00 |
 | EZ Funds | 643 N. Broadway (2 Bldgs) | Michael Denton | Completed (03/26/2010) | 100,000.00 | 0.00 |
 | EZ Funds | 600 N. Broadway | Harb's Carpet | Completed (05/03/2010) | 32,972.00 | 0.00 |
 | EZ Funds | 4111 Martin Mill | Harry K. Allen | Completed (05/20/2010) | 25,724.00 | 0.00 |
 | EZ Funds | 4305 Martin Mill Pk | Vend-A-Wash | Completed (06/01/2010) | 41,646.00 | 0.00 |
 | EZ Funds | 605 N. Broadway | DEC Land Co | Completed (06/01/2010) | 50,000.00 | 0.00 |
 | EZ Funds | 601/603 N. Broadway (2Bldgs) | 617 Central Corp | Completed (06/09/2010) | 100,000.00 | 0.00 |
 | EZ Funds | 706 N. Broadway | Cigarette Service Co | Completed (06/09/2010) | 50,000.00 | 0.00 |
 | EZ Funds | 4124 Martin Mill | Greg Snyder | Completed (06/09/2010) | 30,871.00 | 0.00 |
 | EZ Funds | 25 Emory Pl | Francis Wood | Completed (06/17/2010) | 27,400.00 | 0.00 |
 | EZ Funds | 514 W. Jackson | John Sanders | Completed (07/19/2010) | 50,000.00 | 0.00 |
 | EZ Funds | 3839 Martin Mill Pk | Todd Greene | Completed (07/30/2010) | 50,000.00 | 0.00 |
 | EZ Funds | 3832 Martin Mill | Rocky Top Heat & Air | Completed (08/01/2010) | 50,000.00 | 0.00 |
 | EZ Funds | 2125 Middlebrook Pk | SpdRcr, LLC | Completed (08/04/2010) | 50,000.00 | 0.00 |
 | EZ Funds | 3, 15, 23 Emory Place (3 Bldgs) | Emory Pl Partners | Completed (08/09/2010) | 241,212.80 | 0.00 |
 | EZ Funds | 842 N Central | 846 N. Central, LLC | Completed (08/09/2010) | 33,720.00 | 0.00 |
 | EZ Funds | 200 Jennings Ave (3 Bldgs) | Scott Partin | Completed (08/09/2010) | 134,202.00 | 0.00 |
 | EZ Funds | 4200 Martin Mill | Monir Girgia (King Tut) | Completed (08/10/2010) | 16,774.40 | 0.00 |
 | EZ Funds | 109 Bertrand | E. TN Mechanical | Completed (09/02/2010) | 32,429.00 | 0.00 |
 | EZ Funds | 1831 McCalla | E. TN Mechanical | Completed (09/02/2010) | 43,868.00 | 0.00 |
</p>
</details>