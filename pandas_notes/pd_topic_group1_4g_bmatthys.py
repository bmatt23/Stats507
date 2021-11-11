
# Brendan Matthys, bmatthys@umich.edu

# + endofcell="--"
# ---
# jupyter:
#   jupytext:
#     cell_metadata_json: true
#     notebook_metadata_filter: markdown
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# ## Topics in Pandas
# **Stats 507, Fall 2021** 
#   

# ## Contents
# Add a bullet for each topic and link to the level 2 title header using 
# the exact title with spaces replaced by a dash. 
#
# # + [Sampling in Dataframes](#Sampling-in-Dataframes) 
# # + [Topic 2 Title](#Topic-2-Title)

# ## Sampling in Dataframes
## *Brendan Matthys* 
# Write your name in *bold* on your title slide. 

# ## Intro -- df.sample
#     

# Given that this class is for an applied statistics major, this is a really applicable topic to be writing about. This takes a dataframe and returns a random sample from that dataframe. Let's start here by just importing a dataframe that we can use for 

import pandas as pd
import os
import pickle
import numpy as np

# # +
#------------------------------------------------------------------------------
filepath =os.path.abspath('')
if not os.path.exists(filepath + "/maygames"):

    nba_url ='https://www.basketball-reference.com/leagues/NBA_2021_games-may.html'
    maygames = pd.read_html(nba_url)[0]
    maygames = maygames.drop(['Unnamed: 6','Unnamed: 7','Notes'], axis = 1)
    maygames = maygames.rename(columns = 
                               {
        'PTS':'Away Points',
        'PTS.1':'Home Points'
    })

    #dump the data to reference for later

    pickle.dump(maygames,open(os.path.join(filepath,'maygames'),'wb'))
else:
    maygames = pd.read_pickle('maygames')
    
maygames
# -

# The dataframe we will be working with is all NBA games from the 2020-2021 season played in May. We have 173 games to work with -- a relatively strong sample size.

# Let's start here with taking a sample with the default parameters just to see what the raw function itself actually does:

maygames.sample()

# The default is for this function to return a single value from the dataframe as the sample. Using the right parameters can give you exactly the sample you're looking for, but all parameters of this function are optional.

# ## How many samples?

# The first step to taking a sample from a population of data is to figure out exactly how much data you want to sample. This function has two different ways to specify this -- you can either use the parameters n or frac, but not both.
#
# ### n 
#  * This is a parameter that takes in an integer. It represents the numebr of items from the specified axis to return. If neither n or frac aren't specified, we are defaulted with n = 1.
#  
# ### frac
#  * This is a parameter that takes in a float value. That float returns the fraction of data that the sample should be, representative of the whole population. Generally speaking, the frac parameter is usually between 0 and 1, but can be higher if you want a sample larger than the population
#  
# ### Clarification 
# It's important to note that if just any number is typed in, the sample function will think that it is taking an input for n.

maygames.sample(n = 5)

maygames.sample(frac = 0.5)

print(len(maygames))
print(len(maygames.sample(frac = 0.5)))

# ## Weights and random_state

# The weights and random_state paramteres really define the way that we are going to sample from our original dataframe. Now that we have the parameter that tells us how many datapoints we want for our sample, it is imperative that we sample the right way. 
#
# ### Weights
#
# Weights helps define the probabilities of each item being picked. If the parameter is left untouched, then the default for this is that all datapoints have an equal probability of being chosen. You can choose to specify the weights in a variety of ways. 
#
# If a series is used as the parameter, the weights will align itself with the target object via the index.
#
# If a column name is used, the probabilities for being selected will be based on the value of that specific column. If the sum of the values in that column is not equal to 1, the weights of those values will be normalized so that they sum to 1. If values are missing, they will be treated as if they are weighted as 0. 

maygames.sample(n = 10, weights = 'Attend.')

# The sample above took in 10 datapoints, and was weighted based on the game attendance, so that the games with more people at them had a higher chance of being picked. 

# ### Random_state
#
# Random state is essentially the parameter for the seed we want. This creates a sample that is reproducible if you want it to be. Generally, an integer is inputted for the parameter, but an np.random.RandomState object can be inserted if wanted. The default value for this is None.

sample_1 = maygames.sample(n = 10, weights = 'Attend.', random_state = 1)
sample_1

sample_2 = maygames.sample(n = 10, weights = 'Attend.', random_state = 1)
sample_2

sample_1 == sample_2

# As you can see, the random_state parameter creates a sample that can be reproduced for future uses, which can prove to be incredibly helpful.

# ## Replace and ignore index

# The last few optional parameters we have are replace and ignore index. Both can be advantageous in their own right. 
#
# ### Replace
#
# The parameter replace specifies whether we want to be able to sample with or without replacement. It takes in a Boolean as input. If True, then the datapoint has the ability to be chosen again into the sample. If False, the datapoint is removed from the pool of possible points to be chosen. 

maygames.sample(
    n = 10,
    weights = 'Attend.',
    random_state = 1,
    replace = True)

# ### Ignore_index
#
# The ignore_index parameter is useful if you want your index to be relabeled instead of having the original index labels in the sample. This takes in a Boolean input. If True, the resulting index is relabeled, but if False (default), then the resulting index stays how it was. 

# maygames.sample(
#     n = 10,
#     weights = 'Attend.',
#     random_state = 1,
#     replace = True,
#     ignore_index = True)
# --
