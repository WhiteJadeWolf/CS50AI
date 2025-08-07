# outdated pomegranate code
""" import pomegranate

from collections import Counter

from model import model

def generate_sample():

    # Mapping of random variable name to sample generated
    sample = {}

    # Mapping of distribution to sample generated
    parents = {}

    # Loop over all states, assuming topological order
    for state in model.states:

        # If we have a non-root node, sample conditional on parents
        if isinstance(state.distribution, pomegranate.ConditionalProbabilityTable):
            sample[state.name] = state.distribution.sample(parent_values=parents)

        # Otherwise, just sample from the distribution alone
        else:
            sample[state.name] = state.distribution.sample()

        # Keep track of the sampled value in the parents mapping
        parents[state.distribution] = sample[state.name]

    # Return generated sample
    return sample

# Rejection sampling
# Compute distribution of Appointment given that train is delayed
N = 10000
data = []

# Repeat sampling 10,000 times
for i in range(N):

    # Generate a sample based on the function that we defined earlier
    sample = generate_sample()
    
    # If, in this sample, the variable of Train has the value delayed, save the sample. Since we are interested interested in the probability distribution of Appointment given that the train is delayed, we discard the sampled where the train was on time.
    if sample["train"] == "delayed":
        data.append(sample["appointment"])

# Count how many times each value of the variable appeared. We can later normalize by dividing the results by the total number of saved samples to get the approximate probabilities of the variable that add up to 1.
print(Counter(data)) """

# pgmpy code

from pgmpy.sampling import BayesianModelSampling
from collections import Counter
from model import model


# REJECTION SAMPLING EXAMPLE #

# Create a sampler object of our Bayesian model
sampler = BayesianModelSampling(model)

# Function to generate a sample
def generate_samples(num):
   # Generate samples of size num
   samples = sampler.forward_sample(size=num)
   # print(samples)
   return samples

N = 10000
samples = generate_samples(N)


# Access sample's data
samples_dict = samples.to_dict('records')

# Print the number of times appontment was 'attended' and 'missed'
data = []
for sample in samples_dict:
   if sample['train'] == "delayed":
       data.append(sample['appointment'])


# Count data and display resuly
print(Counter(data))