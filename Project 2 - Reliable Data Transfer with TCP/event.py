# Do NOT modify this file.

class event:
    ''' Represents an event that occurs in the simulation. '''
    def __init__(self, evtime, evtype, eventity, pkt = None):
        ''' 
        Initializes the relevant class variables of an event.
        
        Parameters
        ----------
        - evtime : float
            - Event time.
        - evtype : str 
            - Event type code (e.g., "FROM_LAYER5", "FROM_LAYER3", or 
              "TIMER_INTERRUPT").
        - eventity : char
            - The character "S" to represent that the Sender or "R" to 
              represent that the Receiver is the entity this event is for.
        - pkt : packet
            - A pointer to a packet (if any) that's associated with this event.
        '''
        self.evtime = evtime
        self.evtype = evtype
        self.eventity = eventity
        self.pkt = pkt
        self.prev = None
        self.next = None

    def print_self(self):
        ''' Prints out relevant information about this event. '''
        print(f"Event time: {self.evtime}, type: {self.evtype}, entity: {self.eventity}\n")