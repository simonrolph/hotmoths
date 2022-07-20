# Hot Moths in your area 🦋

By [Simon Rolph](https://github.com/simonrolph) and [Matt Brown](https://github.com/mattjbr123)

🥈🥈 Won second place in the #CDE22 hackathon! 🥈🥈

## What on earth!?!

Hot Moths was created as part of a hackathon running alongside the Constructing a Digital Environmnet conference. The hackathon was titled "Bridging data sciences and the public with art (hybrid)" and was run on the DEVPOST platform. You can find our entry here: https://devpost.com/software/hot-moths

The goal of the hackathon was to "turn scientific data into art creations, in any format, to enhance the communications between scientists and the public." Insect declines are an active topic of research and often makes the news with concerning headlines of 'insectmageddon'. Big trends like this can be overwhelming and we feel a disconnect from these phenomena. We wanted to create a piece of art that helps users appreciate the diversity in an underappreciated taxonomic group. We turned data about moths into an interactive experiental art piece framed around a reimagining of the swipe-style dating app in a near future where we could talk to moths...

a.k.a. we created Tinder for moths!

We were inspired by two main data sources:

 * [Traits data for the butterflies and macro-moths of Great Britain and Ireland, 2021](https://catalogue.ceh.ac.uk/documents/5b5a13b6-2304-47e3-9c9d-35237d1232c6)
 * [Moth trends for Britain and Ireland from the Rothamsted Insect Survey light-trap network (1968 to 2016)](https://catalogue.ceh.ac.uk/documents/0a7d65e8-8bc8-46e5-ab72-ee64ed851583)
 
These data sources contained very rich information about species, their ecology and their long term trends. However, excel sheets full of numbers are not engaging and the aim of our project is to bridge the gap from this data to the public through art.

We also used iNaturalist API species images and the locations of a nearby record of that species. https://api.inaturalist.org/v1/docs/

## How we built it

The user interface was adapted from a basic tinder swipe deck template created by Rob Vermeer: https://codepen.io/RobVermeer/pen/japZpY

The data was downloaded from EIDC and processed in R using R pacakge dplyr to produce a simplified dataframe containing a set of variables for each moth. For example whether they were resident or migrant, their food preferences and so on. The iNaturalist API was used to get a url for an image for each species. We combined the two EIDC datasets together so that for each species we had their traits and their long term trend from the RIS monitoring dataset.

We wrote a series of short sentences that a moth might include in their profile to reflect each of the variables. For example if a species is resident, this might be translated into their bio as 'local lad'. These were also put in a simple spreadsheet.

Building the moth bios was an exercise in natural language generation (NGL) done in Python by picking relevant sentences from the spreadsheets based on the traits and building bios procedurally from these for each moth. These bios were then input into an html template to build the final website.

## Screenshots

![image](https://user-images.githubusercontent.com/17750766/178946060-52295fd4-93cb-4034-957f-f93745d73314.png)
![image](https://user-images.githubusercontent.com/17750766/178946135-67822186-4a39-4c35-b74c-7d199f61beb7.png)
![image](https://user-images.githubusercontent.com/17750766/178946199-041878f3-d0d4-4fb6-9591-aa2299f62667.png)
![image](https://user-images.githubusercontent.com/17750766/178946251-1f633fcd-a2fd-4da6-bcda-c10031e614a3.png)
