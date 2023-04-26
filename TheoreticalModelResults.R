library(tidyverse)
library(tidymodels)

data <- read.csv("TheoreticalData.csv") %>%
  mutate(cosponsors = case_when(Bills_Cosponsored > 0 ~ "Cosponsors", TRUE ~ "Not Cosponsors"),
         coendorsers = case_when(Co.Endorsement == 1 ~ "Co-Endorsers", TRUE ~ "Not Co-Endorsers"))

ggplot(data = data, aes(x = ideology, y = Bills_Cosponsored, color = Co.Endorsement)) +
  geom_point() + 
  facet_wrap(~Spread) +
  labs(x = "Ideology", y = "Number of Bills Co-sponsored",
       title = "Do co-endorsers co-sponsor more bills?",
       subtitle = "Facetted by the spread of party ideology")

ggplot(data = data, mapping = aes(x = cosponsors, fill = coendorsers)) +
  geom_bar(position = "fill") +
  labs(y = "proportion") + 
  facet_wrap(~Cosponsorship_Strength) + 
  labs(x = "Co-Sponsorship", y = "Proportion who are Coendorsers", 
       title = "Are cosponsorship and co-endorsement indepenent?",
       subtitle = "Facetted by the importance of co-endorsement to cosponsorship parameter")

ggplot(data = data, mapping = aes(x = cosponsors, fill = coendorsers)) +
  geom_bar(position = "fill") +
  labs(y = "proportion") + 
  facet_wrap(~Spread) +
  labs(x = "Co-Sponsorship", y = "Proportion who are Coendorsers", 
       title = "Are cosponsorship and co-endorsement indepenent?",
       subtitle = "Facetted by the spread of party ideology")

m1 <- lm(data = data, Bills_Cosponsored ~ ideology + coendorsers)
summary(m1)

