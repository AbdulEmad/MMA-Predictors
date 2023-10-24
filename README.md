# MMA-Predictors
Predicting the results of UFC fights using machine learning methods and monte carlo simulations
# Web Scraping
I got the data from ufcstats.com by scraping the website using BeautifulSoup. 
The data includes career average statistics as well as specific fight data.
# Monte Carlo Simulations
For the Monte Carlo simulations I used the number of wins/losses of a fighter and the method of each win/loss.
A proportion of the wins/losses comes from either a decision, ko or submission this can be modelled through a binomial distribution, since there are a large number of fights a gaussian distribution can be used. A score is assigned to each fighter winning by each outcome. This is done by sampling one fighter's mean and standard deviation of winning for each method, and the other's mean and standard deviation of losing for that method. In each simulation the highest score is taken as the outcome and each match up is simulated a number of times. See the notebook for more details.
# Machine Learning
The data is cleaned and then both fighter's career statistics are used to determine how they would perform in a fight against each other in terms of strikes and takedowns landed.
Using the predicted data the winner of the fight is predicted using a neural network made with PyTorch
