library(igraph)
library(incidentally)
library(backbone)
library(statnet)

d <- incidence.from.congress(session = 116, types = c("hr"), areas = c("All"), format = "data")
network <- sdsm(I, alpha = 0.05, narrative = TRUE)

V(network)$color <- rgb(1,0,0,.5)  #Define the color of Republicans
V(network)$color[which(V(network)$party=="D")] <- rgb(0,0,1,.5)  #...of Democrats
V(network)$color[which(V(network)$party=="I")] <- rgb(0,1,0,.5)  #...of Independents
plot(network, vertex.label = NA, vertex.color = V(network)$color, vertex.frame.color = NA, vertex.size = 3)

edgelist <- as_edgelist(network, names = TRUE)

net <- as.network(x = edgelist, directed = FALSE, loops = FALSE, matrix.type = "adjacency")

num_nodes <- 467

node_names <- d$legislator$name

net2 <- network.initialize(num_nodes)
network.vertex.names(net2) <- node_names
net2[as.matrix(edgelist)] <- 1

set.vertex.attribute(net2, "Party", d$legislator$party)
set.vertex.attribute(net2, "State", d$legislator$state)

plot(net2, vertex.col = "Party", displaylabels = F)