lattice_size <- function(data, small = FALSE, ylim = NA, title = NA) {
# make subset of rotations: either small [3:20] or large [50, 100, 150, 200]
  lattice <- data %>%
              filter(
                  if (small) {
                    n %in% c(3:50)
                  } else {
                    n %in% c(50, 100, 150, 300)
                  }
              )
  lattice$n = as.factor(lattice$n)
  if (is.na(ylim)) {
    ylim = max(lattice$L) + 20
 }

  if (is.na(title)) {
    title = ''
 }

  p <- ggplot(lattice, aes(x=n, y=L)) +
        geom_boxplot() + labs(y = "Lattice size", x = "Number of agents") + theme(text = element_text(size = 20), plot.title = element_text(hjust=0)) + ylim(0, ylim) + ggtitle(title)
  p
}

phi_phacets <- function(data, phis = c(.1, .3, .5, .7, .9)) {

  lattice <- data %>%
              filter(
                  if (small) {
                    n %in% c(3:50)
                  } else {
                    n %in% c(50, 100, 150)
                  }
              ) %>% filter(phi_men %in% phis) %>% filter(phi_women %in% phis)
  lattice$L = log(lattice$L)  # take natural logarithm
  lattice$n = as.factor(lattice$n)
  p <- ggplot(lattice, aes(x=n, y=L)) +
        geom_boxplot() + labs(y = "Lattice size", x = "Number of agents") + theme(text = element_text(size = 20))
  facets <- p + facet_grid(vars(phi_men), vars(phi_women), as.table = FALSE)
  facets
}

algorithms_perfomance_load <- function(N, distro) {
  setwd("/Users/lina/Library/Mobile\ Documents/com~apple~CloudDocs/Documents/Ph.D/SMP/Java_projects/stable-marriage/saved_data/") # FIX this to our comparisons
  if (!(distro %in% c("U", "P", "M"))) {
    stop(c(distro, " is not supported. The allowed distributions are: Uniform = U, Polar = P, Mallows = M"))
  }
  data = data.frame()
  for (i in N) {
    str = paste0("out", distro, "_", i)
    add = read.csv(str, stringsAsFactors = FALSE, header = FALSE) # download data
    # FIX Check the number of observations
    data = bind_rows(data,add)
  }
  colnames(data) = c("Type", "Time", "SE_cost", "n")
  # types = length(unique(data$Type))
  # tab = data %>% count("n") %>% mutate(freq = freq/types)
  # # start year for each player (id)
  # base2 <- ddply(data, .(n), mutate,
  # num_rep = row_number(n)
  # )
  # data$num_rep = rep(1:num_rep, each = k) # FIX

  return(data)
}


algorithms_perfomance <- function(data, metric = "SE_cost", rm.DA = FALSE) {
  # metric can be either "SE_cost" or "Time"
  # k = length(unique(data_ori$Type)) # the number of algorithms used
  # table <- data_ori  %>% count(c("n"))
  # if (any(table$freq < (num_iter * k))) {
  #   issue = which(table$freq  < (num_iter * k))
  #   stop(paste('not enough observations for n: ', table$n[issue]))
  # }
  #
  # data = data_ori %>%
  #           group_by(n) %>%
  #           filter(row_number(n) %in% 1:(num_iter * k))

  # if (all.include) {
  #   num_iter_vec = {}
  # }
  # data$id = rep(1:num_iter, each = k) # FIX
  data$n = as.factor(data$n)
  # data$id = rep(1:1000, each = k)

  data <- data %>%
            filter(
                if (rm.DA) {
                    !Type %in% c("GS_MaleOpt", "GS_FemaleOpt")
                  } else {
                  Type %in% unique(data$Type)
                }
              )
  if (metric == "SE_cost") {
      p <- ggplot(data, aes(x=n, y=SE_cost, fill = Type)) +
        geom_boxplot() + labs(y = "Sex-equality cost", x = "Number of agents") + theme(text = element_text(size = 20))
  } else {
      p <- ggplot(data, aes(x=n, y=Time, fill = Type)) +
          geom_boxplot() + labs(y = "Sex-equality cost", x = "Number of agents") + theme(text = element_text(size = 20))
  }
  p
  return(p)

  }


