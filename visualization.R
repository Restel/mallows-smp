# Created by: lina
# Created on: 03.04.2020
require(RcppCNPy)
require(plotly)
require(ggplot2)
require(reticulate)
require(dplyr)
require(tidyverse)
require(plyr)
require(latex2exp)
require(gridExtra)
require(qwraps2)
require(xtable)
options(qwraps2_markup = "latex")
setwd("/Users/lina/Library/Mobile Documents/com~apple~CloudDocs/Documents/Ph.D/SMP/PyCharm_Projects/PSO_StableLattice")

##### LATTICE SIZE: UNIFORM VS MALLOWS
### READ CSV LOG
source("plot_functions.R")
## Uniform
uniform_data = read.csv("LM_uniform_1000.csv", stringsAsFactors = FALSE)  # check if it is downloaded from icloud
mallows_data = read.csv("LM_mallows_1000.csv", stringsAsFactors = FALSE)
grid.arrange(lattice_size(uniform_data, ylim = 1000), lattice_size(mallows_data,  ylim = 1000), nrow = 1)
SP_SP_data = read.csv("SP_SP.csv", stringsAsFactors = FALSE)

my_summary<-
  list("The lattice size" =
       list("min" = ~ min(.data$L),
            "max" = ~ max(.data$L),
            "median (IQR)" = ~ median_iqr(.data$L),
            "mean (confidence interval)" =  ~ qwraps2::frmtci(.data$L,show_level = TRUE)),
       "The rotation poset size" =
       list("min" = ~ min(.data$R),
            "max" = ~ max(.data$R),
            "median (IQR)" = ~ qwraps2::median_iqr(.data$R),
       "mean (confidence interval)" =  ~ qwraps2::frmtci(.data$R, show_level = TRUE)
       ))
sum_uni <- summary_table(dplyr::group_by(uniform_data, n) %>% filter(n %in% c(50, 100, 150)), my_summary)

sum_mal <- summary_table(dplyr::group_by(mallows_data, n) %>% filter(n %in% c(50, 100, 150)), my_summary)
rbind(sum_uni, sum_mal)

sum_SP <-summary_table(dplyr::group_by(SP_SP_data, n) %>% filter(n %in% c(50, 100, 150)), my_summary)

### Create sampes of outliers and "normal" data in Mallows model
mallows_outlier <- filter(mallows_data, n == 150, L >= 768)
mallows_non_outlier <-filter(mallows_data, n ==150, L  %in% c(128, 48,  8)) %>% group_by(L) %>% slice(1)
data = bind_rows(mallows_outlier,mallows_non_outlier)
#write.csv(data, "mallows_1000_outs.csv")
out_data <- read.csv("outliers_mallows.csv", stringsAsFactors = FALSE)


##### MALLOWS: PHI CASE
phi_fixed = c(.1, .3, .5, .7, .9)
phi_var = c(.1, .3, .5, .7, .9)
plots = list()
for (phi in phi_fixed) {
  for (phi_v in phi_var) {
    name = paste0(phi, "_", phi_v)
    str = paste0("mallow_phi_", phi, "_", phi_v, ".csv")
    data <- read.csv(str, stringsAsFactors = FALSE)
    plots[[name]] = data
  }
}
phis_data <- dplyr::bind_rows(plots)
phi_phacets(phis_data, c(.1, .3, .5, .9))

# phis_data_large <- phis_data %>%  filter(n %in% c(50, 100, 150))
#sum_phis <- summary_table(dplyr::group_by(phis_data_large, interaction(n, phi_men, phi_women)), summary_phi)

##### POLAR MODEL
require(data.table)
polar_data_300 <- fread("LM_polar_200.csv", stringsAsFactors = FALSE)
polar_data_small <-read.csv(mgm)
lattice_size(bind_rows(, polar_data)) # FIX
sum_pol <- summary_table(polar_data_300, my_summary)

#### Perfomance of algorithms
algs = algorithms_perfomance_load(c(20, 50, 100), "U")
table(algs$n)  # must be of length [9 x num_reps] ( 9 types of algorithms)
algs_plots = algorithms_perfomance(algs, 1000, rm.DA = FALSE)
# create latex table
sum_table <- algs %>%
  dplyr::group_by(n, Type) %>%
  dplyr::summarise(mean_SE = mean(SE_cost),quantile1 = quantile(SE_cost, 0.25),quantile3 = quantile(SE_cost, 0.75), mean_time = mean(Time))
xtable(sum_table)



