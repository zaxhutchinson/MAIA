##########################################################
# TEST AI
#
# This file is meant to test the various features of MAIA.
# And to test the methods in ai_helpers.py file.
###########################################################

#import teams.TeamAlpha.ai_helpers0 as aih
import ai_helpers as aih
import math
import random

import zmath

class AI:
    def __init__(self):
        None
        
    def initData(self, sim_data):
        self.sim_data = sim_data

        #print("SIM DATA",sim_data)



        # AI data structures

        # How far are the obstacles N,E,S,W
        # Assume the obj is surrounded.
        self.surroundings = {}
        for i in range(0,350,10):
            self.surroundings[i]=[None,1.0]

        self.first_turn = True
        self.by_ctype = None
        self.cmd_maker = aih.CmdMaker()

        #If our facing is under epsilon degrees to target,
        #Fire.
        self.targeting_epislon = 5.0

        # Fired last turn list. Reload these guns.
        self.fired_slots_by_ctype = {}

    # Implement AI here.
    # IMPORTANT: Must return commands a dictionary that follows the command
    # specifications. Can return empty dictionary or None if there are no
    # commands.
    def runAI(self,view):

        #print (view)

        #print("THE FULL VIEW: ",view)

        if self.first_turn:
            self.by_ctype = aih.getSlotIDsByCtype(view)

            self.total_turn_rate = 0.0
            for engine_slot in self.by_ctype['Engine']:
                engine = aih.getCompBySlotID(view,engine_slot)
                self.total_turn_rate += engine['max_turnrate']
            self.first_turn=False
        else:
            self.cmd_maker.reset()
        
        
        # Get some things we'll need
        my_facing = aih.getFacing(view)
        my_x = aih.getX(view)
        my_y = aih.getY(view)
        #print("FACING: ",my_facing)

        # Reload all weapons that need it
        for gun in self.by_ctype['FixedGun']:
            print("DOES IT NEED RELOADING: ",aih.doesWeaponNeedReloading(view,gun))
            if aih.doesWeaponNeedReloading(view,gun):
                #print("Reloading"+str(gun))
                self.cmd_maker.addCmd(0,gun,aih.CMD_Reload())

        

        # Transmit radar every turn
        for radar in self.by_ctype['Radar']:

            self.cmd_maker.addCmd(0,radar,aih.CMD_TransmitRadar())

        # Be default send a stop turning command. If we still want to turn
        # That can happen below
        for engine_slot in self.by_ctype['Engine']:
            self.cmd_maker.addCmd(0,engine_slot,aih.CMD_Turn(0.0))


        # If we ran the radar last turn, inspect the radar for opponent
        # And update the world around us.
        radar_views = aih.getCompViewsOfVtype(view,'radar')


        # Search for enemy tanks.
        enemy_pings = []
        for sv in radar_views:
            for ping in sv['pings']:
                if ping['objname']=='Tank' and ping['alive']:
                    enemy_pings.append(ping)



        # If we can see the enemy.
        if len(enemy_pings) > 0:

            weapon_results = aih.getCompViewsOfVtype(view,'projectile')
            for wr in weapon_results:
                if wr['objname'] != 'Tank':
                    jitter = random.randint(-5,5)
                    self.cmd_maker.addCmd(0,self.by_ctype['Engine'][0],aih.CMD_Turn(jitter))
            
            # Search through pings for the closest one.
            closest_ping = None
            closest_dist = math.inf
            #fired = False
            for ping in enemy_pings:

                # If we're facing the enemy, fire everything.
                # if ping['direction']==my_facing:
                #     for gun in self.by_ctype['FixedGun']:
                #         self.cmd_maker.addCmd(0,gun,aih.CMD_Fire())
                #         fired = True
            
                if ping['distance'] < closest_dist:
                    closest_dist = ping['distance']
                    closest_ping = ping

            

            # If we have a ping on the enemy, turn
            if closest_ping != None:
                dir_to_turn = zmath.vectorTo(my_x,my_y,closest_ping['x'],closest_ping['y'])
                # Shift the values to make it easier for knowing
                # if a left or right turn is closer.

                print("Closest enemy is "+str(closest_dist)+" away at heading "+str(dir_to_turn))

                # if dir_to_turn > 180:
                #     dir_to_turn -= 360
                theta = dir_to_turn - my_facing
                if theta < -180:
                    theta += 360
                if theta > 180:
                    theta -= 360
                #print("THETA: ",theta)
                
                # If we're within the targeting_epsilon, fire what we can.
                if abs(theta) < self.targeting_epislon:
                    for gun in self.by_ctype['FixedGun']:
                        if aih.canWeaponFire(view,gun):
                            print("FixedGun",gun,"fired.")
                            self.cmd_maker.addCmd(0,gun,aih.CMD_Fire())

                # If we can't turn all the way in one tick
                # turn the max amount.
                if abs(theta) > 0:
                    # if abs(theta) > self.total_turn_rate:
                    #     theta = self.total_turn_rate * aih.sign(theta)
                    #print("Turning",theta,"degrees")

                    for engine_slot in self.by_ctype['Engine']:
                        engine_comp = aih.getCompBySlotID(view,engine_slot)
                        # We might have multiple engines,
                        # if the first engine can handle the turn, fine.
                        if engine_comp['max_turnrate'] >= abs(theta):
                            self.cmd_maker.addCmd(0,engine_slot,aih.CMD_Turn(theta))
                            break
                        # If it can't, set max turn rate and reduce theta.
                        else:
                            turn_rate = aih.sign(theta) * engine_comp['max_turnrate']
                            self.cmd_maker.addCmd(0,engine_slot,aih.CMD_Turn(turn_rate))
                            theta -= turn_rate
                    



        print("COMMANDS: ",self.cmd_maker.getCmds())
        return self.cmd_maker.getCmds()


