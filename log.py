LOG_MAIN = 'log/main.log'
LOG_ERROR = 'log/error.log'
LOG_COMBAT = 'log/combat.log'

def LogInit():
    with open(LOG_MAIN,'w') as f:
        f.write('')
    with open(LOG_ERROR,'w') as f:
        f.write('')
    with open(LOG_COMBAT,'w') as f:
        f.write('')

def LogMsg(msg):
    with open(LOG_MAIN,'a') as f:
        f.write(msg+'\n')

def LogError(msg):
    with open(LOG_ERROR,'a') as f:
        f.write(msg+'\n')

def LogCombat(time,msg):
    with open(LOG_COMBAT,'a') as f:
        f.write(str(time)+" "+msg)
