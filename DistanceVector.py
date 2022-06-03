# Distance Vector project for CS 6250: Computer Networks
#
# This defines a DistanceVector (specialization of the Node class)
# that can run the Bellman-Ford algorithm. The TODOs are all related 
# to implementing BF. Students should modify this file as necessary,
# guided by the  comments and the assignment instructions. This
# is the only file that needs to be modified to complete the project.
#
# Student code should NOT access the following members, otherwise they may violate
# the spirit of the project:
#
# topolink (parameter passed to initialization function)
# self.topology (link to the greater topology structure used for message passing)
#
# Copyright 2017 Michael D. Brown
# Based on prior work by Dave Lillethun, Sean Donovan, Jeffrey Randow, new VM fixes by Jared Scott and James Lohse.

from Node import *
from helpers import *


class DistanceVector(Node):
    
    def __init__(self, name, topolink, outgoing_links, incoming_links):
        """ Constructor. This is run once when the DistanceVector object is
        created at the beginning of the simulation. Initializing data structure(s)
        specific to a DV node is done here."""
        super(DistanceVector, self).__init__(name, topolink, outgoing_links, incoming_links)
        self.vector = {name:0}
        self.messages = []
        self.verbose = False

    def send_initial_messages(self):
        """ This is run once at the beginning of the simulation, after all
        DistanceVector objects are created and their links to each other are
        established, but before any of the rest of the simulation begins. You
        can have nodes send out their initial DV advertisements here. 

        Remember that links points to a list of Neighbor data structure.  Access
        the elements with .name or .weight """
        # Each node needs to build a message and send it to each of its neighbors
        # HINT: Take a look at the skeleton methods provided for you in Node.py
        for incoming_link in self.incoming_links:
            self.send_msg({self.name:{self.name:0}},incoming_link.name)


    def process_BF(self):
        """ This is run continuously (repeatedly) during the simulation. DV
        messages from other nodes are received here, processed, and any new DV
        messages that need to be sent to other nodes as a result are sent. """
        # Implement the Bellman-Ford algorithm here.  It must accomplish two tasks below:
        # Process queued messages
        old_vector = str(self.vector)
        if self.verbose:
            print("The message of "+ str(self.name) + " are: "+str(self.messages))
        for msg in self.messages:
            msg_origin = list(msg.keys())[0] # the sender of the message
            msg_info = msg.get(msg_origin) # the content of msg from a sender
            msg_nodes = list(msg_info.keys()) # the information of the nodes a msg includes
            weight = self.get_outgoing_neighbor_weight(msg_origin)
            # test weather new node being added to the message
            for msg_node in msg_nodes:
                distance = msg_info.get(msg_node)
                if msg_node == self.name:
                    self.vector[msg_node] = 0
                elif distance == -99:
                    self.vector[msg_node] = -99
                elif msg_node in list(self.vector.keys()):
                    new_dis = min(self.vector.get(msg_node), int(distance) + int(weight))
                    self.vector[msg_node] = new_dis
                else:
                    self.vector[msg_node] = int(distance) + int(weight)

        if self.verbose:
            print("The old vector of "+ str(self.name) + " is " + str(old_vector) +
                  "\nThe new vector of " + str(self.name) + " is: " + str(self.vector))
        # Empty queue
        self.messages = []

        #  Send neighbors updated distances
        if self.verbose:
            print("Iterating....")
        if (old_vector == str(self.vector)):
            if self.verbose:
                print("no update message from " + self.name)
            pass
        else:
            for incoming_link in self.incoming_links:
                if min(self.vector.values()) <= -99:
                    for k ,v in self.vector.items():
                        if v <= -99:
                            # print("BREAKKKKKK"+str(self.vector))
                            self.vector[k] = -99
                            self.send_msg({self.name: self.vector}, incoming_link.name)
                else:
                    self.send_msg({self.name:self.vector},incoming_link.name)
                if self.verbose:
                    print(str(self.name) + " send " + str(self.vector) + " to " + str(incoming_link.name))




    def log_distances(self):
        """ This function is called immedately after process_BF each round.  It 
        prints distances to the console and the log file in the following format (no whitespace either end):
        
        A:A0,B1,C2
        
        Where:
        A is the node currently doing the logging (self),
        B and C are neighbors, with vector weights 1 and 2 respectively
        NOTE: A0 shows that the distance to self is 0 """
        # Use the provided helper function add_entry() to accomplish this task (see helpers.py).

        s=''
        for key,value in sorted(self.vector.items()):
            s = s + str(key) + str(value) + ','
        add_entry(self.name,s[:-1])

