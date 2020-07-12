# MAIA
Maine AI Arena

## Table of contents
* [Description](#description)
* [Running](#running)

## Description
MAIA is a platform designed for AI competitions that provides a modular 2D simulation environment for which students write AI to control competing agents. The goal is to give coders all the tools necessary so that they can focus primarily on analysis of information and decision-making. 

MAIA is written entirely in Python3 using only the modules included with a typical Python3 installation and tkinter for the UI. In other words, if you have Python3 on your machine plus tkinter, you can run MAIA. No fussy set up, compilation or libs needed. This was done so that novice coders can easily test their routines locally. Furthermore, students write AI routines in Python3 which are called directly by the simulation during the AI update phase. This allows students to leverage any Python libraries of their choice for the task.

MAIA is very configurable through JSON config files. Maps, teams, objects, components and items can be created by simply adding them to the JSON files. This allows the tournament master to create simple or complex scenarios. This allows for the dissemination of scenarios through JSON files.

MAIA was inspired by MIT's BattleCode competition: https://www.battlecode.org/. Whereas Battlecode differs radically year-to-year, MAIA is designed to be a stable, general platform in which different scenarios can be created. Our hope is that this will allow for coders to develop their routines into AI capable of general game playing.


## Running
MAIA requires:
* Python 3.8
* tkinter

Simply clone or download the repo and run: `$python3 main.py`

MAIA consists of two main UI elements:
* Setup
* Simulation

`$python3 main.py` starts the Setup UI in which you can select the map and assign teams to the predetermined sides. 