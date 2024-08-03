#!/usr/bin/env python

# Spring 2024 CSCI 4211: Introduction to Computer Networks
# This program serves as the SDN controller for the Ethernet-based
# self-learning switches. It was written in Python v3.

from pox.core import core
import pox.openflow.libopenflow_01 as of

# Even a simple usage of the logger is much nicer than print!
log = core.getLogger()

# TODO: Define your global data structures here.
topology = {} # entry n the form of {switch: {hostmac1:port, hostmac2: port ...}}


flood_counter = 0
packets_received = 0

def _handle_PacketIn(event):
  '''
  Handle an OFPacketIn message that a switch has sent to the controller because
  the switch doesn't have a matching rule for the packet it received.
  '''
  global flood_counter
  global packets_received
  packets_received += 1
  log.info('Number of packets received so far: {}'.format(packets_received))
  log.info('Number of ports flooded so far: {}'.format(flood_counter))
  
  # Get the port the packet came in on for the switch that's contacting the 
  # controller.
  packet_input_port = event.port

  # Get the number of ports attached to the sending switch except for the
  # packet's input port. This variable should be used when updating your 
  # global flood counter.
  other_ports = len(event.connection.ports) - 2

  # Use POX to parse the packet.
  packet = event.parsed

  # Get the packet's source and destination MAC addresses.
  src_mac = str(packet.src)
  dst_mac = str(packet.dst)

  # Get the sending switch's ID.
  switch_ID = str(event.connection.dpid) + str(event.connection.ID)
  
  # This line of code prints infomation about packets that are sent to the 
  # controller.
  log.info('Packet has arrived: SRCMAC:{} DSTMAC:{} from switch:{} in-port:{}'.format(src_mac, dst_mac, switch_ID, packet_input_port))

  # TODO: Update the controller's global data structure that stores the 
  # information it learns about the network topology to include an entry for 
  # the packet's source host and the sending switch's port that can reach it, 
  # if such an entry does not already exist.
  if topology.get(switch_ID) is None : 
    topology[switch_ID] = {}

  switch_table = topology.get(switch_ID)
  switch_table[src_mac] = packet_input_port

  # TODO: If the network topology already has an entry for the sending switch 
  # and the destination host, then install a new match-action rule or rules 
  # in the sending switch and have the original packet be fowarded to the 
  # correct output port. This is where you should use the code setting
  # message.match that was provided in Section 2.3 of the Phase 3 
  # instructions. Note: You will need to implement more code than the single 
  # line that is given to you.
  output_port = switch_table.get(dst_mac)
  log.info("ouput port is {}".format(output_port))
  if output_port is not None:
    if packet_input_port == output_port:
      log.info("Dropping packet because of ports")
      return
    else:
      log.info("Output port found, installing flow rules")
      msg = of.ofp_flow_mod()
      msg.data = event.ofp
      msg.match = of.ofp_match(dl_src = of.EthAddr(src_mac), dl_dst = of.EthAddr(dst_mac))
      msg.actions.append(of.ofp_action_output(port=output_port))
      event.connection.send(msg)
      
      log.info("Sending message 2")
      msg2 = of.ofp_flow_mod()
      msg2.match = msg.match.flip()
      msg2.actions.append(of.ofp_action_output(port=switch_table.get(src_mac)))
      event.connection.send(msg2)
  else:
    log.info("Port not found, Flooding")
    flood_counter += other_ports
    msg = of.ofp_packet_out()
    msg.data = event.ofp
    msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
    event.connection.send(msg)
    pass

  # TODO: Otherwise, have the sending switch flood the original packet to 
  # every port except for the one the packet came in from originally. No rules
  # should be installed in the switch in this case. Also, don't forget to 
  # update your global counter for the number of flooded messages.


  # For 2.3 part 4
  # output_port = switch_table.get(dst_mac)
  # if output_port is not None:
  #   if packet_input_port == output_port:
  #     # drop packet
  #     return
  #   else :
  #     msg = of.ofp_flow_mod()
  #     msg.data = event.ofp
  #     msg.match = of.ofp_match.from_packet(packet, packet_input_port)
  #     msg.actions.append(of.ofp_action_output(port=output_port))
  #     event.connection.send(msg)

  
  # else: 
  #   flood_counter += other_ports
  #   msg = of.ofp_packet_out()
  #   msg.data = event.ofp
  #   msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
  #   event.connection.send(msg)

def launch ():
  core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
  log.info("Pair-Learning switch running.")