from opt_flow.core import BasePopulation
from structure.individual import Individual
from structure.instance import Instance

class EmptyIndividual(BasePopulation):
    
    def create(self) -> Individual:
        data: Instance = self.data
        empty_individual = Individual(self.data)
        for _ in data.nodes:
            empty_individual.add_empty_route()
        return empty_individual