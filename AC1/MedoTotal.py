from searchPlus import Problem

parametros="T=26\nM=6\nP=10"
linha1= "= = = = = = = = = =\n"
linha2= "= @ . * . . * . . =\n"
linha3= "= . = = = = = = . =\n"
linha4= "= . = F . . . . . =\n"
linha5= "= . = . . . . . . =\n"
linha6= "= . = . . . . . . =\n"
linha7= "= . = . . . . . . =\n"
linha8= "= * . . . . . . . =\n"
linha9= "= . . . . . . . . =\n"
linha10="= = = = = = = = = =\n"
grelha=linha1+linha2+linha3+linha4+linha5+linha6+linha7+linha8+linha9+linha10
mundoStandard=parametros + "\n" + grelha

class MedoTotal(Problem):
    
    def __init__(self, situacaoInicial=mundoStandard):
        super().__init__(initial = situacaoInicial)
        self.situacaoInicial = situacaoInicial
   
    def actions(self, state):
        grid, T = self.parse_grid_and_t(state)

        #Pacman's position
        pacman_x, pacman_y = None, None

        #Gets Pacmac current position
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                if grid[x][y] == '@':
                    pacman_x, pacman_y = x, y

        possible_directions = ["N", "S", "E", "W"]
        valid_actions = []

        for direction in possible_directions:
            new_x, new_y = pacman_x, pacman_y
            
            if direction == "N":
                new_x -= 1
            elif direction == "S":
                new_x += 1
            elif direction == "E":
                new_y += 1
            elif direction == "W":
                new_y -= 1
            
            if self.is_valid_position(new_x, new_y, grid, T):
                valid_actions.append(direction)
    
        return valid_actions
            
    
    def is_valid_position(self, x, y, grid, T):
        if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
            if grid[x][y] != "=":
                if grid[x][y] != ".":
                    visited_count = int(grid[x][y])
                    if visited_count < T:
                        return True
                else:
                    return True
        return False
    
    def parse_grid_and_t(self, state):
        state_lines = state.split('\n')
        parameters = state_lines[0].split('\n')
        T, M, P = map(int, parameters[0].split('=')[1].split())

        #Gets the grid of the state
        grid = [list(line) for line in state_lines[1:]]

        return grid, T
        
    def result(self, state, action):
        pass

    
    def path_cost(self, c, state1,action,next_state):
        pass
    
    def executa(self,state,actions):
        """Partindo de state, executa a sequência (lista) de acções (em actions) e devolve o último estado"""
        nstate=state
        for a in actions:
            nstate=p.result(nstate,a)
        return nstate
    
    def display(self, state):
        """Devolve a grelha em modo txt"""
        pass

    def result(self, state, action):
        # TODO
        pass

    def path_cost(self, c, state1, action, next_state):
        # TODO
        pass

    def executa(self, state, actions):
        """Partindo de state, executa a sequência (lista) de acções (em actions) e devolve o último estado"""
        nstate = state
        for a in actions:
            nstate = p.result(nstate, a)
        return nstate

    def display(self, state):
        """Devolve a grelha em modo txt"""
        return state[len(parametros)+1:len(state)]