import ai_helpers as aih
import random


class AI:
    def __init__(self):
        None

    def initData(self, sim_data):
        # Store the sim_data in case we need to reference something.
        self.sim_data = sim_data

        # Create a CmdMaker obj
        self.cmd_maker = aih.CmdMaker()

        # Set our state
        self.state = 0

        # #################################
        # Stored data
        self.is_initd = False
        self.gamemap = {}
        self.slots_by_ctype = None
        self.tick = 0
        self.start_performed = False
        self.cmd_iteration = 0

        self.start_cmds_a = [
            aih.CMD_Turn(-45),
            aih.CMD_Turn(0),
            aih.CMD_SetSpeed(1),
            aih.CMD_SetSpeed(1),
            aih.CMD_SetSpeed(1),
            aih.CMD_Turn(45),
            aih.CMD_Turn(0),
        ]

        self.start_cmds_b = [
            aih.CMD_Turn(90),
            aih.CMD_Turn(45),
            aih.CMD_Turn(0),
            aih.CMD_SetSpeed(1),
            aih.CMD_SetSpeed(1),
            aih.CMD_SetSpeed(1),
            aih.CMD_Turn(45),
            aih.CMD_Turn(0)
        ]

    def initRunTime(self, view):
        self.is_initd = True
        self.slots_by_ctype = aih.getSlotIDsByCtype(view)

    def getSlot(self, ctype):
        return self.slots_by_ctype[ctype][0]

    def updateMap(self, view):

        loc = (aih.getX(view), aih.getY(view))

        if loc not in self.gamemap:
            self.gamemap[loc] = None
        else:
            pass

    def distance(self, locA, locB):
        return ((locB[0] - locA[0]) ** 2 + (locB[1] - locA[1]) ** 2) ** 0.5

    def checkForEnemyObj(self, view, objname):
        pings = aih.searchRadarForObjname(view, "Blue Tank")

        # If we see the blue tank, shoot!
        if len(pings) > 0:
            if aih.canWeaponFire(view, self.getSlot("FixedGun")):
                self.cmd_maker.addCmd(0, self.getSlot("FixedGun"), aih.CMD_Fire())

        # Always check if we need to reload.
        if aih.doesWeaponNeedReloading(view, self.getSlot("FixedGun")):
            self.cmd_maker.addCmd(0, self.getSlot("FixedGun"), aih.CMD_Reload())

    def determineNextMove(self, view):
        pings = aih.searchRadarForObjname(view, "Indestructible Block")
        myloc = (aih.getX(view), aih.getY(view))
        if len(pings) > 0:

            objloc = (pings[0]["x"], pings[0]["y"])
            dist = self.distance(objloc, myloc)
            engine_slots = self.slots_by_ctype["Engine"]
            turn_rate = 0.0
            speed = 0.0

            for es in engine_slots:
                engine_comp = aih.getCompBySlotID(view, es)
                turn_rate += engine_comp["cur_turnrate"]
                speed += engine_comp["cur_speed"]

            # If we're far from an indestructible block...
            if dist > 2:
                # First, if we're turning, stop.
                if turn_rate < 0 or turn_rate > 0:
                    self.cmd_maker.addCmd(
                        self.tick, self.getSlot("Engine"), aih.CMD_Turn(0.0)
                    )
                # If we're standing still, move.
                elif speed == 0:
                    self.cmd_maker.addCmd(
                        self.tick, self.getSlot("Engine"), aih.CMD_SetSpeed(1.0)
                    )
                # Otherwise, 10% of the time, turn a random amount left or right.
                elif random.random() < 0.1:
                    self.cmd_maker.addCmd(
                        self.tick,
                        self.getSlot("Engine"),
                        aih.CMD_Turn(random.uniform(-36.0, 36.0)),
                    )
            # If we're close to a block, we want to stop moving forward
            # and turn.
            elif dist <= 2:
                # Stop moving
                if speed > 0:
                    self.cmd_maker.addCmd(
                        self.tick, self.getSlot("Engine"), aih.CMD_SetSpeed(0.0)
                    )
                # Turn in a random direction 18 deg per turn (or 1/20th of a circle).
                if turn_rate == 0:
                    self.cmd_maker.addCmd(
                        self.tick,
                        self.getSlot("Engine"),
                        aih.CMD_Turn(random.choice([-18.0, 18.0])),
                    )

    #Performs appropriate start actions based on starting location
    def startAction(self, view):
        

    # Implement AI here.
    # IMPORTANT: Must return commands a dictionary that follows the command
    # specifications. Can return empty dictionary or None if there are no
    # commands.
    def runAI(self, view):

        self.cmd_maker.reset()

        if not self.is_initd:
            self.initRunTime(view)

            self.cmd_maker.addCmd(
                self.tick, self.getSlot("Radar"), aih.CMD_ActivateRadar()
            )

        self.updateMap(view)

        if not (start_performed):
            start_performed = self.startAction(view, cmd_iteration)
        
        if (start_performed):
            self.checkForEnemyObj(view, "Red Tank")
            self.determineNextMove(view)

        return self.cmd_maker.getCmds()
