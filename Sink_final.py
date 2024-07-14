def main() -> str:
    #Function to read in the file
    def read_file(txt_file: str) -> list:
        objects = []
        with open(txt_file, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 3:
                    char, x, y = parts[0], int(parts[1]), int(parts[2])
                    objects.append((char, x, y))
        return objects
    
    #Define how each pipe connects
    def get_pipe_connections() -> dict:
        connections = {
            '═': {'left', 'right'},
            '║': {'top', 'bottom'},
            '╔': {'bottom', 'right'},
            '╗': {'bottom', 'left'},
            '╚': {'top', 'right'},
            '╝': {'top', 'left'},
            '╠': {'top', 'bottom', 'right'},
            '╣': {'top', 'bottom', 'left'},
            '╦': {'left', 'right', 'bottom'},
            '╩': {'left', 'right', 'top'},
        }
        
        #Add connections for all possible sinks
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ*':
            connections[letter] = {'top', 'bottom', 'left', 'right'}
        
        return connections
    
    #Construct a grid for easier searching
    def construct_grid(objects: list) -> list:
        max_x = max(obj[1] for obj in objects)
        max_y = max(obj[2] for obj in objects)
        
        grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
        for char, x, y in objects:
            grid[y][x] = char
        
        return grid
    
    #Function that finds the sinks
    def find_connected_sinks(objects: list) -> list:
        checked = set()
        connected_sinks = []
    
        def find_connected(obj: list) -> list:
            nonlocal checked, connected_sinks
            
            char, x, y = obj
            pipe_connections = get_pipe_connections()[char]

            connected = []
            for obj2 in objects:
                if obj2 != obj:
                    char2, x2, y2 = obj2
                    if (x2 == x + 1 and y2 == y and 'right' in pipe_connections and 
                        'left' in get_pipe_connections()[char2]):
                        connected.append(("right", obj2))
                    elif (x2 == x - 1 and y2 == y and 'left' in pipe_connections and 
                          'right' in get_pipe_connections()[char2]):
                        connected.append(("left", obj2))
                    elif (x2 == x and y2 == y + 1 and 'bottom' in pipe_connections and 
                          'top' in get_pipe_connections()[char2]):
                        connected.append(("bottom", obj2))
                    elif (x2 == x and y2 == y - 1 and 'top' in pipe_connections and 
                          'bottom' in get_pipe_connections()[char2]):
                        connected.append(("top", obj2))
    
            return connected
    
        def recursive_find_connections(obj:list) -> None:
            nonlocal checked, connected_sinks
    
            checked.add(obj)
            connections = find_connected(obj)
    
            for direction, connection in connections:
                if connection not in checked:
                    if connection[0] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                        connected_sinks.append(connection)
                    recursive_find_connections(connection)
    
        #Find the start
        start = None
        for obj in objects:
            if obj[0] == "*":
                start = obj
                break
    
        #Start searching for sinks
        if start:
            recursive_find_connections(start)
    
        #Extract and sort sink letters
        connected_sinks_letters = sorted(set([sink[0] for sink in connected_sinks]))
        final = ""
        for letter in connected_sinks_letters:
            final += letter
    
        return final
    
    #File name
    pipe_file = "coding_qual_input.txt"
    
    #Read in file
    objects = read_file(pipe_file)
    
    #Get letters of connected sinks then return them
    connected_sinks_letters = find_connected_sinks(objects)
    
    return connected_sinks_letters

#Call main
connected_sinks_letters = main()
print("Connected Sinks Letters:", connected_sinks_letters)
