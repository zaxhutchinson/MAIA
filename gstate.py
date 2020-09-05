# gstate.py
# Global State
# By ZSH
# Created 9-1-2020

# Provides a global repository for state information.

class GState:
    def __init__(self,data):
        self.data=data
        self.items=[]
        self.objs=[]

        self.initState = None
        self.checkState = None

        if self.data['type']=='ITEM_TOUCH':
            self.checkState = self.checkItemTouch
            self.initState = self.initItemTouch
        elif self.data['type']=='ALL_OBJS_DESTROYED':
            self.checkState = self.checkAllObjsDestroyed
            self.initState = self.initAllObjsDestroyed
        elif self.data['type']=='N_OBJS_DESTROYED':
            self.checkState = self.checkNObjsDestroyed
            self.initState = self.initNObjsDestroyed
    def getData(self,key):
        return self.data[key]

    ############################################################
    # ITEM TOUCH
    def initItemTouch(self,objs,items):
        for i in items.values():
            tags=i.getData('tags')
            for t in tags:
                if t in self.data['tags']:
                    self.items.append(i)
                    break # So that we only add it once even if it matches more than one tag.

    def checkItemTouch(self):

        prev_x = None
        prev_y = None

        xstate=True
        ystate=True

        for i in self.items:
            
            if prev_x==None:
                prev_x=i.getData('x')
                prev_y=i.getData('y')
            else:
                xstate = prev_x == i.getData('x')
                ystate = prev_y == i.getData('y')
        
        self.data['state'] = xstate and ystate

        return self.data['state']

    ############################################################
    # ALL OBJS DESTROYED
    def initAllObjsDestroyed(self,objs,items):
        for o in objs.values():
            tags = o.getData('tags')
            for t in tags:
                if t in self.data['tags']:
                    self.objs.append(o)
                    break

    def checkAllObjsDestroyed(self):
        
        all_dead = True

        for o in self.objs:
            all_dead = all_dead and not o.getData('alive')

        self.data['state'] = all_dead

        return all_dead

    ############################################################
    # N OBJS DESTROYED
    def initNObjsDestroyed(self,objs,items):
        for o in objs.values():
            tags = o.getData('tags')
            for t in tags:
                if t in self.data['tags']:
                    self.objs.append(o)
                    break

    def checkNObjsDestroyed(self):

        num_dead = 0

        for o in self.objs:
            if not o.getData('alive'):
                num_dead += 1

        # Int cast just in case someone adds as string
        self.data['state'] = num_dead >= int(self.data['number'])

        return self.data['state']