library(dplyr)
library(readr)

#load data
RIS_moth_trends <- read_csv("RIS/data/RIS_moth_trends.csv")

ecological_traits <- read_csv("trait_data/data/ecological_traits.csv",skip=1)

#select columns
species_data <- RIS_moth_trends %>%
  select(common_name = COMMON_NAME,
         sci_name = SPECIES_NAME,
         growth_rate=GB_AGR)

select_ecological_traits <- ecological_traits %>% 
  select(
    sci_name = scientific_name,
    immigrant,
    resident,
    grid_squares = `gb_10_km_squares_(2000-2016)`,
    nocturnal,
    diurnal,
    easily_disturbed_by_day,
    estimated_dry_mass,
    pickiness = specificity,
    hostplant = hostplant_or_hostplant_category
  )

#combine data
species_data <- left_join(species_data,select_ecological_traits)
View(species_data)

#target columns
#name	forewing	mass	diurnal	gb_grid_squares	host_plants	resident

species_data$widespread <- species_data$grid_squares > mean(species_data$grid_squares,na.rm=T)
species_data$big <- species_data$estimated_dry_mass > mean(species_data$estimated_dry_mass,na.rm=T)


species_data$diurnal2 <- F
species_data$diurnal2[species_data$diurnal=="1"] <- T

species_data$decline <- species_data$growth_rate<0
species_data$pickiness <- substr(species_data$pickiness, 1, 1)
species_data$resident <- species_data$resident== "1"

for (i in 1:nrow(species_data)){
  split_host <- strsplit(species_data$hostplant[i]," ") %>% unlist()
  species_data$hostplant[i] <- split_host %>% head(-2) %>% paste0(collapse = " ")
}


species_data_clean <- species_data %>%
  select(
    common_name,
    sci_name,
    resident,
    diurnal = diurnal2,
    pickiness,
    decline,
    widespread,
    hostplant,
    big
  )


library(httr)
library(jsonlite)

species_data_clean$image <- ""
species_data_clean$att <- ""

#get images from inaturalist
for (i in 411:nrow(species_data_clean )){
  print(i)
  
  si_name <- species_data_clean$sci_name[i] %>% strsplit(" ") %>% unlist() %>% head(2) %>% paste0(collapse= " ")
  res <- GET("https://api.inaturalist.org/v1/taxa",
             query = list(
               q = si_name,
               per_page = 1
             ))
  data <- fromJSON(rawToChar(res$content))
  if(!is.na(data$results$default_photo)){
    species_data_clean$image[i] <- data$results$default_photo$medium_url
    species_data_clean$att[i] <- data$results$default_photo$attribution
  }
  Sys.sleep(0.5)
}


  
  
species_data_clean2 <- species_data_clean %>% filter(image != "")  
  

View(species_data_clean)

write.csv(species_data_clean,file="cleaned_stats_for_page.csv")

