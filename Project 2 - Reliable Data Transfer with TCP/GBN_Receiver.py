# Spring 2024 CSCI 4211: Introduction to Computer Networks
# This program serves as the receiver in a Go-Back-N data 
# transfer. It was written in Python v3.

from simulator import sim
from simulator import to_layer_five
from packet import send_ack

class R_receiver:
    ''' Represents the Receiver in the Go-Back-N protocol. '''
    def __init__(self):
        ''' Initializes the relevant class variables for the Receiver. '''

        # Note: Do NOT change any of the provided class variable names as they 
        # will be used for evaluation.

        # The sequence number of next packet that is expected to be received
        # from the Sender.
        self.seqnum = 0
        # This should be used as the first argument to to_layer_five() and 
        # send_ack().
        self.entity = 'R'
        self.seqOfLastCorrectlyReceived = -1
        return

    def R_input(self, received_packet):
        ''' 
        The Receiver received a packet from layer 3. It should verify the
        received packet and behave accordingly. 
        
        Parameters
        ----------
        - received_packet : packet
            - The received packet that was sent by the Sender.
        ''' 
        # Check the FSM to know the actions to take and review section 2.5.2 
        # Software Interfaces in the Project Instructions for how to use each 
        # method.
        # TODO: If the packet is correct, deliver to layer 5 and take the 
        # necessary actions as descriped in the FSM.
        
        if received_packet.get_checksum() != received_packet.checksum:
            sim.droppedData += 1
            sim.corruptedData += 1
            return
        
        if received_packet.seqnum == self.seqnum:
            data = received_packet.payload.data
            to_layer_five(self.entity, data)
            sim.totalMsgSent += 1
            send_ack(self.entity, self.seqnum)
            self.seqOfLastCorrectlyReceived = self.seqnum
            self.seqnum += 1
        else:
            send_ack(self.entity, self.seqOfLastCorrectlyReceived)
            # update counter
            sim.droppedData += 1
            sim.retransmittedAck += 1
            sim.totalMsgSent += 1
            
       
        return

b = R_receiver()