algs = algorithms_perfomance_load(c(150,200, 500), "U")
algs_plots = algorithms_perfomance(algs, "SE_cost", rm.DA = TRUE)
algs_plots
algs %>%
  dplyr::group_by(n, Type) %>%
  dplyr::summarise(mean_SE = mean(SE_cost),quantile1 = quantile(SE_cost, 0.25),quantile3 = quantile(SE_cost, 0.75), mean_time = mean(Time))

sum_table <- algs %>%
  dplyr::group_by(n, Type) %>%
  dplyr::summarise(mean_SE = mean(SE_cost),quantile1 = quantile(SE_cost, 0.25),quantile3 = quantile(SE_cost, 0.75), mean_time = mean(Time), N_obs = n())
xtable(sum_table)

EX = algs$SE_cost[algs$Type == "exhaustive_search_SEq_"]
PB = algs$SE_cost[algs$Type == "PowerBalance_SEq"]
BILS = algs$SE_cost[algs$Type == "iBiLS_SEq_0.125"]
t.test(EX,PB) # significant at 0.0018 p level
t.test(EX,BILS) # not significant
t.test(PB,BILS) # significant at p = .0026

###############################################
##########PREVIOUS SCRIPTS#####################
lattice_dataset <- function(str) {
  np = import("numpy")
  lattice = np$load(str)
  lattice = as.data.frame(lattice)
  full_col_names = c("size", "nagents", "time", "tau")
  col_length = length(colnames(lattice))
  colnames(lattice)[1:col_length] = full_col_names[1:col_length]
  lattice$size = as.integer(lattice$size)
  return(lattice)
}

lattice_size <- function(data, small = FALSE, ylim = NA, title = NA) {
# make subset of rotations: either small [3:20] or large [50, 100, 150, 200]
  lattice <- data %>%
              filter(
                  if (small) {
                    nagents %in% c(3:50)
                  } else {
                    nagents %in% c(50, 100, 150)
                  }
              )
  lattice$nagents = as.factor(lattice$nagents)
  if (is.na(ylim)) {
    ylim = max(lattice$size) + 20
 }

  if (is.na(title)) {
    title = ''
 }

  p <- ggplot(lattice, aes(x=nagents, y=size)) +
        geom_boxplot() + labs(y = "Lattice size", x = "Number of agents") + theme(text = element_text(size = 20), plot.title = element_text(hjust=0)) + ylim(0, ylim) + ggtitle(title)
  p
}

lattice_time<- function(data1, data2, small = FALSE) {
  data1 <- data1 %>% mutate(data1, distro = 'Uniform')
  lattice <- data2 %>% mutate(data2, distro = 'Mallows')  %>% bind_rows(data1)

  lattice <- lattice %>%
              filter(
                  if (small) {
                    nagents %in% c(3:50)
                  } else {
                    nagents %in% c(50, 100, 150)
                  }
              )
  lattice$nagents = as.factor(lattice$nagents)
 #  if (is.na(ylim)) {
 #    ylim = max(lattice$size) + 20
 # }
  p <- ggplot(lattice, aes(x=nagents, y=time, fill = distro)) +
        geom_boxplot() + labs(y = "Time", x = "Number of agents") + theme(text = element_text(size = 20), plot.title = element_text(hjust=0))
  p
}

lattice_uniform <- lattice_dataset("lattice_uniform_all.npy")
A <- lattice_size(lattice_uniform, small= FALSE, ylim = 700)
lattice_uniform_sum <- lattice_uniform %>%
                  group_by(nagents) %>%
                  dplyr::summarise(median = median(size), sd = sd(size), Q1_Q3 = paste(quantile(size, c(0.25, 0.75)), collapse = "-")
, min_max = paste(min(size), "-", max(size)), n_obs = n()) %>%
                  filter(nagents %in% c(50, 100, 150))


lattice_mallow <- lattice_dataset("lattice_mallow_all_6.npy")
B <- lattice_size(lattice_mallow, small= FALSE, ylim = 700)
grid.arrange(A, B, nrow = 1)

lattice_mallow_sum <- lattice_mallow %>%
                  group_by(nagents) %>%
                  dplyr::summarise(median = median(size), sd = sd(size), Q1_Q3 = paste(quantile(size, c(0.25, 0.75)), collapse = "-")
, min_max = paste(min(size), "-", max(size)), n_obs = n()) %>%
                  filter(nagents %in% c(50, 100, 150))



lattice_time(lattice_uniform, lattice_mallow)

lattice_mallow <- lattice_dataset("lattice_mallow_all_tau1.0.npy")
lattice_size(lattice_mallow, small= FALSE)

