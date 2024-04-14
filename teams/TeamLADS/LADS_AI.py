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
        self.cmd_start_iteration = 0
        self.cmd_iteration = 0
        self.start_cmd_set = []

        self.start_cmds_a = [
            aih.CMD_Turn(-45),
            aih.CMD_Turn(0),
            aih.CMD_SetSpeed(1),
            aih.CMD_SetSpeed(1),
            aih.CMD_SetSpeed(1),
            aih.CMD_SetSpeed(1),
            aih.CMD_SetSpeed(0),
            aih.CMD_Turn(45),
            aih.CMD_Turn(0),
            aih.CMD_Turn(0),
        ]

        self.start_cmds_b = [
            aih.CMD_Turn(90),
            aih.CMD_Turn(45),
            aih.CMD_Turn(0),
            aih.CMD_SetSpeed(1),
            aih.CMD_SetSpeed(1),
            aih.CMD_SetSpeed(1),
            aih.CMD_SetSpeed(1),
            aih.CMD_SetSpeed(0),
            aih.CMD_Turn(45),
            aih.CMD_Turn(0),
            aih.CMD_Turn(0),
        ]

        self.cmd = [
            aih.CMD_SetSpeed(1),
            aih.CMD_SetSpeed(1),
            aih.CMD_SetSpeed(1),
            aih.CMD_SetSpeed(1),
            aih.CMD_SetSpeed(1),
            aih.CMD_SetSpeed(1),
            aih.CMD_SetSpeed(0),
            aih.CMD_Turn(30),
            aih.CMD_Turn(30),
            aih.CMD_Turn(30),
            aih.CMD_Turn(30),
            aih.CMD_Turn(30),
            aih.CMD_Turn(30),
            aih.CMD_Turn(30),
            aih.CMD_Turn(30),
            aih.CMD_Turn(30),
            aih.CMD_Turn(30),
            aih.CMD_Turn(30),
            aih.CMD_Turn(30),
            aih.CMD_Turn(30),
            aih.CMD_Turn(30),
            aih.CMD_Turn(30),
            aih.CMD_Turn(30),
            aih.CMD_Turn(30),
            aih.CMD_Turn(30),
            aih.CMD_Turn(30),
            aih.CMD_Turn(30),
            aih.CMD_Turn(30),
            aih.CMD_Turn(0),
            aih.CMD_Turn(0),
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
        pings = aih.searchRadarForObjname(view, "Red Tank")

        # If we see the blue tank, shoot!
        if len(pings) > 0:
            if aih.canWeaponFire(view, self.getSlot("FixedGun")):
                self.cmd_maker.addCmd(0, self.getSlot("FixedGun"), aih.CMD_Fire())

        # Always check if we need to reload.
        if aih.doesWeaponNeedReloading(view, self.getSlot("FixedGun")):
            self.cmd_maker.addCmd(0, self.getSlot("FixedGun"), aih.CMD_Reload())

    def determineNextMove(self, view):
        self.cmd_maker.addCmd(
            self.tick, self.getSlot("Engine"), self.cmd[self.cmd_iteration]
        )
        self.cmd_iteration += 1
        if len(self.cmd) <= self.cmd_iteration:
            self.cmd_iteration = 0

    # Performs appropriate start actions based on starting location
    def startAction(self, view):
        self.cmd_maker.addCmd(
            self.tick,
            self.getSlot("Engine"),
            self.start_cmd_set[self.cmd_start_iteration],
        )
        self.cmd_start_iteration += 1
        return len(self.start_cmd_set) <= self.cmd_start_iteration

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

        if (aih.getX(view), aih.getY(view)) == (1, 13):
            self.start_cmd_set = self.start_cmds_a
        elif (aih.getX(view), aih.getY(view)) == (13, 1):
            self.start_cmd_set = self.start_cmds_b

        if not (self.start_performed):
            self.start_performed = self.startAction(view)

        if self.start_performed:
            self.checkForEnemyObj(view, "Red Tank")
            self.determineNextMove(view)

        return self.cmd_maker.getCmds()
