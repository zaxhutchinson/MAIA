# Instructions

## Sim Setup
To set up a simulation, you should follow these steps:
* 1 Select the desired map.
* 2 Pick the teams for all sides by selecting the team AND the side and selecting *Add Team*. You can remove teams from a side by selecting the team in the right panel and clicking *Remove Team*.
* 3 Click *Build Sim*.
* 4 Click *Run Sim*.

## Running Simulations

## Self v Self
You can run a simulation pitting the same team against itself. Simply select it for all sides in sim setup. All team data is copied into separate objects during build.

## Adding Teams to the teams.json
The following is a template for a teams.json containing a single team, named TeamAlpha. TeamAlpha consists of 1 agent (size=1). The agent is defined in the agent_defs list. *Callsign* is a name specific to the agent. This provides an in-game way for agents to identify other agents that may control similar objects. The *squad* data point allows for teams to define sub-units. *Object* defines which object (from objects.json) the agent controls. *AI_file* designates the python script that will control the agent (see ai.md for instructions on creating the AI file).

```json
{
    "TeamAlpha" : {
        "size" : 1,
        "name" : "TeamAlpha",
        "agent_defs" : [
            {
                "callsign": "Leader",
                "squad" : "A",
                "object" : "2",
                "AI_file" : "AI_file0.py"
            }
        ]
    }
}
```

## Creating Team Directories
You should create a directory under the *teams* directory using a unique team name. Teams in competition cannot have the same name as the team name is used to find the AI files. Within your team directory, you place your AI class files and all other files you will need.

IMPORTANT: If you include additional python scripts in your local team subdirectory that are called by the AI class, your team directory should contain an empty file named, ```__init__.py```. This is necessary to designate the subdirectory as usable by Python.

Loading local files must be done using relative imports from the toplevel MAIA directory. For example, your team name is, TeamZero. Your AI class utilizes a custom Python script called, myscript.py. The import statement at the top of your AI script should look like:

```python
import teams.TeamZero.myscript
```

or, I suggest using:

```python
import teams.TeamZero.myscript as myscript
```

Now, let's assume your AI class file is called: *AIfile_7.py*. The directory structure from MAIA's directory would look like

- teams
    - TeamZero
        - \__init\__.py
        - AIfile_7.py
        - myscript.py