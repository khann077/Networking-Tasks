# Devajya Khanna
# Spring 2024 CSCI 4211: Introduction to Computer Networks
# This program serves as the sender in a Stop-and-Wait data 
# transfer. It was written in Python v3.

from simulator import sim
from simulator import to_layer_three
from event_list import evl
from packet import *

class S_sender:
    ''' Represents the Sender in the Stop-and-Wait protocol. '''
    def __init__(self):
        ''' Initializes the relevant class variables for the Sender. '''
        # Note: Do NOT change any of the provided class variable names as they 
        # will be used for evaluation.
        
        # For Stop-and-Wait, the state can be "WAIT_LAYER5" or "WAIT_ACK".
            # "WAIT_LAYER5" is the state where the Sender waits for messages 
            # from the application layer (layer 5).
            # "WAIT_ACK" is the state where the Sender waits to receive an 
            # ACK from the Receiver.
        self.state = "WAIT_LAYER5"
        # The sequence number of the next packet that will be sent.
        self.seq = 0
        # This should be used as the second argument to evl.start_timer().
        self.estimated_rtt = 30
        # This should be used as the first argument to to_layer_three() and 
        # evl.start_timer().
        self.entity = 'S'
        

        # TODO: Initialize any other useful class variables you can think of.
        self.lastTransmit = ""

        return

    def S_output(self, message):
        '''
        The Sender received a message from layer 5, so it should try to create
        a packet containing the message and send it to layer 3.
        
        Parameters
        ----------
        - message : msg
            - The message the Sender received from layer 5.
        '''
        # Follow the finite state machine (FSM) to know the exact actions that 
        # should be taken in each state to send this message to the receiver and 
        # review section 2.5.2 Software Interfaces in the Project Instructions 
        # for how to use each method.
        # TODO: 
        # 1) Verify the current state of the Sender to make sure it should
            # actually send the message to the Receiver.
        # 2) Send the message 
            # Use the message when constructing the new packet.
            # new_packet = packet(seqnum = self.seq, payload = message)
            # Send the packet to the Receiver.
            # to_layer_three(self.entity, new_packet)
        # 3) Start the timer (you only need one timer)
        # 4) Check what you need to do to handle if the packet you sent is 
            # lost or corrupted. 
        # 5) Do not forget to update the class variables and the statistics 
        # counters accordingly.
        
        if self.state == "WAIT_LAYER5":
        # Construct a new packet using the current sequence number and the received message.
            
            new_packet = packet(seqnum=self.seq, payload=message)
            # Send the packet to the Receiver.
            to_layer_three(self.entity, new_packet)
            self.lastTransmit = message
            sim.totalMsgSent+=1
            # Start the timer for the packet.
            evl.start_timer(self.entity, self.estimated_rtt)
            # Update the state to "WAIT_ACK".
            self.state = "WAIT_ACK"
        else:
            print("waiting for ack, new message dropped: " + message.data)
            sim.droppedData += 1
        return


    def S_input(self, received_packet):
        '''
        The Sender received a packet from layer 3. It should verify the
        received packet and behave accordingly. 
        
        Parameters
        ----------
        - received_packet : packet
            - The received packet that was sent by the Receiver.
        '''
        # Check the FSM to know the actions to take and review section 2.5.2 
        # Software Interfaces in the Project Instructions for how to use each 
        # method.
        # TODO: Verify the current state of the Sender to make sure it should 
        # actually process the received packet, the checksum to make sure that
        # received packet is uncorrupted, and the acknowledgment number to see
        # whether it is the expected one.
                
        if self.state == "WAIT_ACK":
        # Check if the received packet is not corrupted using the checksum.
            if received_packet.checksum == received_packet.get_checksum():
                # Check if the acknowledgment number is the expected one.
                if received_packet.acknum == self.seq:
                    # Stop the timer since the acknowledgment is received.
                    evl.remove_timer()
                    # Update the state to "WAIT_LAYER5" for the next message.
                    self.state = "WAIT_LAYER5"
                    # Increment the sequence number for the next packet.
                    self.seq = 1 - self.seq
                else:
                    # received packet has the wrong sequence number
                    sim.droppedAck += 1
            else:
                # ACK is corrupted/fails checksum
                sim.corruptedAck += 1
                sim.droppedAck += 1
        else:
            # sender cannot receive ack/ is not in state to do so, so it ignores/drops the packet
            sim.droppedAck += 1
        return


    def S_handle_timer(self):
        ''' Handles the expiration of the Sender's timer. If this function
            is triggered, then it means that the ACK for the most recently 
            sent packet wasn't received by the Sender in time, so the packet 
            needs to be retransmitted. '''
        # Check the FSM to know the actions to take and review section 2.5.2 
        # Software Interfaces and 2.5.4 Helpful Hints in the Project Instructions
        # for how to use each method and how to handle timers.
        # TODO: Verify the current state of the Sender to make sure it should 
        # actually handle the timeout. Retransmit the most recently sent packet 
        # and start the timer again.

        if self.state == "WAIT_ACK":
            # Retransmit the most recently sent packet.
            to_layer_three(self.entity, packet(seqnum=self.seq, payload=self.lastTransmit))
            sim.totalMsgSent+=1
            sim.retransmittedData += 1
            # Restart the timer for the retransmitted packet.
            evl.start_timer(self.entity, self.estimated_rtt)

        return

a = S_sender()