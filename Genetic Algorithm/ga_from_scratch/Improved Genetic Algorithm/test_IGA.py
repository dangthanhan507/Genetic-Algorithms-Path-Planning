from IGA import IGA
from map_lib import original_map, map2, map3


if __name__ == '__main__':
    obstacles, shape, MAP = original_map()
    ga = IGA(50, 8, 10, MAP)
    
    ga.init_population()
    print('Initial population')
    for i in ga.get_population():
        print(i)
    print('\n\n')

    for _ in range(ga.get_generations()):
        print('ITERATION: ',i)
        print(f'Checking feasibility of initial populations')
        print('SHOULD ALL BE FEASIBLE')
        for i in ga.get_population():
            if ga.check_feasibility_path(i):
                print('PATH is FEASIBLE')
            else:
                print('PATH is INFEASIBLE')
        print('\n')
        
        print('Printing Fitness of population')
        for i in ga.fitness():
            print(i)
        print('\n')

        print(f'CHOOSING TOP {ga.get_parents_mating()}')
        ga.selection()
        for i in ga.get_population():
            print(i)
        print('\n')

        print('CROSSOVER OPERATION')
        ga.crossover()
        print('  RESULTING POPULATION')
        for i in ga.get_population():
            print('   {}{:>5}'.format('FEASIBLE' if ga.check_feasibility_path(i) else 'INFEASIBLE', ' '), i)
        print('\n')

        print('MUTATION OPERATION (ADDING)')
        ga.mutation_add()
        print('  RESULTING POPULATION')
        for i in ga.get_population():
            print('   {}{:>5}'.format('FEASIBLE' if ga.check_feasibility_path(i) else 'INFEASIBLE', ' '), i)
        print('\n')

        
        print('MUTATION OPERATING (REMOVE)')
        ga.mutation_remove()
        for i in ga.get_population():
            print('   {}{:>5}'.format('FEASIBLE' if ga.check_feasibility_path(i) else 'INFEASIBLE', ' '), i)
        print('\n\n\n')
        

        print('\n\n\n')

        print('SOLUTION:')
        print('  ', ga.solution())
        print('  ', ga.convert_solution())
        print('  ', ga.fitness_function(ga.solution()))
