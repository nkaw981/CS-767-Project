import ast
import statistics

with open("results_50%.txt") as file:
    mean = []
    median = []
    agents = []

    for line in file.read().split("\n"):
        print(round(float(ast.literal_eval(line)['mean']), 6))
        #print(float(ast.literal_eval(line)['mean']) - float(ast.literal_eval(line)['median']))
        mean.append(float(ast.literal_eval(line)['mean']))
        median.append(float(ast.literal_eval(line)['median']))
        agents.append(float(ast.literal_eval(line)['count']))
    print("Mean:", statistics.mean(mean))
    print("Median:", statistics.mean(median))
    print("Count:", statistics.mean(agents))
    