agent_population_size = [20, 40, 80]
agent_offspring_size = [20, 40, 80]
agent_time_steps = [10, 20, 40, 60]
classifier_population_size = [20, 40, 80]
classifier_offspring_size = [20, 40, 80]
hidden_layer_agent = [1, 2]
hidden_neurons_agent = [5, 10, 25, 50, 100]
hidden_neuron_classifier = [5, 10, 25]
number_experiment = range(0, 20)

c = 0
for el in agent_population_size:
    for el1 in agent_offspring_size:
        for el2 in agent_time_steps:
            for el3 in classifier_population_size:
                for el4 in classifier_offspring_size:
                    for el5 in hidden_layer_agent:
                        for el6 in hidden_neurons_agent:
                            for el7 in hidden_neuron_classifier:
                                c += 1
print(c)