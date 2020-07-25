import traceback

LOG_MAIN = 'log/main.log'
LOG_ERROR = 'log/error.log'
LOG_COMBAT = 'log/combat.log'
LOG_DEBUG = 'log/debug.log'
DEBUG = False

def LogInit():
    with open(LOG_MAIN,'w') as f:
        f.write('')
    with open(LOG_ERROR,'w') as f:
        f.write('')
    with open(LOG_COMBAT,'w') as f:
        f.write('')
    with open(LOG_DEBUG,'w') as f:
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

def LogSetDebug(val):
    global DEBUG
    DEBUG=val
def LogDebug(msg):
    if DEBUG:
        with open(LOG_DEBUG,'a') as f:
            f.write(msg)

def LogMostRecentException(msg):
    with open(LOG_ERROR,'a') as f:
        f.write("##### EXCEPTION #####\n")
        f.write(msg+"\n")
        traceback.print_exc(file=f)