lattice_exp <- lattice_dataset("lattice_exp_all.npy")
lattice_size(lattice_exp, small= FALSE, title = "Polar distribution")
lattice_exp_sum <- lattice_exp %>%
                  group_by(nagents) %>%
                  dplyr::summarise(median = median(size), sd = sd(size), Q1_Q3 = paste(quantile(size, c(0.25, 0.75)), collapse = "-")
, min_max = paste(min(size), "-", max(size)), n_obs = n()) %>%
                  filter(nagents %in% c(50, 100, 150))

# SP

lattice_sp_uni <- lattice_dataset("lattice_sp_uniform_all.npy")
SP_uni <- lattice_size(lattice_sp_uni, title = "SP, Uniform", ylim = 38)

lattice_sp_id <- lattice_dataset("lattice_sp_identical_all.npy")
SP_id <- lattice_size(lattice_sp_id, title = "SP, Identical", ylim = 38)

# both sides SP
lattice_sp_sp <- lattice_dataset("lattice_sp_sp_all.npy")
SP_SP<- lattice_size(lattice_sp_sp, title = "SP, SP", ylim = 38)
grid.arrange(SP_uni, SP_SP, SP_id, nrow = 1)
### Function for rotations vs agents visualization

lattice_mallow[lattice_mallow$size ==256,] # max element!
lattice_mallow[lattice_mallow$size ==4608,] # max element!






visualize_rotations= function (str, arg = "small", title = '(B)', ylim){
  np = import("numpy")
  rotations = np$load(str)
  rotations = as.data.frame(rotations)
  colnames(rotations)[1:3] = c("npairs", "nrot", "nagents")
  rotations$nagents = as.integer(rotations$nagents)

  # make subset of rotations: either small [3:20] or large [50, 100, 150, 200]
  rotations <- rotations %>%
              filter(
                  if (arg == "small") {
                    nagents %in% c(3:20)
                  } else {
                    nagents %in% c(50, 100, 150, 200)
                  }
              )
  rotations$nagents = as.factor(rotations$nagents)
  rotations$nrot = as.integer(rotations$nrot)

  p <- ggplot(rotations, aes(x=nagents, y=nrot)) +
        geom_boxplot() + labs(y = "Rotation poset size", x = "Number of agents") + ylim(0, ylim) + ggtitle(title) + theme(text = element_text(size = 20), plot.title = element_text(hjust=0))
  p
  return(p)
}
# DONE:ggtitle("Scatter plot") + theme_bw() + theme(plot.title = element_text(hjust=0.5))
A <- visualize_rotations("uniform_rotations_moreobs.npy", title = "(A)", ylim = 11)
B <- visualize_rotations("mallow_data_moreobs.npy", title = '(B)', ylim = 11)
C <- visualize_rotations("uniform_rotations_moreobs.npy", 'large', title = '(A) Uniform', ylim = 65)
D <- visualize_rotations("mallow_data_moreobs.npy", 'large', title = '(B) Mallows', ylim = 65)
nrot <- grid.arrange(C, D, nrow = 1)
# Function for pairs visualization

