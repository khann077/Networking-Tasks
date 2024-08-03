# Spring 2024 CSCI 4211: Introduction to Computer Networks
# This program serves as the sender in a Go-Back-N data 
# transfer. It was written in Python v3.

from simulator import sim
from simulator import to_layer_three
from event_list import evl
from packet import *
from circular_buffer import circular_buffer

class S_sender:
    ''' Represents the Sender in the Go-Back-N protocol. '''
    def __init__(self):
        ''' Initializes the relevant class variables for the Sender. '''
        # Note: Do NOT change any of the provided class variable names as they 
        # will be used for evaluation.
        
        # The sequence number of the next packet that will be sent.
        self.seq = 0
        # This should be used as the second argument to evl.start_timer().
        self.estimated_rtt = 30
        # This should be used as the first argument to to_layer_three() and 
        # evl.start_timer().
        self.entity = 'S'
        # The circular buffer that will store any outstanding and 
        # unacknowledged packets.
        self.c_b = circular_buffer(5)

        # TODO: Initialize any other useful class variables you can think of.
        
        self.window_size = 3
        self.send_base = 0
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
        # Check the FSM to know the actions to take and review section 2.5.2 
        # Software Interfaces in the Project Instructions for how to use each 
        # method.
        # TODO: Implement the output function as mentioned in the FSM to send 
        # the message to the receiver if the circular buffer isn't full. If it 
        # is, then drop the message and update your variables and indicate 
        # that in your output and update the statistics counters accordingly.

        if self.c_b.isfull():
            sim.droppedData += 1
            print("window full, new message is dropped: " + message.data)
            return


        if self.seq < self.send_base + self.window_size : 
            pckt = packet(seqnum=self.seq, payload=message, acknum=self.seq)
            self.c_b.push(pckt)
            to_layer_three(self.entity, pckt)
            sim.totalMsgSent += 1
            if self.send_base == self.seq:
                evl.start_timer(self.entity, self.estimated_rtt)
            self.seq += 1
        else:
            sim.droppedData += 1
            print("window full, new message is dropped: " + message.data)

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
        # TODO: Verify the received packet's checksum to make sure that it's
        # uncorrupted and it's acknowledgment number to see whether it is 
        # within the Sender's window. Update the circular buffer based on the 
        # received acknowledgment number using pop(). Go-Back-N uses cumulative 
        # ACKs meaning that more than one packet may need to be removed 
        # from the circular buffer.

        if received_packet.checksum != received_packet.get_checksum():
            # ACK is corrupted/fails checksum
            sim.corruptedAck += 1
            sim.droppedAck += 1
            return
       

        if received_packet.acknum >= self.send_base:
            num_packets_acked = received_packet.acknum - self.send_base +1
            for _ in range(num_packets_acked):
                self.c_b.pop()
                self.send_base += 1

            if self.send_base == self.seq:
                evl.remove_timer()
            else:
                evl.start_timer(self.entity, self.estimated_rtt)
        else:
            sim.droppedAck += 1
            pass
            # update counter

        return


    def S_handle_timer(self):
        ''' Handles the expiration of the Sender's timer. If this function
            is triggered, then it means that an ACK for any of the most 
            recently sent packets wasn't received by the Sender in time, so 
            all currently outstanding and unacknowledged packet needs to be 
            retransmitted. '''
        # Check the FSM to know the actions to take and review section 2.5.2 
        # Software Interfaces and 2.5.4 Helpful Hints in the Project Instructions
        # for how to use each method and how to handle timers.
        # TODO: Send all the unACKed packets in the circular buffer.
        evl.start_timer(self.entity, self.estimated_rtt)
        for pckt in self.c_b.read_all():
            sim.totalMsgSent += 1
            sim.retransmittedData += 1
            to_layer_three(self.entity, pckt)

        return

a = S_sender()