library(igraph)
library(incidentally)
library(backbone)
library(statnet)

networkData2008 <- incidence.from.congress(session = 111, types = c("hr"), areas = c("All"), format = "igraph")
network <- sdsm(networkData2008, alpha = 0.05, narrative = TRUE)

legislatorData2008 <- read.csv("200electiondata.csv")

edgelist <- as_edgelist(network, names = TRUE)

num_nodes <- 483

node_names <- legislatorData2008$name

net2 <- network.initialize(num_nodes)
network.vertex.names(net2) <- node_names
net2[as.matrix(edgelist)] <- 1

set.vertex.attribute(net2, "Party", legislatorData2008$party)
set.vertex.attribute(net2, "State", legislatorData2008$state)
set.vertex.attribute(net2, "Endorsement", legislatorData2008$Endorsement)
set.vertex.attribute(net2, "Ideology", legislatorData2008$Ideology)

#plot(net2, vertex.col = "Party", displaylabels = F)

with_endorsement_and_party <- ergm(net2 ~ edges + nodecov('Ideology') + nodematch("Party") + nodematch("State") + nodematch('Endorsement')) # Estimate the theta coefficients
summary(with_endorsement_and_party)

without_party_with_endorsement <- ergm(net2 ~ edges + nodecov('Ideology') + nodematch("Endorsement") + nodematch("State")) # Estimate the theta coefficients
summary(without_party_with_endorsement)