visualize_pairs = function (str, N){
  np = import("numpy")
  rotations = np$load(str)
  rotations = as.data.frame(rotations)
  colnames(rotations) = c("npairs", "nrot", "nagents")
  rotations$npairs = as.numeric(rotations$npairs)
  rotations$nagents = as.factor(rotations$nagents)
  rotations$nrot = as.factor(rotations$nrot)
  subset = subset(rotations, nagents == N)
  plot = ggplot(subset, aes(x=nrot, y=npairs)) +
    geom_boxplot() + labs(x = paste("Number of rotations, the number of agents equals ", as.character(N)), y = "The median number of pairs in a rotation") + theme(text = element_text(size = 20)
  ggplotly(plot)
}


str = "mallow_data_taus_20.npy"
str = "mallow_data_taus_20_0.8.npy"
str = "mallow_data_taus_20_1.0.npy"
visualize_tau("mallow_data_taus_20_1.0.npy")
visualize_tau("mallow_data_taus_20_0.8.npy")
visualize_tau("mallow_data_taus_20_0.4.npy")
visualize_tau("mallow_data_taus_50_0.4.npy")
vizualize_tau_phi(20)
np = import("numpy")
vizualize_tau_phi <- function(N, phis = c("0.4", "0.8", "1.0")) {

  rotations = data.frame()
  for (i in (phis)) {
    str = paste("mallow_data_taus", N, i, sep = "_") %>%
      paste0(".npy")
    data = np$load(str) %>%
      as.data.frame() %>%
      mutate(phi = as.numeric(i))
    rotations = rbind(rotations, data)
  } # download all data for tau \in [0.3-0.7]

  # downloading data for tau = 1.0, 0.0
  for (i in (phis)) {
  # tau = 1.0
  str = paste("mallow_data_reversedtaus", N, i, sep = "_") %>%
      paste0(".npy")
  data = np$load(str) %>%
      as.data.frame() %>%
      mutate(phi = as.numeric(i))
  rotations = rbind(rotations, data)
  # tau = 0.0

   str = paste("mallow_data_identicaltaus", i, sep = "_") %>%
      paste0(".npy")
  data = np$load(str) %>%
      as.data.frame() %>%
      mutate(phi = as.numeric(i))
  rotations = rbind(rotations, data)
  }

  colnames(rotations) = c("npairs", "nrot", "nagents", "tau", "nrep", "phi")
  left = c(0.0, 0.3, 0.4, 0.5, 0.6, 0.7, 1.0)
  rotations <- rotations %>%
          mutate(tau = round(tau,1)) %>%
          filter(tau %in% left)
  table <- rotations  %>%
        count(c("tau", "phi"))
  if (any(table$freq < 100)) {
    issue = which(table$freq  < 100)
    stop(paste('not enough observations for taus: ', issue))
  }

  # retain 100 obs per group
   rotations = rotations %>%
              group_by(tau, phi) %>%
              filter(row_number(nrep) %in% 1:100) #

  rotations <- rotations %>%
          mutate(tau = as.factor(tau),
                  phi = as.factor(phi))
   ggplot(rotations, aes(x=tau, y=nrot, fill = phi)) +
    geom_boxplot() + labs(x = "Kendall tau distance", y = "Rotation poset size", fill = TeX('$\\phi$')) + theme(text = element_text(size = 20)) +  scale_fill_discrete(labels = c("0.4", "0.8", "1.0 (Uniform)"))
# TeX('$\\alpha^\\beta$')labs(")
}
vizualize_tau_phi(20)


visualize_tau = function (str){
  np = import("numpy")
  rotations_ori = np$load(str)
  rotations_ori = as.data.frame(rotations_ori)
  colnames(rotations_ori) = c("npairs", "nrot", "nagents", "tau", "nrep")
  left = c(0.3, 0.4, 0.5, 0.6, 0.7)
  rotations_ori <- rotations_ori %>%
          mutate(tau = round(tau,1)) %>%
          filter(tau %in% left)

  # checking if the number of observations is sufficient
  table <- rotations_ori  %>% count("tau")
  if (any(table$freq < 100)) {
    issue = which(table$freq  < 100)
    stop(paste('not enough observations for taus: ', issue))
  }
  rotations = rotations_ori %>%
              group_by(tau) %>%
              filter(row_number(nrep) %in% 1:100) # retain 100 observations per taus
  rotations$tau = as.factor(rotations$tau)
  plot = ggplot(rotations, aes(x=tau, y=nrot)) +
    geom_boxplot() + labs(x = "The value of kendal tau distance", y = "The size of a rotational poset")
  ggplotly(plot)

}

tau_distro <- function(str) {
  data <- np$load(str) %>%
          as.data.frame()
  colnames(data) = c("npairs", "nrot", "nagents", "tau", "nrep")
  data$tau = as.numeric(data$tau)
  hist(data$tau)
}


str_mallow = 'mallow_data.npy'
str_uniform = 'uniform_rotations_shuffle.npy'
visualize_rotations(str_uniform)
visualize_rotations(str_mallow)
visualize_pairs(str_uniform, N = 150)
visualize_pairs(str_mallow, N = 200)

# data_mallow = np$load(str_mallow) # check the dimension of data sets
# data_uniform = np$load(str_iniform)


np = import("numpy")
test = np$load("mallow_data_taus_20.npy")
data = npyLoad("mallow_data_taus_20.npy")
data = np$load("mallow_data.npy")


# visualize = function (str, bla){
#   rotations = npyLoad(str)
#   exp_N = c(50, 100, 150, 200) # number of agents
#   exp_N_size = length(exp_N)
#   ids = numeric(100 * exp_N_size) # generate a factor vector with number of agents for each experimnent
#   for (i in exp_N) {
#     a = match(i,exp_N) # position of i in vector exp_N
#     ids[((a-1)*100 + 1): (a*100)] = i
#   }
#   rotations = as.data.frame(rotations)
#   rotations$nagents = as.factor(ids)
#   colnames(rotations) = c("median_pairs", "n_rotations","nagents")
#   rotations_dataframe = as.data.frame(rotations)
#   rotations_dataframe[,1] = as.numeric(rotations_dataframe[,1])
#   rotations_dataframe[,2] = as.numeric(rotations_dataframe[,2])
#   subset = subset(rotations_dataframe, nagents == bla)
#   nrotations = ggplot(subset, aes(x=n_rotations, y=median_pairs)) +
#     geom_boxplot()
#   ggplotly(nrotations)
# }




