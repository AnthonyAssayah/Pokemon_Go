<img src="https://user-images.githubusercontent.com/92322613/148082594-2c6f0944-9ffd-4abc-a283-23137b6e866c.gif" width="850" height="260" />

# Pokemon Go ! <img src="https://user-images.githubusercontent.com/92322613/148254967-f5b3e6ee-c628-42c7-907c-87140e883fe4.png" height="36"> 

This project is our last assigment in OOP course, based on a ***Directed and Weighted Graphs*** implemented on *Python*. This exercise's goal is with the help of agents we have to catch all the Pokemon on the graph. Therefore, this task is divided in two main parts, the `Client` which set the connection between the server and us and `Student_code` where we programmed the algorithms and th Gui representation to allow us to really visualize the graph and all its parameters and options. 

## Design 📌

There are 3 principal classes defined in this project, we also used the different classes and interfaces from our last Python project [*EX3_OPP*](https://github.com/AnthonyAssayah/EX3_OPP.git), the interfaces are in the ```api``` package and their implementations can be found in ```classes``` package. Their properties and 
methods are detailed in our previous project. 

### <ins>***1 - The Client***<ins> 

This class is use to communicate with the server in order to import us all the data about the Pokemons and the Agents. 'client.py' contains a set of different fucntions:

  <br />
  
  | **Functions**      |    **Explanation**        |
|-----------------|-----------------------|
| `start_connection(self, ip, port)` | Use the IP ="127.0.0.1" and  port = "6666" to start a new connection to the game server. |
| `__send_message(self, msg)` | Send the encode message with the socket. |
| `get_agents(self)` | Returns the json string of agents in a pretty format. |
| `add_agent(self, json_of_node)` | Add a new agent in the json file. |
| `get_graph(self)` | Returns the graph as a json string |
| `get_info(self)` | Returns the current game info. |
| `get_pokemons(self)` | Returns the current Pokemons state as json string (value, type, location). |
| `is_running(self)` | Returns 'true' if the game is still running, else 'false'. |
| `time_to_end(self)`| Returns time to end in mili-seconds string. |
| `start(self)` | Used tp start to run the game. |
| `stop(self)` | Used to stop to end the game and upload results. |
| `move(self)` | Activate all valid choose_next_edge calls and returns the agents state. |
| `choose_next_edge(self, next_agent_node_json)` | Choose the next destination for a specific agent. |
| `log_in(self, id_str)` | Used to enter the id as str to login and upload your score to the web server. |
| `stop_connection(self)` | Used to close the connection. |
