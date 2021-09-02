from IGA import IGA
from map_lib import original_map


if __name__ == '__main__':
    obstacles, shape, MAP = original_map()
    ga = IGA(10, 5, 5, MAP)
    
    ga.init_population()
    print(f'initial population: {ga.get_population()}')

    print(f'Checking feasibility of initial populations')
    for i in ga.get_population():
        if ga.check_feasibility_path(i):
            print('PATH is FEASIBLE')
        else:
            print('PATH is INFEASIBLE')

