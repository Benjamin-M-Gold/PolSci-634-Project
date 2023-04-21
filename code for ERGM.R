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

plot(net2, vertex.col = "Party", displaylabels = F)

flomodel <- ergm(net2 ~ edges + nodecov('Ideology')) # Estimate the theta coefficients
summary(flomodel)


## Useless code right now
V(network)$color <- rgb(1,0,0,.5)  #Define the color of Republicans
V(network)$color[which(V(network)$party=="D")] <- rgb(0,0,1,.5)  #...of Democrats
V(network)$color[which(V(network)$party=="I")] <- rgb(0,1,0,.5)  #...of Independents
plot(network, vertex.label = NA, vertex.color = V(network)$color, vertex.frame.color = NA, vertex.size = 3)
