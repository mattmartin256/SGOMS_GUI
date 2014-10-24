'''
Version 1.3 
October 17, 2014

@author: Matt Martin (https://github.com/mattmartin256)

This is a GUI to be used for SGOMS modeling.
SGOMS objects such as Planning Units, Unit Tasks, Methods, and Operators are represented as connected nodes.
These objects can be converted to Python ACT-R readable code via the GUI 
(ACT-R syntax must be input by the user for the ACT-R file to run, or dummy code can be used if you don't care about running ACT-R).
This GUI may be developed to support other general features of ACT-R modeling, such as buffers, agents, and environment objects
Full documentation for the code can be found at: https://github.com/CarletonCognitiveModelingLab/SGOMS_GUI

A description of SGOMS theory can be found at:  
West, R. L., & Somner, S. (2011) Scaling up from Micro Cognition to Macro Cognition: Using SGOMS to build
    Macro Cognitive Models of Sociotechnical Work in ACTR. The proceedings of Cognitive Science

This project was funded in part by a grant from Natural Sciences and Engineering Research Council of Canada,
under the supervision of Dr. R. L. West, at Carleton University, Ottawa.

New for Verson 1.3 (compared to 1.0):

Edit node function (version 1.1)
File --> Save As / Load function (version 1.2)
Larger Firing Condition and Behaviour slots (version 1.3)

Future code:
File --> Save function (no need to select each time)
Copy/Paste node
'''

'''
Notes to self:
I could very easily write a copy/paste function for my code, where I store a node (relation) for copying somewhere,
and then pasting it somewhere else.

It's also kind of a hassel to do save as every time, I could just save the directory in some variable
in the frame or something, and just reference that each time I save. Save as would change the directory in the variable
'''

## Import Statements
from javax.swing import JFrame
from javax.swing import JPanel
from javax.swing import JButton
from javax.swing import JRadioButton
from javax.swing import ButtonGroup
from javax.swing import JLabel
from javax.swing import JTextField
from javax.swing import BorderFactory
from javax.swing import JMenu
from javax.swing import JMenuBar
from javax.swing import JMenuItem
from javax.swing import JPopupMenu
from javax.swing import JDialog
from javax.swing import JOptionPane
from javax.swing import JFileChooser
from javax.swing.filechooser import FileNameExtensionFilter
from javax.swing import SwingUtilities

from java.awt import Point
from java.awt import Color
#from java.awt import Dimension
from java.awt import FlowLayout
#from java.awt import GridLayout
from java.awt import GridBagLayout
from java.awt import GridBagConstraints
from javax.swing import BoxLayout

from java.awt.event import KeyEvent
from java.awt.event import KeyListener
from java.awt.event import MouseListener
from java.awt.event import MouseMotionListener

#import os
import java.io as io
import org.python.util as util

########
## The SGOMS-Related model stuff
########

class PlanningUnit(io.Serializable):
    '''An SGOMS Planning Unit that contains a set of firing conditions, behaviours, and a list of Unit Tasks'''

    def __init__(self, theID="PlanningUnit", theFiringConditions=None, theBehaviour=None, theUnitTaskList=None):
        '''Creates a PlanningUnit

        theID should be a string that identifies the Planning Unit
        theFiringConditions should be a list of strings representing the conditions under which the PlanningUnit
            should fire (can be ACT-R syntax involving buffers, or can be dummy code)
        theBehaviour should be a list of strings representing the behaviour of the PU 
            (can be in terms of ACT-R buffers, environment, etc., or dummy code)
        theUnitTaskList should be a list of UnitTasks that belong to the PlanningUnit
        '''

        self.ID = theID
                    
        self.firingConditions = theFiringConditions
        if theFiringConditions == None:
            self.firingConditions = []  ## By default the firingConditions is an empty list, 
                                        ## to be populated by strings later, representing relevant context buffer info
                                        ## that is required to fire the planning unit production (or dummy code, whatever)      
        self.behaviour = theBehaviour
        if theBehaviour == None:
            self.behaviour = []         ## By default the behaviour is an empty list, 
                                        ## to be populated by strings later, representing relevant production behaviour
                                        
        self.unitTaskList = theUnitTaskList
        if theUnitTaskList == None:
            self.unitTaskList = []      ## Keep track of a list of the unit tasks contained by the Planning Unit

        print "(PlanningUnit.__init__) Planning Unit Created: ", self.ID
        self.printPlanningUnitContents()
        
    def __str__(self):
        '''Returns a string representation of the Planning Unit
        
        Usage: print planningUnit1 --> "PU: ID of planningUnit1"'''
        
        return "PU: " + self.ID

    def addUnitTask(self, theUnitTask):
        '''Adds theUnitTask to the Planning Unit

        theUnitTask should be a UnitTask'''

        self.unitTaskList.append(theUnitTask)

        print "(PlanningUnit.addUnitTask); Unit Task ", theUnitTask.ID, " was added to Planning Unit ", self.ID  
        
    def printPlanningUnitContents(self):
        '''Prints the Planning Unit's ID, firing conditions, behaviours, and the IDs of all the Unit Tasks it contains'''

        self.printFiringConditions()
        self.printBehaviours()
        
        print "(printPlanningUnitContents) ", self.ID, " has ", len(self.unitTaskList), " Unit Tasks:"

        if len(self.unitTaskList) > 0:
            for item in self.unitTaskList:
                print item.ID

        else:
            print self.ID, " has no unit tasks"
            
    def printFiringConditions(self):
        '''Print the firing conditions of the planning unit'''
        
        if len(self.firingConditions) > 0:
            for firingCondition in self.firingConditions:
                print "(PlanningUnit.printFiringConditions)", self.ID, " firing condition: ", str(firingCondition)
        else:
            print "(PlanningUnit.printFiringConditions)", self.ID, " has no firing condition"
            
    def printBehaviours(self):
        '''Print the behaviours of the planning unit'''
        
        if len(self.behaviour) > 0:
            for behaviour in self.behaviour:
                print "(PlanningUnit.printBehaviours)", self.ID, " behaviour: ", str(behaviour)
                
        else:
            print "(PlanningUnit.printBehaviours)", self.ID, " has no behaviour"
    
class UnitTask(io.Serializable):
    '''An SGOMS Unit Task that contains a set of firing conditions, behaviours, and a list of Methods'''
    
    def __init__(self, theID="Unit Task", theFiringConditions=None, theBehaviour=None, theMethodList = None):
        '''Creates a Unit Task

        ID is a string that names the Unit Task
        theFiringConditions should be a list of strings that represent the firing conditions of a production in ACT-R (or dummy code)
        theBehaviour should be a list of strings that represent the behaviour of a production in ACT-R (or dummy code)
        theMethodList should be a list of Methods that the UnitTask contains'''

        self.ID = theID
            
        self.firingConditions = theFiringConditions
        if theFiringConditions == None:
            self.firingConditions = []    
            
        self.behaviour = theBehaviour
        if theBehaviour == None:
            self.behaviour = []
            
        if theMethodList == None:
            self.methodList = []
        else:
            self.methodList = theMethodList

        print "(UnitTask.__init__) Unit Task Created: ", self.ID,
        
    def __str__(self):
        '''Returns a string representation of the Unit Task
        
        Usage: print unitTask1 --> "UT: ID of unitTask1"'''
        
        return "UT: " + str(self.ID)
    
    def addMethod(self, theMethod):
        '''Adds theMethod to theMethodList,
        
        theMethod should be a Method'''

        self.methodList.append(theMethod)

        print "(UnitTask.addMethod); Method ", theMethod.ID, " was added to Unit Task", self.ID
    
    def printUnitTaskContents(self):
        '''Prints the unit task's ID, firing conditions, behaviour, and Method list'''
        
        print "(UnitTask.printUnitTaskContents) ", self.ID
        self.printFiringConditions()
        self.printBehaviours()
        self.printMethodList()
    
    def printMethodList(self):
        '''Prints the ID of each method in the method list'''
        
        if len(self.methodList) > 0:
            print "(UnitTask.printMethodList)", self.ID, "has", str(len(self.methodList)), "methods:"
            for method in self.methodList:
                print method.ID
        else:
            print "(UnitTask.printMethodList()) ", self.ID, " has no methods"
            
    def printFiringConditions(self):
        '''Prints the firing conditions of the UnitTask'''
        
        if len(self.firingConditions) > 0:
            for firingCondition in self.firingConditions:
                print "(UnitTask.printFiringConditions)", self.ID, " firing condition: ", str(firingCondition)
        else:
            print "(UnitTask.printFiringConditions)", self.ID, " has no firing condition"
            
    def printBehaviours(self):
        '''Print the behaviours of the UnitTask'''
        
        if len(self.behaviour) > 0:
            for behaviour in self.behaviour:
                print "(UnitTask.printBehaviours)", self.ID, " behaviour: ", str(behaviour)
        else:
            print "(UnitTask.printBehaviours)", self.ID, " has no behaviour"
            
class Method(io.Serializable):
    '''An SGOMS Method that contains a set of firing conditions, behaviours, and a list of Operators'''
    
    def __init__(self, theID="Method", theFiringConditions=None, theBehaviour=None, theOperatorList = None):
        '''Initializes an SGOMS Method
        
        theID should be a string which identifies the Method
        theFiringConditions should be a list of strings that represent the firing conditions of a production in ACT-R (or dummy code)
        theBehaviour should be a list of strings that represent the behaviour of a production in ACT-R (or dummy code)
        theOperatorList should be a list of Operators that belong to the Method
        '''
        
        self.ID = theID
                    
        self.firingConditions = theFiringConditions
        if theFiringConditions == None:
            self.firingConditions = []    
            
        self.behaviour = theBehaviour
        if theBehaviour == None:
            self.behaviour = []
            
        self.operatorList = theOperatorList
        if theOperatorList == None:
            self.operatorList = []   

        print "(Method.__init__) Method Created: ", self.ID
        
    def __str__(self):
        '''Returns the string representation of the Method
        
        Usage: print method1 --> "Method: ID of method"
        '''
        
        return "Method: " + str(self.ID)
    
    def addOperator(self, theOperator):
        '''Adds theOperator to theOperatorList,
        
        theOperator should be an Operator'''

        self.operatorList.append(theOperator)

        print "(Method.addOperator); Operator ", theOperator.ID, " was added to Method ", self.ID
    
    def printMethodContents(self):
        '''Prints the contents of the method, including its ID, operators, firing conditions, and behaviour'''
        
        print "(Method.printMethodContents)", self.ID
        self.printFiringConditions()
        self.printBehaviours()
        self.printOperators()
        
    def printOperators(self):
        '''Print the ID of each operator this Method contains'''
        
        print "(Method.printOperators), operators of ", self.ID, ":"
        
        if len(self.operatorList) > 0:
            for operator in self.operatorList:
                print operator.ID
        else:
            print "(Method.printOperators) ", self.ID, " has no operators"
                 
    def printFiringConditions(self):
        '''Print the firing conditions of the Method'''
        
        if len(self.firingConditions) > 0:
            for firingCondition in self.firingConditions:
                print "(Method.printFiringConditions)", self.ID, " firing condition: ", str(firingCondition)
        else:
            print "(Method.printFiringConditions)", self.ID, " has no firing condition"
            
    def printBehaviours(self):
        '''Print the behviour of the Method'''
        
        if len(self.behaviour) > 0:
            for behaviour in self.behaviour:
                print "(Method.printBehaviours)", self.ID, " behaviour: ", str(behaviour)
        else:
            print "(Method.printBehaviours)", self.ID, " has no behaviour"

class Operator(io.Serializable):
    '''An SGOMS Operator that contains a set of firing conditions and behaviours'''
    
    def __init__(self, theID="Operator", theFiringConditions=None, theBehaviour=None):
        '''Initializes an SGOMS Operator
        
        theID should be a string which identifies the Operator
        theFiringConditions should be a list of strings that represent the firing conditions of a production in ACT-R (or dummy code)
        theBehaviour should be a list of strings that represent the behaviour of a production in ACT-R (or dummy code)
        '''
        
        self.ID = theID 
            
        self.firingConditions = theFiringConditions
        if theFiringConditions == None:
            self.firingConditions = []    
            
        self.behaviour = theBehaviour
        if theBehaviour == None:
            self.behaviour = []

        print "(Operator.__init__) Operator Created: ", self.ID
        
    def __str__(self):
        '''Returns a string representation of the Operator
        
        Usage: print operator1 --> "Operator: ID of operator1"
        '''
        
        return "Operator: " + str(self.ID)
    
    def printOperatorContents(self):
        '''Prints the contents of the Operator, including its ID, firing conditions, and behaviours'''
        
        print "(Operator.printOperatorContents)", self.ID
        self.printFiringConditions()
        self.printBehaviours()
        
    def printFiringConditions(self):
        '''Print the firing conditions of the Operator'''
        
        if len(self.firingConditions) > 0:
            for firingCondition in self.firingConditions:
                print "(Operator.printFiringConditions)", self.ID, " firing condition: ", str(firingCondition)
        else:
            print "(Operator.printFiringConditions)", self.ID, " has no firing conditions"
            
    def printBehaviours(self):
        '''Print the behviours of the Operator'''
        
        if len(self.behaviour) > 0:
            for behaviour in self.behaviour:
                print "(Operator.printBehaviours)", self.ID, " behaviour: ", str(behaviour)
        else:
            print "(Operator.printBehaviours)", self.ID, " has no behaviour"

class PUxUTRelation(io.Serializable):
    '''Represents the relationship between a PlanningUnit and a UnitTask, 
    including the location of the UnitTask within the PlanningUnit
    
    Used by UTNodes; each UTNode points to a unique PUxUTRelation
    Multiple different PUxUTRelations can point to the same UnitTask, but have different PlanningUnits, locations.
    Can be used to reuse functionality of the UnitTask in different contexts
    
    PUxUTRelations also represent the DM chunk for each UnitTask in ACT-R; 
    each PUxUTRelation has an associated DM_string which is output to ACT-R code
    '''

    def __init__(self, theID=0, thePlanningUnit=None, theUnitTask=None, theLocation=0):
        '''Initializes the relationship between thePlanningUnit and theUnitTask

        theID should be a unique integer (or possibly string), each relation's ID must be unique
        thePlanningUnit should be a single PlanningUnit that contains theUnitTask in its unitTasklist
            (Or can be None by default, representing an unconnected Unit Task)
        theUnitTask should be a single UnitTask
        theLocation represents the location/order of the Unit Task within the Planning Unit
            (Location = 0 means unconnected, or the first UT in a PU'''

        self.ID = theID 
        self.planningUnit = thePlanningUnit
        self.unitTask = theUnitTask
        self.location = theLocation ## The location of the unit task within the planning unit/tree
        
        ## The tupple ID is a more complicated representation of the relation; mostly used for test purposes
        if self.planningUnit == None:
            self.tuppleID = "PUxUTRelation", self.ID, None, self.unitTask.ID, self.location
        else:
            self.tuppleID = "PUxUTRelation", self.ID, self.planningUnit.ID, self.unitTask.ID, self.location

        print "(PUxUTRelation.init) Created: ", self.tuppleID
        
        #######################
        ## ACT-R related stuff
        #######################
        ## Each Planning Unit in SGOMS is represented by a series of chunks in DM that contains info about:
        ## The Planning Unit the Unit Task belongs to, the associated Unit Task, the cue to fire the Unit Task
        ## and the 'cuelag'- the cue of the previous Unit Task (following the Rooster's model)
        ## the cuelag is the previous cue ('none' if no previous cue)
        ## the cue is the previous unit_task ('start' if no previous unit_task). E.g.
        ## DM.add ('planning_unit:prep_wrap    cuelag:none          cue:start          unit_task:veggies')
        ## DM.add ('planning_unit:prep_wrap    cuelag:start         cue:veggies        unit_task:finished')
        ##
        ## The PUxUTRelations will each have a string representation of the DM chunk to be outputed to ACT-R
        #######################
        
        ## Maintain some variables to populate the DM string
        ## We are assuming that relations are unconnected at startup
        
        if self.planningUnit != None:
            self.planning_unit_DM = self.planningUnit.ID
        else:
            self.planning_unit_DM = ''     ## This will not work in ACT-R, it is equivalent to None 
        
        self.cuelag_DM = 'none'
        self.cue_DM = 'start'
        
        if self.unitTask != None:
            self.unit_task_DM = self.unitTask.ID
        else:
            self.unit_task_DM = ''
            
        self.DM_string = 'planning_unit:' + self.planning_unit_DM + ' cuelag:' + self.cuelag_DM \
                        + ' cue:' + self.cue_DM + ' unit_task:' + self.unit_task_DM 
    
    def __str__(self):
        '''Returns a string representation of the PUxUTRelation (i.e. its tupple ID converted to a string)'''
        
        return str(self.tuppleID[0]) + str(self.tuppleID[1]) + str(self.tuppleID[2]) + str(self.tuppleID[3]) + str(self.tuppleID[4])
    
    def updateTuppleID(self):
        '''Updates the tuppleID, based on any changes made to the PUxUTRelation'''
        
        if self.planningUnit == None:
            self.tuppleID = "PUxUTRelation", self.ID, None, self.unitTask.ID, self.location
        else:
            self.tuppleID = "PUxUTRelation", self.ID, self.planningUnit.ID, self.unitTask.ID, self.location
            
        print "(PUxUTRelation.updateTuppleID) new ID:", self.tuppleID
        
    def updateDM_string(self):
        '''Updates the DM_string, based on any changes made to the planning_unit_DM etc.'''
        
        self.DM_string = 'planning_unit:' + self.planning_unit_DM + ' cuelag:' + self.cuelag_DM \
                        + ' cue:' + self.cue_DM + ' unit_task:' + self.unit_task_DM
                        
        print "(PUxUTRelation.updateDM_string) new DM_string:", self.DM_string

class UTxMRelation(io.Serializable):
    '''Represents the relationship between a UnitTask and a Method
    
    Similar in concept to the PUxUTRelation; see above
    Used by MNodes; each MNode points to a unique UTxMRelation
    UTxMRelaitons do not keep track of a DM_string, since there is no role for it in SGOMS theory'''

    def __init__(self, theID=0, theUnitTask=None, theMethod=None, theLocation=0):
        '''Initializes the relationship between thePlanningUnit and theUnitTask

        theID should be a unique integer (or possibly string); each relation's ID must be unique
        theUnitTask should be a single UnitTask that contains theMethod in its methodList
            (Or can be None by default, representing an unconnected Method)
        theMethod should be a single Method with theUnitTask as its parent
        theLocation represents the location/order of the Method within the Unit Task'''

        self.ID = theID 
        self.unitTask = theUnitTask
        self.method = theMethod
        self.location = theLocation ## The location of the unit task within the planning unit/tree
        if self.unitTask == None:
            self.tuppleID = "UTxMRelation", self.ID, None, self.method.ID, self.location
        else:
            self.tuppleID = "UTxMRelation", self.ID, self.unitTask.ID, self.method.ID, self.location

        print "(UTxMRelation.init) Created: ", self.tuppleID
        
    def __str__(self):
        '''Returns a string representation of the UTxMRelation (i.e. its tupple ID converted to a string)'''
        
        return str(self.tuppleID[0]) + str(self.tuppleID[1]) + str(self.tuppleID[2]) + str(self.tuppleID[3]) + str(self.tuppleID[4])
    
    def updateTuppleID(self):
        '''Updates the tuppleID, based on any changes made to the UTxMRelation'''
        
        if self.unitTask == None:
            self.tuppleID = "UTxMRelation", self.ID, None, self.method.ID, self.location
        else:
            self.tuppleID = "UTxMRelation", self.ID, self.unitTask.ID, self.method.ID, self.location
            
        print "(UTxMRelation.updateTuppleID) new ID:", self.tuppleID
        
class MxORelation(io.Serializable):
    '''Represents the relationship between a Method and Operator
    
    Similar in concept to the PUxUTRelation and the UTxMRelation; see above
    Used by ONodes; each ONode points to a unique MxORelation
    MxORelaitons do not keep track of a DM_string, since there is no role for it in SGOMS theory'''
    
    def __init__(self, theID=0, theMethod=None, theOperator=None, theLocation=0):
        '''Initializes the relationship between thePlanningUnit and theUnitTask

        theID should be a unique integer (or possibly string); each relation's ID must be unique
        theMethod should be a single Method that contains theOperator in its operatorList
        (Or can be None by default, representing an unconnected Operator)
        theOperator should be a single Operator with theMethod as its parent
        theLocation represents the location/order of the Operator within the Method'''

        self.ID = theID 
        self.method = theMethod
        self.operator = theOperator
        self.location = theLocation     ## The location of the operator within the method
        if self.method == None:
            self.tuppleID = "MxORelation", self.ID, None, self.operator.ID, self.location
        else:
            self.tuppleID = "MxORelation", self.ID, self.method.ID, self.operator.ID, self.location

        print "(MxORelation.init) Created: ", self.tuppleID
        
    def __str__(self):
        '''Returns a string representation of the MxORelation (i.e. its tupple ID converted to a string)'''
        
        return str(self.tuppleID[0]) + str(self.tuppleID[1]) + str(self.tuppleID[2]) + str(self.tuppleID[3]) + str(self.tuppleID[4])
    
    def updateTuppleID(self):
        '''Updates the tuppleID, based on any changes made to the MxORelation'''
        
        if self.method == None:
            self.tuppleID = "MxORelation", self.ID, None, self.operator.ID, self.location
        else:
            self.tuppleID = "MxORelation", self.ID, self.method.ID, self.operator.ID, self.location
            
        print "(MxORelation.updateTuppleID) new ID:", self.tuppleID
    
        
##### The Model #####
        
class SGOMS_Model(io.Serializable):
    '''The underlying model that the GUI interacts with
    
    Essentially serves as the middle man between the GUI and the ACT-R output function
    PlanningUnits, UnitTasks, Methods, Operators, and their relations are all stored here
    Most of the functions related to SGOMS theory take place here,
        as does converting the SGOMS units to ACT-R code (via the outputToACTR() method)'''

    def __init__(self, thePlanningUnitList=None, theUnitTaskList=None, theMethodList=None, theOperatorList=None,
                 thePUxUTRelationList=None, theUTxMRelationList=None, theMxORelationList=None, theBufferList=None):
        '''The initializing method for the model

        planningUnitList should be a list of Planning Units
        unitTaskList should be a list of Unit Tasks
        theMethodList should be a list of Methods
        theOperatorList should be a list of Operators
        thePUxUTRelationList should be a list of PUxUTRelations
        theUTxMRelationList should be a list of UTxMRelations
        theMxORelationList should be a list of MxORelations
        theBufferList should be a list of strings representing the buffers the ACT-R file should contain
            (a list of default buffers is provided in the __init__ method)
        '''

        print "SGOMS_Model initiated"

        self.planningUnitList = thePlanningUnitList
        if thePlanningUnitList == None:
            self.planningUnitList = []

        self.unitTaskList = theUnitTaskList
        if theUnitTaskList == None:
            self.unitTaskList = []
            
        self.methodList = theMethodList
        if theMethodList == None:
            self.methodList = []
            
        self.operatorList = theOperatorList
        if theOperatorList == None:
            self.operatorList = []

        self.pUxUTRelationList = thePUxUTRelationList
        if thePUxUTRelationList == None:   
            self.pUxUTRelationList = []
            
        self.uTxMRelationList = theUTxMRelationList
        if theUTxMRelationList == None:
            self.uTxMRelationList = []
            
        self.mxORelationList = theMxORelationList
        if theMxORelationList == None:
            self.mxORelationList = []
            
        if theBufferList == None:
            self.bufferList = []
            
        ## The default buffers that every SGOMS_Model must have
        ## These represent buffers that will be used in the ACT-R representation of the model
        ## Right now buffers are strings, but they could probably be objects in future versions of code
        ## In the future, users should probably be able to create/select buffers to use from the GUI
        self.bufferList.append("buffer_context")
        self.bufferList.append("buffer_DM")
        self.bufferList.append("buffer_planning_unit")
        self.bufferList.append("buffer_unit_task")
        self.bufferList.append("buffer_method")
        self.bufferList.append("buffer_operator")

        
        ## A counter to keep track of the number of relations in the model (i.e, PUxUTRelations, UTxMRelations, and MxORelations
        ## Is used to set a unique ID of each relation
        self.relationCounter = 0
        
        ## The initial behaviour for ACT-R must be set somewhere
        ## This will be a list of strings
        self.initialBehaviour = []
        
    def __str__(self):
        '''Prints a string representation of the SGOMS_Model'''
        
        return "SGOMS_Model with " + str(len(self.planningUnitList)) + " Planning Units, " + \
            str(len(self.unitTaskList)) + " Unit Tasks, " + str(len(self.methodList)) + "Methods, and " + \
            str(len(self.operatorList)) + " Operators"

    def addPlanningUnit(self, thePlanningUnit):
        '''Adds thePlanningUnit to the planningUnitList

        thePlanningUnit should be a PlanningUnit'''

        self.planningUnitList.append(thePlanningUnit)

        print "(Model.addPlanningUnit): ", thePlanningUnit.ID, " added. Total number of Planning Units in the model = ", \
        len(self.planningUnitList)

    def addUnitTask(self, theUnitTask):
        '''Adds theUnitTask to self.unitTaskList,
        
        theUnitTask should be a UnitTask
        '''

        self.unitTaskList.append(theUnitTask)
        
        print "(Model.addUnitTask): ", theUnitTask.ID, " added. Total number of Unit Tasks in the model = ", len(self.unitTaskList)
        
    def addMethod(self, theMethod):
        '''Adds theMethod to self.methodList,
        
        theMethod should be a Method
        '''

        self.methodList.append(theMethod)
        
        print "(SGOMS_Model.addMethod): ", theMethod.ID, " added. Total number of Methods in the model = ", len(self.methodList)
        
    def addOperator(self, theOperator):
        '''Adds theOperator to self.operatorList,
        
        theOperator should be an Operator
        '''

        self.operatorList.append(theOperator)
        
        print "(SGOMS_Model.addOperator): ", theOperator.ID, " added. Total number of Operators in the model = ", len(self.operatorList)
        
    def addUnitTaskToPlanningUnit(self, theUnitTask, thePlanningUnit):
        '''Legacy code, not used in v1.0
        Adds theUnitTask to thePlanningUnit's list of unit tasks, not preventing duplicates
        
        theUnitTask should be a UnitTask
        thePlanningUnit should be a PlanningUnit'''
        
        thePlanningUnit.unitTasks.append(theUnitTask)
                    
        print "(SGOMS_Model.addUnitTaskToPlanningUnit) ", theUnitTask.ID, " added to", thePlanningUnit.ID

    def addPUxUTRelationReturnSelf(self, theUnitTask, thePlanningUnit=None,  theLocation=0):
        '''Creates a relationship between thePlanningUnit and theUnitTask at the location given,
        and adds it to the list of PUxUTRelations. 
        Returns the newly created relation

        theUnitTask should be a UnitTask
        thePlanningUnit should be a PlanningUnit (but can be None by default, indicating a non-connected UnitTask)
        theLocation should be an Integer, representing the order of the UT within the PU'''

        ## self.relationCounter assigns a unique ID to each relation (the first parameter of a Relation)
        r = PUxUTRelation(self.relationCounter, thePlanningUnit, theUnitTask, theLocation)

        self.pUxUTRelationList.append(r)
        self.relationCounter += 1   

        print "(Model.addPUxUTRelationReturnSelf) Adding to list : ", r.tuppleID
        
        return r
    
    def addUTxMRelationReturnSelf(self, theMethod, theUnitTask=None, theLocation=0):
        '''Creates a relationship between theUnitTask and theMethod at the location given,
        and adds it to the list of UTxMRelations. 
        Returns the newly created relation

        theMethod should be a Method
        theUnitTask should be a UnitTask (but can be None by default, indicating an unconnected Method)
        theLocation should be an Integer, representing the order of the Method within the UnitTask'''

        ## self.relationCounter assigns a unique ID to each relation (the first parameter of a Relation)
        r = UTxMRelation(self.relationCounter, theUnitTask, theMethod, theLocation)

        self.uTxMRelationList.append(r)
        self.relationCounter += 1   

        print "(Model.addUTxMRelationReturnSelf) Adding to list : ", r.tuppleID
        
        return r
    
    def addMxORelationReturnSelf(self, theOperator, theMethod=None, theLocation=0):
        '''Creates a relationship between theMethod and theOperator at the location given,
        and adds it to the list of MxORelations.
        Returns the newly created relation 

        theOperator should be an Operator
        theMethod should be a Method (but can be None by default, indicating an unconnected Operator)
        theLocation should be an Integer, representing the order of the Operator within the Method'''

        ## self.relationCounter assigns a unique ID to each relation (the first parameter of a Relation)
        r = MxORelation(self.relationCounter, theMethod, theOperator, theLocation)

        self.mxORelationList.append(r)
        self.relationCounter += 1   

        print "(Model.addMxORelationReturnSelf) Adding to list : ", r.tuppleID
        
        return r 
        
    def getPrecedingRelations(self, theRelation):
        '''Returns a list of PUxUTRelations that have a location of theRelation-1
        
        theRelation should be a PUxUTRelation contained in self.pUxUTRelationList
        This method is used to update the DM_string of a PUxUTRelation after two UTNodes have been connected'''
               
        returnList = []
        
        ## If they belong to the same planning unit, and item.location is theRelation-1, add to returnList
        for item in self.pUxUTRelationList:
            if item.planningUnit == theRelation.planningUnit and item.planningUnit !=None:
                if item.location == theRelation.location-1:
                    returnList.append(item)
        
        print "(SGOMS_Model.getPrecedingRelations)", theRelation.ID, "found ", len(returnList), "preceding relations"
        return returnList
        
    def printModelContentsBasic(self):
        '''Print the IDs of all Planning Units, Unit Tasks, Methods, and Operators in the Model
        Used early on for testing purposes, should use printModelContentsAdvanced'''

        print "xxxxx SGOMS_Model printModelContentsBasic xxxxx"

        ## Planning Units
        print "(printModelContentsBasic), Planning Units:"
        if len(self.planningUnitList) > 0:
            print "There are ", len(self.planningUnitList), " Planning Units in the Model:"
            for item in self.planningUnitList:
                print item.ID
        else:
            print "There are no Planning Units in the Model"

        ## Unit Tasks
        print "(printModelContentsBasic), Unit Tasks:"
        if len(self.unitTaskList) > 0:
            print "There are ", len(self.unitTaskList), " Unit Tasks in the Model:"
            for item in self.unitTaskList:
                print item.ID
        else:
            print "There are no Unit Tasks in the Model"
            
        ## Methods
        print "(printModelContentsBasic), Methods:"
        if len(self.methodList) > 0:
            print "There are ", len(self.methodList), " Methods in the Model:"
            for item in self.methodList:
                print item.ID
        else:
            print "There are no Methods in the Model"
        
        ## Operators
        print "(printModelContentsBasic), Operators:"
        if len(self.operatorList) > 0:
            print "There are ", len(self.operatorList), " Operators in the Model:"
            for item in self.operatorList:
                print item.ID
        else:
            print "There are no Operators in the Model"

        print "xxxxx End of (printModelContentsBasic) xxxxx"

    def printModelContentsAdvanced(self):
        '''Prints the entire contents of the model,
        including each Planning Unit and its contents,
        each Unit Task its contents
        each Method and its contents
        each Operator and its contents
        as well as each relation in the model'''

        print "==== (printModelContentsAdvanced) ===="
        print "Planning Units:"
        if len(self.planningUnitList) > 0:
            print "There are ", len(self.planningUnitList), " Planning Units in the Model:"
            for item in self.planningUnitList:
                item.printPlanningUnitContents()
        else:
            print "There are no Planning Units in the Model"

        print "Unit Tasks:"
        if len(self.unitTaskList) > 0:
            print "There are ", len(self.unitTaskList), " Unit Tasks in the Model:"
            for item in self.unitTaskList:
                item.printUnitTaskContents()
        else:
            print "There are no Unit Tasks in the model"
            
        print "Methods:"
        if len(self.methodList) > 0:
            print "There are ", len(self.methodList), " Methods in the Model:"
            for item in self.methodList:
                item.printMethodContents()
        else:
            print "There are no Methods in the model"
            
        print "Operators:"
        if len(self.operatorList) > 0:
            print "There are ", len(self.operatorList), " Operators in the Model:"
            for item in self.operatorList:
                item.printOperatorContents()
        else:
            print "There are no Operators in the model"

        print "(printModelContents), PUxUTRelations:"
        if len(self.pUxUTRelationList) > 0:
            print "There are ", len(self.pUxUTRelationList), " PUxUTRelationships in the Model:"
            for item in self.pUxUTRelationList:
                print item.tuppleID
                print item.DM_string
        else:
            print "There are no PUxUTRelationships in the Model"
            
        print "UTxMRelations:"
        if len(self.uTxMRelationList) > 0:
            print "There are ", len(self.uTxMRelationList), " UTxMRelations in the Model:"
            for item in self.uTxMRelationList:
                print item.tuppleID
        else:
            print "There are no UTxMRelations in the Model"

        print "MxORelations:"
        if len(self.mxORelationList) > 0:
            print "There are ", len(self.mxORelationList), " MxORelations in the Model:"
            for item in self.mxORelationList:
                print item.tuppleID
        else:
            print "There are no MxORelations in the Model"

        print "==== End of (printModelContentsAdvanced) ===="
        
    def updateRelation(self, theRelation):
        '''Legacy code; used for testing purposes.
        The updating of relations in v.1.0 takes place in the UTNode, MNode and ONode classes
        
        Takes a relation and updates its planning_unit_DM, cuelag, cue, unit task, and DM string
        based on its preceding relation in self.pUxUTRelationList
        
        theRelation should be a PUxUTRelation that is contained within self.pUxUTRelationList'''
        
        print "(SGOMS_Model.updateRelation), update: ", theRelation.ID
        
        precedingRelations = self.getPrecedingRelations(theRelation)   ## Returns a list of preceding relations
        
        ## Set the planning_unit_DM string, regardless if there are preceding relations
        if theRelation.planningUnit != None:
            theRelation.planning_unit_DM = theRelation.planningUnit.ID
        
        ## Set the unit_task_DM string, regardless if there are preceding relations
        if theRelation.unitTask != None:
            theRelation.unit_task_DM = theRelation.unitTask.ID
        
        ## Set the cue to be 'start' if theRelation's location is 0, and the culag to be 'none'
        if theRelation.location == 0:
            print "(SGOMS_Model.updateRelation) self.location == 0"
            ## Set the cuelag to 'none'
            theRelation.cuelag = 'none'
            ## Set the cue ('start' if location = 0)
            theRelation.cue_DM = 'start'
        
        if len(precedingRelations) > 0: ## If there are preceding relations...
            print "(SGOMS_Model.updateRelation) self.location is not 0, setting cue etc."
            #FDO print "(SGOMS_Model.updateRelation) preceding relation = ", precedingRelations[0]
            #FDO print "(SGOMS_Model.updateRelation) preceding relations's cue_DM = ", precedingRelations[0].cue_DM 
            theRelation.cuelag_DM = precedingRelations[0].cue_DM ## Pick an arbitrary node for now
            #FDO print "(UTNode.updateRelation) self.cuelag=", self.pUxUTRelation.cuelag_DM
            theRelation.cue_DM = precedingRelations[0].unitTask.ID
            
        theRelation.updateTuppleID()
        theRelation.updateDM_string()
        

    ########## Write to ACT-R ##########

    def outputToACTR(self, theFileName):
        '''Takes what is in the model and outputs it into Python ACT-R readable code
        
        theFileName should be a string that designates the directory to which the file is saved'''

        #directory = os.getcwd()
        #print "(SGOMS_Model.outputToACTR) Directory = " + directory

        f = open(theFileName, "w")  ## Open a new file for writing
        #f = open("TestWriting.py", "w")  
        
        print "(SGOMS_Model.outputToACTR) filename = ", theFileName

        ## Write the basic import statements
        #f.write("import sys\n")
        #f.write("sys.path.insert(0, 'C:/CCMSuite/CCMSuite/')\n")
        
        ## The ACT-R file must have access to ccm (the Python ACT-R library) in order to run
        ## Either must save ACT-R file to the same directory as ccm, or write import statement at top of ACT-R file.
        ## To download CCMsuite visit: https://sites.google.com/site/pythonactr/set-up/ccmsuite-download
        ## or https://github.com/CarletonCognitiveModelingLab/ccmsuite
        
        f.write("import ccm\n")     
        f.write("log=ccm.log()\n")
        f.write("from ccm.lib.actr import *\n\n")

        ## Write the environment statements
        f.write("## The Environment\n")
        f.write("class MyEnvironment(ccm.Model):\n")
        f.write("   pass    ## Environment is empty\n\n")

        ## Write the Agent
        f.write("class MyAgent(ACTR):\n")
        for buffer in self.bufferList:
            f.write("    " + buffer + "=Buffer()\n")    ## For each buffer in self.bufferList, write the appropriate ACT-R code

        f.write("    DM=Memory(buffer_DM)\n\n")     ## The DM is hard-coded for now, note that "buffer_DM" must be a buffer
                                                    ## instantiated above (i.e. is in the bufferList) or else the ACT-R code won't run
        ## Write the init method, adding chunks to DM
        f.write("    def init():\n")
        for relation in self.pUxUTRelationList:
            f.write("        DM.add('" + relation.DM_string + "')\n")
            
        ## ^Each PUxUTRelation has a string representation of the unit task, planning unit, and firing conditions
        ## of the unit task (represented by cue and cuelag). 
        ## This is input into declarative memory in ACT-R, and is how unit tasks/planning units are represented in ACT-R
        ## (in addition to planning unit and unit task productions)
        
        ## In order for the production system to work correctly, the final unit_task slot value must equal 'finished'
        ## e.g. 'planning_unit:prep_wrap    cuelag:spreads    cue:sauce    unit_task:finished'
        ## This 'finished' unit task may have no behaviour, but must be represented in the DM_string
        ## by having a PUxUTRelation with a 'finished' unit task exist at the end of the planning unit.
        ## This is so the lastUnitTask production at the end of the ACT-R file can fire
        
        ## Write the initial behaviour of the model
        
        f.write("\n\n##Initial Model Behaviours\n")
        
        
        ## For syntax reasons, there should be a pass at the end of each function that has no other behaviour (otherwise error)
        if len(self.initialBehaviour) < 1:
            f.write("        pass    ## No initial model behaviours\n")
        else:
            for behaviour in self.initialBehaviour:
                f.write("        " + behaviour + "\n")
        
        ## Write the Planning Unit Productions
        f.write("    \n## Planning Units\n")
        for planningUnit in self.planningUnitList:
            f.write("\n    def " + planningUnit.ID + "(")
            for firingCondition in planningUnit.firingConditions:
                f.write(firingCondition + ",\n")
            f.write("):\n")
            
            if len(planningUnit.behaviour) < 1:
                f.write("        pass    ## No behaviour specified for this Planning Unit\n")
            else:
                for behaviour in planningUnit.behaviour:
                    f.write("        " + behaviour + "\n")
            
        ## Write the Unit Task Productions
        f.write("    \n## Unit Tasks\n")
        for unitTask in self.unitTaskList:
            f.write("\n    def " + unitTask.ID + "(")
            for firingCondition in unitTask.firingConditions:
                f.write(firingCondition + ",\n") 
            f.write("):\n")
            
            if len(unitTask.behaviour) < 1:
                f.write("        pass    ## No behaviour specified for this Unit Task\n")
            else:
                for behaviour in unitTask.behaviour:
                    f.write("        " + behaviour + "\n")
                
                    
        ## Write the Method Productions
        f.write("    \n## Methods\n")
        for method in self.methodList:
            f.write("\n    def " + method.ID + "(")
            for firingCondition in method.firingConditions:
                f.write(firingCondition + ",\n")
            f.write("):\n")
            
            if len(method.behaviour) < 1:
                f.write("        pass    ## No behaviour specified for this Method\n")
            else:
                for behaviour in method.behaviour:
                    f.write("        " + behaviour + "\n")
            
        ## Write the Operator Productions
        f.write("    \n## Operators \n")
        for operator in self.operatorList:
            f.write("\n    def " + operator.ID + "(")
            for firingCondition in operator.firingConditions:
                f.write(firingCondition + ",\n")
            f.write("):\n")
            
            if len(operator.behaviour) < 1:
                f.write("        pass    ## No behaviour specified for this Operator\n")
            else:
                for behaviour in operator.behaviour:
                    f.write("        " + behaviour + "\n")
            
        ## Write the general productions that handle choosing unit tasks
        
        f.write("\n## Global productions for retrieving Unit Tasks from DM\n\n")
        
        ## Request Next Unit Task
        f.write("    def request_next_unit_task(b_plan_unit='planning_unit:?planning_unit " \
                + "cuelag:?cuelag cue:?cue unit_task:?unit_task state:running', " \
                + "b_unit_task='unit_task:?unit_task state:finished'):\n")
        f.write("        DM.request('planning_unit:?planning_unit cue:?unit_task unit_task:? cuelag:?cue')\n")
        f.write("        b_plan_unit.set('planning_unit:?planning_unit cuelag:?cuelag " \
                + "cue:?cue unit_task:?unit_task state:retrieve')\n\n")
        
        ## Retrive Next Unit Task
        f.write("    def retrieve_next_unit_task(b_plan_unit='state:retrieve', " \
                                + "b_DM='planning_unit:?planning_unit cuelag:?cuelag cue:?cue!finished unit_task:?unit_task'):\n")
        f.write("        b_plan_unit.set('planning_unit:?planning_unit cuelag:?cuelag " \
                + "cue:?cue unit_task:?unit_task state:running')\n")
        f.write("        b_unit_task.set('unit_task:?unit_task state:start')\n\n")
        
        ## Last Unit Task
        f.write("    def last_unit_task(b_unit_task='unit_task:finished state:start', " \
                       + "b_plan_unit='planning_unit:?planning_unit'):\n")
        f.write("        b_unit_task.set('stop')\n\n")
        
        ########### Not sure what to do about setting the context at end of PU, how to make general?
        #f.write("        b_context.set('customer:new order:wrap status:prepped done:?planning_unit')\n\n")


        ## Write the code to run the model

        f.write("## Code to run the model\n")
        f.write("tim = MyAgent()\n")
        f.write("env = MyEnvironment()\n")
        f.write("env.agent = tim\n")
        f.write("ccm.log_everything(env)\n\n")

        f.write("env.run()\n")
        f.write("ccm.finished()\n")
        
        f.close()
        
        print "(SGOMS_Model.outputToACTR) ACT-R file export completed"

#######
# The GUI model classes (i.e. the GUI back-end related stuff)
#######

class Node(io.Serializable):
    '''Defines the default inheritable behaviour of a model node. 
    Nodes by themselves are not used in the GUI (although they could be); only their subclasses are
    The entire GUI consists basically of nodes and edges'''
    
    RADIUS = 15     ## Nodes are by default circles, and their radius is set here
    
    def __init__(self, aLabel = "Node", aLocation = None, theIncidentEdges = None):
        '''Initializes the Node with an empty point and label, if none provided
        
        aLabel should be a string 
        aLocation should be a Point
        theIncidentEdges should be a list of Edges'''   
        
        self.label = aLabel
        
        if aLocation == None:
            self.location = Point(0,0)
        else:
            self.location = aLocation
            
        if theIncidentEdges == None:    ## The list of edges that the node is connected to
            self.incidentEdges = []
        else:
            self.incidentEdges = theIncidentEdges
        
        self.nodeType = "Node"  ## A shortcut flag for determining the type of node, 
                                ## ^used in getClosestNodeType("Node"), and getHopsToNodeType("Node")
        self.rootNode = False   ## By default, a node is not the root. 
                                ## ^The root flag was used early on for testing purposes, now 
                                ## getClosestNodeType("Node"), and getHopsToNodeType("Node") are used instead of getHopsToRootNode()
        self.selected = False   ## Indicates whether the node is selected or not
        self.recursed = False   ## A flag for using recursive functions such as getRootNode()
        
        ## Specifies the default order within the hierarchy (distance from the root)
        ## Order is essentially the number of hops from some specified node (e.g. the root node, or a PUNode)
        orderVar = self.getHopsToRootNode()  ## Returns none if no root node
        if orderVar == None:    ## If can't find a root node, it's order is by default zero
            self.order = 0
        else:
            self.order = orderVar   
        
    
    def __str__(self):
        '''Returns a string representing the Node as label (x,y)'''
        
        return self.label + " (" + str(self.location.x) + "," + str(self.location.y) + ")"
    
    def toggleSelected(self):
        '''Changes the selected boolean to True/False depending on previous state'''
        
        self.selected = not self.selected
                    
        print "(Node.toggleSelected) ", self.label, " selected = ", self.selected
            
    def addIncidentEdge(self, theIncidentEdge):
        '''Adds theIncidentEdge to the list of incidentEdges'''
        
        self.incidentEdges.append(theIncidentEdge)
        
    def returnNeighbourNodes(self):
        '''Returns a list of nodes that the current node is connected to'''
        returnList = []
        
        for edge in self.incidentEdges:
            returnList.append(edge.otherEndFrom(self))
            
        return returnList
    
    def returnUnvisitedNeighbourNodes(self):
        '''Returns each neighbour node where recursed == False
        Used in recursive functions such as getHopsToRootNode()
        the recursed flag prevents previously found nodes from being found again infinitely'''
        
        returnList = []
        
        for edge in self.incidentEdges:
            if edge.otherEndFrom(self).recursed == False:
                returnList.append(edge.otherEndFrom(self))
        
        return returnList
    
    def update(self):
        '''Updates the Node
        
        calls self.updateOrder()'''
        
        print "(Node.update) updating: ", self.label
        self.updateOrder()
        
    def updateEverythingButOrder(self):
        '''Updates everything except the order (order must be updated separately)
        
        This method does nothing for Nodes, but is modified in inherited subclasses
        '''
        
        print "(Node:", self.label, ".updateEverythingButOrder)"
    
    def updateOrder(self):
        '''Updates self.order based on the distance to root node'''
        
        print "(Node.updateOrder) updating:", self.label
        orderVar = self.getHopsToRootNode() ## Will return None if can't find root node
        if orderVar == None:    ## If can't find a root node, distance is zero
            self.order = 0
        else:
            self.order = orderVar
    
    def getRootNode(self):
        '''Returns the root node of the hierarchy. 
        Returns None if there is no root node'''
        
        if self.rootNode == True:   ## If self is the root node, return self
            print "(Node.getRootNode) ", self.label, " (self is the root node)"
            return self
        
        nodes = self.getEveryConnectedNode()
        
        ## If there are no connected nodes, return none
        if len(nodes) < 1:
            print "(Node.getRootNode) There are no nodes connected to ", self.label 
            return None
        
        ## If there is a root node connected to the current node, return it
        for item in nodes:
            if item.rootNode == True:
                print "(Node.getRootNode) ", item.label, " is the root node"
                return item
        
        ## If the search did not find any root nodes, return none
        print "(Node.getRootNode) there are no root nodes connected to ", self.label
        return None  
    
    def getHopsToRootNode(self):
        '''Returns the number of hops away from the root node the current node is (as an int)
        Calls getHopsToRootNodeHelper
        
        Note: the 'root' node is any connected node where self.rootNode = True.
        This flag can be set to true for any node object, but is true by default for PUNodes 
        This method was used prior to getHopsToNodeType("NodeType), which is the preferred method of doing things as of version 1.0
        This method is now basically obsolete, but can be used for testing purposes
        
        Returns 0 if self is the root
        Returns None if self is not the root, and self is not connected to anything
        Returns None if self is connected to other nodes, but none are the root (returns value from helper)
        Returns an int if self is connected to a root, int is how many hops away self is from the root
        
        E.g. nodes a(root) --> b --> c
        c.getHopsToRootNode() --> returns 2'''
                       
        nodeList = self.returnUnvisitedNeighbourNodes()  ## The initial list of related nodes to send to helper
        
        everyConnectedNode = [] ## The list to keep track of each node the method finds
                                ## used for resetting the recursed flags to false at the end of the function
                
        ## Return zero if the self is the root
        if self.rootNode == True:
            print "(Node.getHopsToRootNode) ", self.label, " is the root node"
            return 0
        
        ## Return None if there are no neighbour nodes (i.e. throw an exception)
        if len(nodeList) < 1:
            print "(Node.getHopsToRootNode) ", self.label, " is not connected to anything"
            return None
        
        self.recursed = True    ## Prevent the recursive function from finding itself; 
                                ## This flag is checked in the returnUnvisitedNeighbourNodes() method
        
        ## This is the recursive call to the helper method, stores the return value in returnVar
        returnVar = self.getHopsToRootNodeHelper(nodeList, everyConnectedNode)
        
        print "(Node.getHopsToRootNode) hops to root node from", self.label, "=", returnVar
        self.recursed = False   ## Reset the recursed flag to False at the end
        return returnVar
        
    def getHopsToRootNodeHelper(self, theNodeList, everyConnectedNode, times=0):
        '''Helper method for getHopsToRootNode
        Returns the number of hops away from the root node the current node is
        Returns None if it exhausts the nodes connected to self, and finds no root
        
        theNodeList is basically a list of connected nodes to recurse over in order to find more nodes
        it is populated by the function returnUnvisitedNeighbourNodes()
        nodes that have been found by this function have their recursed flag set to true, to avoid recursing infinitely
        
        everyConnectedNode keeps track of every node found by the search,
        so that every node's 'recursed' flag can be reset at the end of the function
        
        times keeps track of the recursive level, and by proxy the distance from the initial node the function is'''

        ## Set every node in theNodeList's recursed flag to True, 
        ## in order to prevent nodes from finding previous nodes, and recursing infinitely
        for item in theNodeList:
            item.recursed = True
            ## Keep track of every node found by the function so that their flags can be reset at the end
            if item not in everyConnectedNode:
                everyConnectedNode.append(item)
                    
        ## Print the recursive level 
        #FDO print "---------- Level", times+1, "----------"
       
        ## This is the check for end state, if it has gone 20 times, the function ends and returns None
        ## This function is for testing purposes only, it should not be tripped under normal circumstances
        ## This is basically like throwing an exception, it stops an infinite loop if something goes wrong
        if times > 19:
            ## Reset each recursed flag back to False before returning
            for thing in everyConnectedNode:
                    thing.recursed = False
            print ("(Node.getHopsToRootNodeHelper) Recursed 20 times, returning None")
            return None
        
        ## Another check for the end state, if it has found the root node, return the # of hops
        ## (each item in theNodeList is one hop away from the previous node, so hops = times +1)
        for item in theNodeList:
            if item.rootNode == True:   ## If it has found a root
                ## Reset each recursed flag back to False before returning
                for thing in everyConnectedNode:
                    thing.recursed = False
                print "(Node.getHopsToRootNodeHelper)", self.label, "is ", times + 1, " hops from the root node"
                return times+1      ## Return # of hops
        
        ## Now we get into the 'guts' of the function
        passList = []  ## A variable for storing the list to be passed on to the next function call
        
        for item in theNodeList:
            ## For every item in theNodeList keep a list of related nodes
            ## tempList is a list of Nodes related to the item in question, each item will have a tempList
            tempList = []   ## This is not going to contain anything that has already been activated, 
                            ## as they are excluded in the returnUnvisitedNeighbourNodes method
            tempList += item.returnUnvisitedNeighbourNodes()
            
            #FDO print "Length of tempList on times", times, len(tempList)
                       
            for thing in tempList:
                #FDO print item.label, " is connected to ", thing.label
                thing.recursed = True   ## Keep track of which nodes have been found already
                passList.append(thing)  ## Everything that returnUnvisited has found gets put into passList
                
        ## This is the check for the end state, if there are no unvisited nodes left,
        ## and it has not found a root node, return None (throw an exception)
        if len(passList) < 1:
            print "(Node.getHopsToRootNodeHelper) passList is empty, returning None"
            ## Reset the recursed flags
            for item in everyConnectedNode:
                #print item.label
                item.recursed = False
                #if item not in returnList:
                #    returnList.append(item)
                #    print "appending happened ok"
            #FDO print "helper returnlist", str(returnList)
            return None
        
        #FDO print "hi"        
        return self.getHopsToRootNodeHelper(passList, everyConnectedNode, times+1)     
    
    def getClosestNodeType(self, theNodeType):
        '''Returns the closest node of the same type as theNodeType,
        Returns None if it can't find a node of the same type as theNodeType
        Used for setting the parent SGOMS unit for the current node (e.g. the parent PU of a UT)
        
        Returns self if self is the closest node of the same type as theNodeType
        Returns None if self is not connected to anything
        Returns None if self is connected to other nodes, but none are the same type as theNodeType
        Returns an int if self is connected to a root, int is how many hops away self is from the root
        
        Usage: uTNode.getClosestNodeType("PUNode") --> returns the nearest connected node of type PUNode
        
        theNodeType should be a string == "PUNode", "UTNode", "MNode", or "ONode"
        '''
        nodeList = self.returnUnvisitedNeighbourNodes()  ## The initial list of related nodes to send to helper
        
        everyConnectedNode = [] ## The list to keep track of each connected node
        
        ## Check to see if the supplied node is the same type as self, if so return self
        ## (Like returning self if self is the root node)
        
        if self.nodeType == theNodeType:
            print "(Node.getClosestNodeType) self is of the same type (", theNodeType, \
            ")as the supplied node, returning self:", self.label
            return self  
        
        ## Return None if there are no neighbour nodes (i.e. throw an exception)
        if len(nodeList) < 1:
            print "(Node.getClosestNodeType) ", self.label, " is not connected to anything, returning None"
            return None
        
        self.recursed = True  ## Prevent the recursive function from finding itself
        
        ## This is the recursive call to the helper method, stores the return value in returnVar
        returnVar = self.getClosestNodeTypeHelper(nodeList, everyConnectedNode, theNodeType)
        
        print "(Node.getClosestNodeType) closest node to ", self.label, " of specified type =", returnVar
        self.recursed = False   ## Reset the recursed flag to False at the end
        return returnVar
    
    def getClosestNodeTypeHelper(self, theNodeList, everyConnectedNode, theNodeType, times=0):
        '''Helper method for getClosestNodeType
        Returns the closest node of the type specified
        Returns None if it exhausts the nodes connected to self, and finds no node of the type specified
        
        theNodeList is basically a list of connected nodes to recurse over in order to find more nodes
        it is populated by the function returnUnvisitedNeighbourNodes()
        nodes that have been found by this function have their recursed flag set to true, to avoid recursing infinitely
        
        everyConnectedNode keeps track of every node found by the search,
        so that every node's 'recursed' flag can be reset at the end of the function
        
        theNodeType is the original string supplied to getClosestNodeType, it is used to do the end-state checking,
        and it is not modified in any way.
        theNodeType should be a string == "PUNode", "UTNode", "MNode", or "ONode"
        
        times keeps track of the recursive level, and by proxy the distance from the initial node the function is'''
        
        ## Set every node in theNodeList's recursed flag to True, 
        ## in order to prevent nodes from finding previous nodes, and recursing infinitely
        for item in theNodeList:
            item.recursed = True
            ## Keep track of every node found by the function so that their flags can be reset at the end
            if item not in everyConnectedNode:
                everyConnectedNode.append(item)
                    
        ## Print the recursive level 
        #FDO print "---------- Level", times+1, "----------"
       
        ## This is a check for an end state, if it has gone 20 times, the function ends and returns None
        ## This function is for testing purposes only, it should not be tripped under normal circumstances
        ## This is basically like throwing an exception, it stops an infinite loop if something goes wrong
        if times > 19:
            ## Reset each recursed flag back to False before returning
            for thing in everyConnectedNode:
                    thing.recursed = False
            print ("(Node.getClosestNodeTypeHelper) Recursed 20 times, returning None")
            return None
        
        ## Check for the end state: if it has found a node of the same type as theNodeType, return the node
        for item in theNodeList:
            
            if item.nodeType == theNodeType:
                ## Reset each recursed flag back to False before returning
                for thing in everyConnectedNode:
                    thing.recursed = False
                print "(Node.getClosestNodeTypeHelper)", item.label, "is the closest ", theNodeType, " to ", self.label
                return item      ## Return the node it found
                    
        ## Now we get into the 'guts' of the function
        passList = []  ## A variable for storing the list to be passed on to the next function call
        
        for item in theNodeList:
            ## For every item in theNodeList keep a list of related nodes
            ## tempList is a list of Nodes related to the item in question, each item will have a tempList
            tempList = []   ## This is not going to contain anything that has already been found, 
                            ## as they are excluded in the returnUnvisitedNeighbourNodes method
            tempList += item.returnUnvisitedNeighbourNodes()
            
            #FDO print "Length of tempList on times", times, len(tempList)
                       
            for thing in tempList:
                #FDO print item.label, " is connected to ", thing.label
                thing.recursed = True   ## Keep track of which nodes have been found already
                passList.append(thing)  ## Everything that returnUnvisited has found gets put into passList
                
        ## This is the check for the end state, if there are no unvisited nodes left,
        ## and it has not found a node of the same type as theNodeType, return None (throw an exception)
        if len(passList) < 1:
            print "(Node.getClosestNodeTypeHelper)", self.label, " is not connected to nodes of type", theNodeType, ", returning None"
            ## Reset the recursed flags
            for item in everyConnectedNode:
                #FDO print item.label
                item.recursed = False
            #FDO print "helper returnlist", str(returnList)
            return None
               
        return self.getClosestNodeTypeHelper(passList, everyConnectedNode, theNodeType, times+1)
    
    def getHopsToNodeType(self, theNodeType):
        '''Returns the number of hops away from the nearest specified type of node the current node is (returns an int)
        Calls getHopsToNodeTypeHelper()
        
        theNodeType should be a string == "PUNode", "UTNode", "MNode", or "ONode"
                
        Returns 0 if self is of the same type as theNodeType
        Returns None if self is not connected to anything
        Returns None if self is connected to other nodes, but none are of the type specified (returns value from helper)
        Returns an int if self is connected to a node of the type specified, 
        the int is how many hops away self is from the nearest node of the same type as theNodeType
        
        E.g. nodes a(PUNode) --> b --> c
        c.getHopsToNodeType("PUNode") --> returns 2'''
                       
        nodeList = self.returnUnvisitedNeighbourNodes()  ## The initial list of related nodes to send to helper
        
        everyConnectedNode = [] ## The list to keep track of each connected node
        
        ## Check to see if the supplied node is the same type as self, if so return 0
        if self.nodeType == theNodeType:
            print "(Node.getHopsToNodeType) self is of the same type", theNodeType, "as the supplied nodeType, returning 0"
            return 0
                
        ## Return None if there are no neighbour nodes (i.e. throw an exception)
        if len(nodeList) < 1:
            print "(Node.getHopsToNodeType) ", self.label, " is not connected to anything, returning None"
            return None
        
        self.recursed = True  ## Prevent the function from finding itself
        
        ## This is the recursive call to the helper method, stores the return value in returnVar
        returnVar = self.getHopsToNodeTypeHelper(nodeList, everyConnectedNode, theNodeType)
        
        print "(Node.getHopsToNodeType) hops to nearest", theNodeType, " from ", self.label, "=", returnVar
        self.recursed = False   ## Reset the recursed flag to False at the end
        return returnVar
    
    def getHopsToNodeTypeHelper(self, theNodeList, everyConnectedNode, theNodeType, times=0):
        '''Helper method for getHopsToNodeType
        Returns the number of hops away from the closest node of the specified type the current node is
        Returns None if it exhausts the nodes connected to self, and finds no node of the same type as theNodeType
        
        theNodeList is basically a list of connected nodes to recurse over in order to find more nodes
        it is populated by the function returnUnvisitedNeighbourNodes().
        Nodes that have been found by this function have their recursed flag set to true, to avoid recursing infinitely
        
        everyConnectedNode keeps track of every node found by the search,
        so that every node's 'recursed' flag can be reset at the end of the function
        
        theNodeType is the original string supplied to getHopsToNodeType, it is used to do the end-state checking,
        and it is not modified in any way.
        theNodeType should be a string which == "PUNode", "UTNode", "MNode", or "ONode"
        
        times keeps track of the recursive level, and by proxy the distance from the initial node the function is'''
        
        ## Set every node in theNodeList's recursed flag to True, 
        ## in order to prevent nodes from finding previous nodes, and recursing infinitely
        for item in theNodeList:
            item.recursed = True
            ## Keep track of every node found by the function so that their flags can be reset at the end
            if item not in everyConnectedNode:
                everyConnectedNode.append(item)
                    
        ## Print the recursive level 
        #FDO print "---------- Level", times+1, "----------"
       
        ## This is a check for an end state, if it has gone 100 times, the function ends and returns None
        ## This function is for testing purposes only, it should not be tripped under normal circumstances
        ## This is basically like throwing an exception, it stops an infinite loop if something goes wrong
        if times > 99:
            ## Reset each recursed flag back to False before returning
            for thing in everyConnectedNode:
                    thing.recursed = False
            print ("!!!!!!(Node.getHopsToNodeTypeHelper) Recursed 100 times, returning None!!!!!!")
            return None
        
        ## If it has found a node of the same type as theNodeType, return the node
        for item in theNodeList:
            
            if item.nodeType == theNodeType:
                ## Reset each recursed flag back to False before returning
                for thing in everyConnectedNode:
                    thing.recursed = False
                print "(Node.getHopsToNodeTypeHelper)", self.label, "is ", times + 1, " hops from the closest", \
                theNodeType, ":", item.label
                return times+1      ## Return # of hops
        
        ## Now we get into the 'guts' of the function
        passList = []  ## A variable for storing the list to be passed on to the next function call
        
        for item in theNodeList:
            ## For every item in theNodeList keep a list of related nodes
            ## tempList is a list of Nodes related to the item in question, each item will have a tempList
            tempList = []   ## This is not going to contain anything that has already been activated, 
                            ## as they are excluded in the returnUnvisitedNeighbourNodes method
            tempList += item.returnUnvisitedNeighbourNodes()
            
            #FDO print "Length of tempList on times", times, len(tempList)
                       
            for thing in tempList:
                #FDO print item.label, " is connected to ", thing.label
                thing.recursed = True   ## Keep track of which nodes have been found already
                passList.append(thing)  ## Everything that returnUnvisited has found gets put into passList
                
        ## This is another check for the end state, if there are no unvisited nodes left,
        ## and it has not found a node of the same type as theNodeType, return None (throw an exception)
        if len(passList) < 1:
            print "(Node.getHopsToNodeTypeHelper)", self.label, " is not connected to any ", theNodeType, " returning None"
            ## Reset the recursed flags
            for item in everyConnectedNode:
                #print item.label
                item.recursed = False
            #FDO print "helper returnlist", str(returnList)
            return None
             
        ## The recursive function call
        return self.getHopsToNodeTypeHelper(passList, everyConnectedNode, theNodeType, times+1)
    
    def getEveryConnectedNode(self):
        '''Returns a list of all nodes that the current node is (indirectly) connected to
        Returns an empty list if there are no connected nodes
        
        Eg. Nodes a --> b --> c
        c.getEveryConnectedNode() --> returns [a, b]'''
       
        self.recursed = True  ## Prevent the function from finding itself
        
        everyConnectedNode = [] ## The list to keep track of each connected node
        
        nodeList = self.returnUnvisitedNeighbourNodes()  ## The initial list of related nodes to send to helper
        
        ## Return empty list if there are no neighbour nodes 
        if len(nodeList) < 1:
            print "(Node.getEveryConnectedNode)", self.label, " is not connected to anything"
            self.recursed = False   ## Reset the recursed variable before returning
            return nodeList
       
        
        ## This is the recursive call, the helper should return a list of every connected node
        returnList = self.getEveryConnectedNodeHelper(nodeList, everyConnectedNode)
                
        print "(Node.getEveryConnectedNode)", self.label, "is connected to ", str(returnList)
        self.recursed = False   ## Reset the recursed variable before returning
        
        return returnList

    def getEveryConnectedNodeHelper(self, theNodeList, everyConnectedNode, times=0):
        '''A helper method for the recursive getEveryConnectedNode() method
        
        functions essentially the same as getHopsToRootNodeHelper(), except it returns
        everyConnectedNode, rather than the # of hops
        
        theNodeList is basically a list of connected nodes to recurse over in order to find more nodes
        it is populated by the function returnUnvisitedNeighbourNodes()
        nodes that have been found by this function have their recursed flag set to true, to avoid recursing infinitely
        
        everyConnectedNode keeps track of every node found by the search,
        so that they can be returned at the end of the function, and so that their recursed flags can be reset 
        
        times keeps track of the recursive level, and by proxy the distance from the initial node the function is'''
        
        for item in theNodeList:
            item.recursed = True    ## Prevent the function from finding itself
            if item not in everyConnectedNode:
                everyConnectedNode.append(item)
                
        ## Print the recursive level 
        #FDO print "---------- Level", times+1, "----------"
       
        ## This is the check for end state, if it has gone 20 times, the function ends and returns None
        if times > 19:
            print "(Node.getEveryConnectedNodeHelper) Recursed 20 times, returning None"
            return None
                
        passList = []  ## A variable for storing the list to be passed on to the next function call
        
        for item in theNodeList:
            ## For every item in theNodeList keep a list of related nodes
            ## tempList is a list of Nodes related to the item in question, each item will have a tempList
            tempList = []   ## This is not going to contain anything that has already been found, 
                            ## as they are excluded in the returnUnvisitedNeighbourNodes method
            tempList += item.returnUnvisitedNeighbourNodes()
            
            #FDO print "Length of tempList on times", times, len(tempList)
            
            for thing in tempList:
                #FDO print item.label, " is connected to ", thing.label
                thing.recursed = True   ## Keep track of which nodes have been found already
                passList.append(thing)  ## Everything that returnUnvisited has found gets put into passList
                
        ## This is the check for the end state, if there are no unvisited nodes left,
        ## return the list of every connected node
        if len(passList) < 1:
            #FDO print "(Node.getEveryConnectedNodeHelper) passList is empty, returning everyConnectedNode:"
            for item in everyConnectedNode:
                print item.label
                item.recursed = False   ## Reset the recursed flag back to false for every node found
            
            return everyConnectedNode
                    
        return self.getEveryConnectedNodeHelper(passList, everyConnectedNode, times+1)
    
    def printNode(self):
        '''Prints the node as: label(x,y)'''
        
        print self.label, "(", self.location.x, ",", self.location.y, ")" 
    
    def draw(self, aPen):
        '''Draws the node
        
        aPen should be a Graphics object'''
                        
        #Draw a black border around the circle
        aPen.setColor(Color.black)
        aPen.fillOval(self.location.x - Node.RADIUS, self.location.y - Node.RADIUS, Node.RADIUS * 2,
                      Node.RADIUS * 2)
        
        #Draw a blue-filled circle around the center of the node (if not selected)
        if self.selected == True:
            aPen.setColor(Color.red)
        else:
            aPen.setColor(Color.blue)
        aPen.fillOval(self.location.x - self.RADIUS, self.location.y - self.RADIUS, self.RADIUS * 2,
                      self.RADIUS * 2)
        
        # Draw a label at the top right corner of the node (including its label, and order)
        aPen.setColor(Color.black)
        stringVar = self.label + "," + str(self.order)
        aPen.drawString(stringVar, self.location.x + self.RADIUS, self.location.y - self.RADIUS)
        
class PUNode(Node):
    '''Specifies the behaviour/appearance of a PlanningUnitNode (PUNode)
    
    PUNode inherits from Node
    Each PUNode will point to a unique underlying PlanningUnit'''
    
    HEIGHT = 40
    WIDTH = 50
    
    def __init__(self, aLabel = "PUNode", aLocation = None, theIncidentEdges = None, thePU = None):
        '''Initializes the Node with an empty point and label, if none provided
        
        aLabel should be a string, by default it is the Label of thePU (if one is provided)
        aLocation should be a Point
        theIncidentEdges should be a list of Edges
        thePU should be a PlanningUnit
        
        A blank PU is not created by default, it should be passed in only'''
        
        if aLocation == None:
            self.location = Point(0,0)
        else:
            self.location = aLocation
            
        if theIncidentEdges == None:
            self.incidentEdges = []
        else:
            self.incidentEdges = theIncidentEdges
                
        self.planningUnit = thePU
        
        if aLabel == "PUNode" and self.planningUnit != None:
            self.label = self.planningUnit.ID
        else:
            self.label = aLabel 

        self.selected = False   ## Indicates whether the node is selected or not
        self.rootNode = True    ## Specifies whether the node is the root node (PUs are by default the root)
        self.nodeType = "PUNode"    ## A shortcut flag for determining the type of node, 
                                    ##^ used in getClosestNodeType(), and getHopsToNodeType()
        self.recursed = False
        self.order = 0
        
        print "(PUNode) initiated, ", self 
        
    def __str__(self):
        '''Returns a string representation of the PUNode
        
        looks like: PUNode: label PU: label (x,y)'''
        
        return "PUNode: " + self.label \
                + " (" + str(self.location.x) + "," + str(self.location.y) + ")"
                
    def update(self):
        '''Updates the PUNode, based on any changes to the graph
        Calls updateOrder() and updatePU()'''
        
        print "(", self.label, ".update)"
        
        self.updateOrder()
        self.updatePU()
        
    def updateEverythingButOrder(self):
        '''Updates everything except the order (order must be updated separately)
        
        calls self.updatePU()
        '''
        
        print "(PUNode:", self.label, ".updateEverythingButOrder)"
        self.updatePU()
         
    def updatePU(self):
        '''Updates the PUNode, based on which nodes are connected to it
        Makes sure the label of the PUNode corresponds to the ID of the planningUnit
        Adds the UT of each connected UTNode to the PU's list of UTs
        
        This basically resets the PU contents each time it is called
        based on the nodes the PUNode is connected to
        The function is primarily concerned with connecting UTNodes to PUNodes'''
        
        print "(PUNode: ",self.label,".updatePU)"
        
        ## Update the label of the PUNode
        self.label = self.planningUnit.ID
        
        ## Clear the list and repopulate on each update
        del self.planningUnit.unitTaskList[:]
        
        connectedNodes = self.getEveryConnectedNode()
        
        ## We are not adding anything to SGOMS model here, we are only modifying what already exists
        ## e.g. no UnitTasks or PlanningUnits are being deleted or added to the SGOMS lists
        ## We are also only worried about the PU contents, the relations can worry about themselves elsewhere
        ## The list of unit tasks in the PlanningUnit is 'semi-ordered', i.e. each instance of a UT is
        ## represented in the UnitTaskList, but the order is not important (order is represented by relations)
        for node in connectedNodes:
            ## Check to make sure the connected node in question is a UTNode
            if isinstance(node, UTNode):
                ## Add the UTNode's UT to the PUNode's PU
                self.planningUnit.addUnitTask(node.pUxUTRelation.unitTask)
        
    def draw(self, aPen):
        '''Draws the PUNode
        
        aPen should be a Graphics object'''
                        
        #Draw a black border around the rectangle
        aPen.setColor(Color.black)
        aPen.fillRect(self.location.x - int(PUNode.WIDTH/2), self.location.y - int(PUNode.HEIGHT/2), PUNode.WIDTH,
                      PUNode.HEIGHT)
        
        #Draw a blue-filled rectangle around the center of the node (if not selected)
        if self.selected == True:
            aPen.setColor(Color.red)
        else:
            aPen.setColor(Color.blue)
        aPen.fillRect(self.location.x - int(PUNode.WIDTH/2), self.location.y - int(PUNode.HEIGHT/2), PUNode.WIDTH,
                      PUNode.HEIGHT)
        
        # Draw a label at the top right corner of the node
        aPen.setColor(Color.black)
        aPen.drawString(self.planningUnit.ID, self.location.x + int(PUNode.WIDTH/2), self.location.y - int(PUNode.HEIGHT/2))
        
class UTNode(Node):
    '''Specifies the behaviour/appearance of a UTNode
    
    UTNode inherits from Node
    Each UTNode points directly to a unique underlying PUxUTRelation'''
    
    RADIUS = 20
    
    def __init__(self, aLabel = "UTNode", aLocation = None, theIncidentEdges = None, thePUxUTRelation = None):
        '''Initializes the Node with an empty point and label, if none provided
        
        aLabel should be a string, by default it is the Label of theUT  
        aLocation should be a Point
        theIncidentEdges should be a list of Edges
        thePUxUTRelation should be a PUxUTRelation
        
        A blank PUxUTRelation is not created by default, it should be passed in only'''
        
        self.selected = False  ## Indicates whether the node is selected or not
        self.rootNode = False  ## Indicates whether the node is the root node (false by default for UTNodes)
        self.nodeType = "UTNode"    ## A shortcut flag for determining the type of node, 
                                    ##^ used in getClosestNodeType(), and getHopsToNodeType()
        self.recursed = False  ## A flag for recursive functions to use    
        
        if aLocation == None:
            self.location = Point(0,0)
        else:
            self.location = aLocation
            
        if theIncidentEdges == None:
            self.incidentEdges = []
        else:
            self.incidentEdges = theIncidentEdges
                
        self.label = aLabel
            
        ## Specifies the distance from the root (i.e. distance to connected PlanningUnitNode)
        orderVar = self.getHopsToNodeType("PUNode") ## Returns none if no connected root node
        if orderVar == None:    ## If can't find a root node, order = 0
            self.order = 0
        else:
            self.order = orderVar
        
        ## The UTNode must be fed a PUxUTRelation, else it remains none
        self.pUxUTRelation = thePUxUTRelation
                
        print "(UTNode) initiated, ", self 
    
    def __str__(self):
        '''Returns a string representation of the UTNode'''
        
        return "UTNode: " + self.label \
                + " (" + str(self.location.x) + "," + str(self.location.y) + ")"
    
    def returnRelation(self):
        '''Returns the PUxUTRelation of the node'''
        
        return self.pUxUTRelation
    
    def returnUnitTask(self):
        '''Returns the UnitTask'''
        
        return self.pUxUTRelation.unitTask
    
    def getPrecedingUTNodes(self):
        '''Returns a list of nodes where the node's order is self.order -1
        This is used for setting the cuelag and cue, which relies on the previous node in the PU order
        '''
        
        connectedNodes = self.getEveryConnectedNode()
        returnList = []
        
        for node in connectedNodes:
            if isinstance(node, UTNode):
                if node.order == self.order-1:
                    returnList.append(node)
                    
        #FDO print "(UTNode.getPrecedingUTNodes), returning: "
        #FDO for item in returnList:
        #FDO     print item.label
        return returnList
    
    def update(self):
        '''Updates the Node
        
        calls self.updateOrder()
        calls self.updateUT()
        and self.updateRelation()'''
        
        print "(UTNode:", self.label, ".update)"
        self.updateOrder()
        self.updateUT()
        self.updateRelation()
        
    def updateEverythingButOrder(self):
        '''Updates everything except the order (order must be updated separately)
        
        calls self.updateUT()
        and self.updateRelation()
        '''
        
        print "(UTNode:", self.label, ".updateEverythingButOrder)"
        self.updateUT()
        self.updateRelation()
        
    
    def updateOrder(self):
        '''Updates self.order based on the distance to root node'''
        
        orderVar = self.getHopsToNodeType("PUNode") ## Will return None if can't find root node
        if orderVar == None:    ## If can't find a root node, distance is zero
            self.order = 0
        else:
            self.order = orderVar
            
        print "(UTNode:", self.label, ".updateOrder) Order =", self.order
    
    def updateUT(self):
        '''Updates the UTNode, based on which nodes are connected to it
        Makes sure the label of the UTNode corresponds to the ID of the UnitTask
        Adds the Method of each connected MNode to the UT's list of Methods
        
        This basically resets the UT contents each time it is called
        based on the nodes the UTNode is connected to
        The function is primarily concerned with connecting MNodes to UTNodes'''
        
        print "(UTNode: ",self.label,".updateUT)"
        
        ## Update the label of the UTNode
        self.label = self.pUxUTRelation.unitTask.ID
        
        ## I believe this is the syntax for clearing a list in python
        del self.pUxUTRelation.unitTask.methodList[:]
        
        connectedNodes = self.getEveryConnectedNode()
        
        ## We are not adding anything to SGOMS model here, we are only modifying what already exists
        ## e.g. no UnitTasks or Methods are being deleted or added to the SGOMS lists
        ## We are also only worried about the UT contents, the relations can worry about themselves in updateRelation
        ## The list of Methods in the UnitTask is 'semi-ordered', i.e. each instance of a Method is
        ## represented in the methodList, but the order is not important (order is represented by relations)
        for node in connectedNodes:
            ## Check to make sure the connected node in question is an MNode
            if isinstance(node, MNode):
                ## Add the MNode's method to the UTNode's unitTaskList
                self.pUxUTRelation.unitTask.addMethod(node.uTxMRelation.method)
    
    def updateRelation(self):
        '''Updates self.pUxUTRelation based on the node's distance to the PU root
        
        Sets the relation's PU to be that of the PUNode's, none if there is no PUNode root
        Sets the relation's location to be hops to root node - 1, 0 if there is not PUNode root
        Sets the relation's planning_unit_DM, cuelag_DM, cue_DM, and unit_task_DM, based on the location
        Does not worry about the UT or PU lists in SGOMS
        Updates the relation's tuppleID and DM_string'''
        
        #FDO print "(", self.label, ".updateRelation)"
        
        root = self.getClosestNodeType("PUNode")
        
        ## If the root is a PUNode (i.e. not None), assign the PU to the relation, and the relation's location is order-1
        if isinstance(root, PUNode):
            print "(UTNode.updateRelation) root is a PUNode"
            self.pUxUTRelation.planningUnit = root.planningUnit
            self.pUxUTRelation.location = self.order-1      ## Here we just use the node's order to set the relation's location
                                                        ## order = hops away; location 0 means it is the first in a chain or unconnected    
            ### ACT-R Stuff ###
            ## Set the planning_unit_DM string
            self.pUxUTRelation.planning_unit_DM = root.planningUnit.ID
            
            ## Set the cuelag (previous relation's cue, 'none' if location = 0), 
            ###### This should probably be changed in future versions #######
            if self.pUxUTRelation.location == 0:    ## Location == 0 represents either an unconnected node or the first of a chain
                print "(UTNode.updateRelation) self.location == 0"
                self.pUxUTRelation.cuelag = 'none'
                ## Set the cue ('start' if location = 0)
                self.pUxUTRelation.cue_DM = 'start'
            else:   ## If the location is not 0:
                print "(UTNode.updateRelation) self.location is not 0, setting cuelag etc."
                precedingNodes = self.getPrecedingUTNodes() ## A list of nodes with an order of self.order-1
                #FDO print "(UTNode.updateRelation) preceding node = ", precedingNodes[0]
                #FDO print "(UTNode.updateRelation) preceding node's cue_DM = ", precedingNodes[0].pUxUTRelation.cue_DM 
                
                if len(precedingNodes) > 0:     ## Check to see if there are preceding nodes
                    ## If there are preceding Nodes:
                    ## Make sure the preceding node is updated (we only care about the one arbitrary preceding node)
                    ## ^Order etc. is updated elsewhere
                    precedingNodes[0].updateRelation()  ## This needs to be done to avoid bugs
                    ## Pick an arbitrary preceding node to set the cue and cuelag, don't deal with splitting or looping
                    self.pUxUTRelation.cuelag_DM = precedingNodes[0].pUxUTRelation.cue_DM 
                    #FDO print "(UTNode.updateRelation) self.cuelag=", self.pUxUTRelation.cuelag_DM
                    self.pUxUTRelation.cue_DM = precedingNodes[0].pUxUTRelation.unitTask.ID
                    
                else:
                    print "(UTNode.updateRelation) there are no preceding UT nodes, but ", self.label, \
                    " is connected to a PU:", self.pUxUTRelation.planningUnit.ID
                    ## If there are no preceding nodes (i.e. this node is the first in the series), set the attributes to their defaults
                    self.pUxUTRelation.cuelag_DM = 'none'
                    self.pUxUTRelation.cue_DM = 'start'
        
        else:   ## If there is no PUNode as a root, set the attributes back to their defaults
            print "(UTNode.updateRelation) there is no PUNode Root"
            self.pUxUTRelation.planningUnit = None
            self.pUxUTRelation.location = 0
            
            self.pUxUTRelation.planning_unit_DM = ''
            self.pUxUTRelation.cuelag_DM = 'none'
            self.pUxUTRelation.cue_DM = 'start'
            
        self.pUxUTRelation.unit_task_DM = self.pUxUTRelation.unitTask.ID
        
        self.pUxUTRelation.updateTuppleID()
        self.pUxUTRelation.updateDM_string()
        
        
    def draw(self, aPen):
        '''Draws the UTNode
        
        aPen should be a Graphics object'''
                         
        #Draw a black border around the oval
        aPen.setColor(Color.black)
        aPen.fillOval(self.location.x - UTNode.RADIUS, self.location.y - UTNode.RADIUS, UTNode.RADIUS * 2,
                      UTNode.RADIUS * 2)
        
        #Draw a green-filled oval around the center of the node (if not selected)
        if self.selected == True:
            aPen.setColor(Color.red)
        else:
            aPen.setColor(Color.green)
        
        aPen.fillOval(self.location.x - UTNode.RADIUS, self.location.y - UTNode.RADIUS, UTNode.RADIUS * 2,
                      UTNode.RADIUS * 2)
        
        # Draw a label at the top right corner of the node
        # Label looks like: UT.label, order within PU
        aPen.setColor(Color.black)
        #stringVar = str(self.pUxUTRelation.unitTask.ID) + ", ID:" + str(self.pUxUTRelation.ID) + \
        #", loc:" + str(self.pUxUTRelation.location) 
        aPen.drawString(self.pUxUTRelation.unitTask.ID, self.location.x + self.RADIUS, self.location.y - self.RADIUS)


class MNode(Node):
    '''Specifies the behaviour/appearance of an MNode
    
    MNode inherits from Node
    Each MNode points directly to a unique underlying UTxMRelation'''
    
    RADIUS = 15
    
    def __init__(self, aLabel = "MNode", aLocation = None, theIncidentEdges = None, theUTxMRelation = None):
        '''Initializes the Node with an empty point and label, if none provided
        
        aLabel should be a string 
        aLocation should be a Point
        theIncidentEdges should be a list of Edges
        theUTxMRelation should be a PUxUTRelation
        
        A blank UTxMRelation is not created by default, it should be passed in only'''
        
        self.selected = False  ## Indicates whether the node is selected or not
        self.rootNode = False  ## Indicates whether the node is the root node (false by default for MNodes)
        self.nodeType = "MNode"    ## A shortcut flag for determining the type of node, 
                                    ##^ used in getClosestNodeType(), and getHopsToNodeType()
        self.recursed = False  ## A flag for recursive functions to use    
        
        if aLocation == None:
            self.location = Point(0,0)
        else:
            self.location = aLocation
            
        if theIncidentEdges == None:
            self.incidentEdges = []
        else:
            self.incidentEdges = theIncidentEdges
                
        self.label = aLabel
            
        ## Specifies the distance from the root (i.e. distance to connected UTNode)
        orderVar = self.getHopsToNodeType("UTNode") ## Returns none if not connected to any UTNode
        if orderVar == None:    ## If can't find a connected UTNode, order = 0
            self.order = 0
        else:
            self.order = orderVar
        
        ## The UTxMRelation has to be passed in, it is None by default
        self.uTxMRelation = theUTxMRelation
                
        print "(MNode) initiated, ", self 
    
    def __str__(self):
        '''Returns a string representation of the MNode'''
        
        return "MNode: " + self.label \
                + " (" + str(self.location.x) + "," + str(self.location.y) + ")"
            
    def update(self):
        '''Updates the MNode
        
        calls self.updateOrder()
        calls self.updateMethod()
        and self.updateRelation()'''
        
        print "(MNode:", self.label, ".update)"
        self.updateOrder()
        self.updateMethod()
        self.updateRelation()
        
    def updateEverythingButOrder(self):
        '''Updates everything except the order (order must be updated separately)
        
        calls self.updateMethod()
        and self.updateRelation()
        '''
        
        print "(MNode:", self.label, ".updateEverythingButOrder)"
        self.updateMethod()
        self.updateRelation()
    
    def updateOrder(self):
        '''Updates self.order based on the distance to the closest UTNode'''
        
        orderVar = self.getHopsToNodeType("UTNode") ## Will return None if can't find root node
        if orderVar == None:    ## If can't find a root node, distance is zero
            self.order = 0
        else:
            self.order = orderVar
        print "(MNode.updateOrder)", self.label, " order =", self.order
            
    def updateMethod(self):
        '''Updates the MNode, based on which nodes are connected to it
        Makes sure the label of the MNode corresponds to the ID of the Method
        Adds the Operator of each connected ONode to the Method's list of Operators
        
        This basically resets the Method's contents each time it is called
        The function is primarily concerned with connecting MNodes to ONodes'''
        
        print "(MNode: ",self.label,".updateMethod)"
        
        ## Update the label
        self.label = self.uTxMRelation.method.ID
        
        ## I believe this is the syntax for clearing a list in python
        del self.uTxMRelation.method.operatorList[:]
        
        connectedNodes = self.getEveryConnectedNode()
        
        ## We are not adding anything to SGOMS model here, we are only modifying what already exists
        ## e.g. no UnitTasks or Methods are being deleted or added to the SGOMS lists
        ## We are also only worried about the UT contents, the relations can worry about themselves in updateRelation
        ## The list of Methods in the UnitTask is 'semi-ordered', i.e. each instance of a Method is
        ## represented in the methodList, but the order is not important (order is represented by relations)
        for node in connectedNodes:
            ## Check to make sure the connected node in question is an MNode
            if isinstance(node, ONode):
                ## Add the MNode's method to the UTNode's unitTaskList
                self.uTxMRelation.method.addOperator(node.mxORelation.operator)
            
    def updateRelation(self):
        '''Updates self.uTxMRelation based on the node's distance to the UT root
        
        Sets the relation's UT to be that of the closest connected UTNode, none if there is no connected UTNode
        Sets the relation's location to be hops to closest UTNode - 1, 0 if there is no connected UTNode
        '''
        
        #FDO print "(MNode: ", self.label, ".updateRelation)"
        
        root = self.getClosestNodeType("UTNode")     
        
        ## If the root is a UTNode (i.e. not None), assign the UT to the relation, and the relation's location is order-1
        if isinstance(root, UTNode):
            print "(MNode.updateRelation): ", self.label, " found a connected UTNode:", root.label
            self.uTxMRelation.unitTask = root.pUxUTRelation.unitTask
            self.uTxMRelation.location = self.order-1   ## order = hops away; location 0 means it is the first in a chain or unconnected
            
        self.uTxMRelation.updateTuppleID()
            
    def draw(self, aPen):
        '''Draws the MNode
        
        aPen should be a Graphics object
        '''
                         
        #Draw a black border around the oval
        aPen.setColor(Color.black)
        aPen.fillOval(self.location.x - self.RADIUS, self.location.y - self.RADIUS, self.RADIUS * 2,
                      self.RADIUS * 2)
        
        #Draw a yellow-filled oval around the center of the node (if not selected)
        if self.selected == True:
            aPen.setColor(Color.red)
        else:
            aPen.setColor(Color.yellow)
        
        aPen.fillOval(self.location.x - self.RADIUS, self.location.y - self.RADIUS, self.RADIUS * 2,
                      self.RADIUS * 2)
        
        # Draw a label at the top right corner of the node
        # Label looks like: UT.label, order within PU
        aPen.setColor(Color.black)
        #stringVar = str(self.uTxMRelation.method.ID) + ", ID:" + str(self.uTxMRelation.ID) + \
        #", loc:" + str(self.uTxMRelation.location) 
        aPen.drawString(self.uTxMRelation.method.ID, self.location.x + self.RADIUS, self.location.y - self.RADIUS)
        
class ONode(Node):
    '''Specifies the behaviour/appearance of an ONode
    
    ONode inherits from Node
    Each ONode points directly to a unique underlying MxORelation'''
    
    RADIUS = 12
    
    def __init__(self, aLabel = "ONode", aLocation = None, theIncidentEdges = None, theMxORelation = None):
        '''Initializes the Node with an empty point and label, if none provided
        
        aLabel should be a string 
        aLocation should be a Point
        theIncidentEdges should be a list of Edges
        theMxORelation should be an MxORelation
        
        A blank MxORelation is not created by default, it should be passed in only'''
        
        self.selected = False  ## Indicates whether the node is selected or not
        self.rootNode = False  ## Indicates whether the node is the root node (false by default for ONodes)
        self.nodeType = "ONode"    ## A shortcut flag for determining the type of node, 
                                    ##^ used in getClosestNodeType(), and getHopsToNodeType()
        self.recursed = False  ## A flag for recursive functions to use    
        
        if aLocation == None:
            self.location = Point(0,0)
        else:
            self.location = aLocation
            
        if theIncidentEdges == None:
            self.incidentEdges = []
        else:
            self.incidentEdges = theIncidentEdges
                
        self.label = aLabel
            
        ## Specifies the distance from the root (i.e. distance to a connected MNode)
        orderVar = self.getHopsToNodeType("MNode") ## Returns none if not connected to any MNode
        if orderVar == None:    ## If can't find a connected MNode, order = 0
            self.order = 0
        else:
            self.order = orderVar
        
        ## The MxORelation must be passed in, it is None by default
        self.mxORelation = theMxORelation
                
        print "(MNode) initiated, ", self 
    
    def __str__(self):
        '''Returns a string representation of the ONode'''
        
        return "ONode: " + self.label \
                + " (" + str(self.location.x) + "," + str(self.location.y) + ")"
            
    def update(self):
        '''Updates the ONode
        
        calls self.updateOrder()
        and self.updateRelation()'''
        
        print "(ONode:", self.label, ".update)"
        self.updateOrder()
        self.updateRelation()
        
    def updateEverythingButOrder(self):
        '''Updates everything except the order (order must be updated separately)
        
        calls self.updateRelation()
        '''
        
        print "(ONode:", self.label, ".updateEverythingButOrder)"
        
        self.updateRelation()
    
    def updateOrder(self):
        '''Updates self.order based on the distance to the closest MNode'''
        
        orderVar = self.getHopsToNodeType("MNode") ## Will return None if can't find root node
        if orderVar == None:    ## If can't find a root node, distance is zero
            self.order = 0
        else:
            self.order = orderVar
            
        print "(ONode.updateOrder)", self.label, " order = ", self.order
            
    def updateRelation(self):
        '''Updates self.mxORelation based on the node's distance to the MNode root
        
        Makes sure the label of the ONode corresponds to the ID of the Operator
        Sets the relation's Method to be that of the closest connected MNode, none if there is no connected MNode
        Sets the relation's location to be hops to closest MNode - 1, 0 if there is no connected MNode
        '''
        
        #FDO print "(ONode: ", self.label, ".updateRelation)"
        
        ## Update the label
        self.label = self.mxORelation.operator.ID
        
        root = self.getClosestNodeType("MNode")     
        
        ## If the root is a MNode (i.e. not None), assign the Method to the relation, and the relation's location is order-1
        if isinstance(root, MNode):
            print "(ONode.updateRelation): ", self.label, " found a connected MNode:", root.label
            self.mxORelation.method = root.uTxMRelation.method
            self.mxORelation.location = self.order-1
            
        self.mxORelation.updateTuppleID()
            
    def draw(self, aPen):
        '''Draws the ONode
        
        aPen should be a Graphics object
        '''
                 
        #Draw a black border around the oval
        aPen.setColor(Color.black)
        aPen.fillOval(self.location.x - self.RADIUS, self.location.y - self.RADIUS, self.RADIUS * 2,
                      self.RADIUS * 2)
        
        #Draw a green-filled oval around the center of the node (if not selected)
        if self.selected == True:
            aPen.setColor(Color.red)
        else:
            aPen.setColor(Color.gray)
        
        aPen.fillOval(self.location.x - self.RADIUS, self.location.y - self.RADIUS, self.RADIUS * 2,
                      self.RADIUS * 2)
        
        # Draw a label at the top right corner of the node
        # Label looks like: operator.label, order within parent Method
        aPen.setColor(Color.black)
        #stringVar = str(self.mxORelation.operator.ID) + ", ID:" + str(self.mxORelation.ID) + \
        #", loc:" + str(self.mxORelation.location) 
        aPen.drawString(self.mxORelation.operator.ID, self.location.x + self.RADIUS, self.location.y - self.RADIUS)

class Edge(io.Serializable):
    '''Defines the model edge (i.e. the line that connects two nodes on the graph)'''
    
    def __init__(self, theStartNode, theEndNode, theLabel=None):
        '''Initializes the Edge with a startnode and end node
        
        theStartNode should be a Node
        theEndNode should be a Node'''
        
        self.startNode = theStartNode
        self.endNode = theEndNode
        if theLabel == None:
            self.label = theStartNode.label + " --> " + theEndNode.label 
        else:
            self.label = theLabel
        
        self.selected = False   ## Edges can be selected like nodes; by default they are unselected
        
    def __str__(self):
        '''Returns label, startNode --> endNode'''
        
        return str(self.label) + " " + str(self.startNode.label) + " --> " + str(self.endNode.label)
    
    def toggleSelected(self):
        '''Changes the selected boolean to True/False depending on previous state'''
        
        self.selected = not self.selected
                    
        print "(Edge.toggleSelected) selected = ", self.selected
        
    def otherEndFrom(self, aNode):
        '''If given a node that the edge is connected to, returns the other node
        
        aNode should be a Node that the Edge is connected to'''
        
        if self.startNode == aNode:
            return self.endNode
        else:
            return self.startNode
        
    def returnMidpoint(self):
        '''Returns a point as a midpoint between the startNode and endNode'''
        
        mX = (self.startNode.location.x +
              self.endNode.location.x) / 2
            
        mY = (self.startNode.location.y +
              self.endNode.location.y) / 2
              
        midPoint = Point(mX,mY)
        return midPoint
                
    def draw(self, aPen):
        '''Draws the edge
        
        aPen should be a Graphics object'''
        
        #Draw a line from the center of he startNode to the center of the endNode (red if selected, black otherwise)
        if self.selected == True:
            aPen.setColor(Color.red)
        else:
            aPen.setColor(Color.black)
        aPen.drawLine(self.startNode.location.x, self.startNode.location.y,
                      self.endNode.location.x, self.endNode.location.y)
        aPen.fillOval(self.returnMidpoint().x - 4, self.returnMidpoint().y - 4,     ## Draw an oval at the midpoint for selecting
                      8, 8)
        
    def printEdge(self):
        '''Prints the Edge as sNode(x,y) --> eNode(x,y)'''
        
        print self.startNode.label, "(", self.startNode.location.x, ",", self.startNode.location.y, ")", \
        " --> ", self.endNode.label, "(", self.endNode.location.x, ",", self.endNode.location.y, ")"
       
class Graph(io.Serializable):
    '''Defines a collection of Nodes, Edges, and their behaviour'''
    
    def __init__(self, theLabel = "Graph", theNodes = None, theSGOMS_Model = None):
        '''Initializes the Graph, with a set of nodes and edges, as well as an SGOMS_Model
        
        theLabel should be a string
        theNodes should be a list of Nodes
        theSGOMS_Model should be an SGOMS_Model
        '''
        
        self.label = theLabel 
        
        if theNodes == None:
            self.nodes = []
        else:
            self.nodes = theNodes
        
        if theSGOMS_Model == None:
            self.sGOMS = SGOMS_Model()
        else:
            self.sGOMS = theSGOMS_Model
        
        ## Store a variable to represent whether to create a new PU, UT, Method, or Operator
        ## Valid options: "PLANNING_UNIT", "UNIT_TASK", "METHOD", "OPERATOR"
        self.selectedSGOMSType = None
             
    
    def __str__(self):
        '''Returns the Graph as label, (#of Nodes, #of Edges)'''
        
        return self.label + " (" + str(len(self.nodes)) + " nodes, " + str(len(self.returnEdges())) + " edges)"
    
    def returnEdges(self):
        '''Returns all Edges contained in self.nodes'''
        
        returnList = []
        
        for node in self.nodes:
            for edge in node.incidentEdges:
                if edge not in returnList:
                    returnList.append(edge)
                    
        return returnList
    
    def returnSelectedNodes(self):
        '''Returns a list of all currently selected nodes'''
        
        returnList = []
        
        for node in self.nodes:
            if node.selected == True:
                returnList.append(node)
        return returnList
    
    def returnSelectedEdges(self):
        '''Returns a list of all currently selected edges'''
        
        returnList = []
        
        for e in self.returnEdges():
            if e.selected == True:
                returnList.append(e)
        return returnList
    
    def addNode(self, aNode):
        '''Legacy code; this method is not used in v1.0, should use addNodeAdvanced
        Adds a node to self.nodes
        
        aNode should be a Node
        '''
        
        self.nodes.append(aNode)
        
        self.update()
        
    def addNodeAdvanced(self, aLabel, aPoint):
        '''Creates a new node, with aPoint as its location, and aLabel as its label
        and adds the node to self.nodes'''
        
        node = Node(aLabel, aPoint)
        
        self.nodes.append(node)
        
        self.update()
        
    def addPUNode(self, aPUNode):
        '''Legacy code, this method is not used in v1.0; should use addPUNodeAdvancedNew
        Adds aPUNode to self.nodes
        adds the PUNode's PU to the SGOMS_Model
        
        aPUNode should be a PUNode, with an instantiated planning unit'''
        
        self.nodes.append(aPUNode)
        self.sGOMS.addPlanningUnit(aPUNode.planningUnit)
        
        self.update()
        
        print "(Graph.addPUNode),", aPUNode 
        
    def addPUNodeAdvanced(self, aLabel, aPoint):
        '''Legacy code, this method is not used in v1.0; should use addPUNodeAdvancedNew
        Creates a new PUNode, with aLabel and aPoint as the label and point of the PUNode
        Creates a blank PlanningUnit, which it will feed to the PUNode and add to self.sGOMS
        
        aLabel should be a string
        aPoint should be a Point
        '''

        pU = PlanningUnit(aLabel)
        pUNode = PUNode(pU.ID, aPoint, None, pU)
        
        self.nodes.append(pUNode)
        self.sGOMS.addPlanningUnit(pU)
        
        self.update()
        
        print "(Graph.addPUNodeAdvanced)", pUNode
        
    def addPUNodeAdvancedNew(self, aPlanningUnit, aPoint):
        '''Creates new PUNode, with aPlanningUnit and aPoint as the PlanningUnit and point of the PUNode
        
        The aPlanningUnit will be added to SGOMS_Model, it should be a PlanningUnit
        The PUNode will be added to self.nodes
        aPoint should be a point
        '''
        
        self.sGOMS.addPlanningUnit(aPlanningUnit)   ## Adds the new Planning Unit to the list of PlanningUnits in SGOMS
        
        ## Add the new node
        ## (self, aLabel = "PUNode", aLocation = None, theIncidentEdges = None, thePU = None):
        pUNode = PUNode(aPlanningUnit.ID, aPoint, None, aPlanningUnit)
        
        self.nodes.append(pUNode)
        
        self.update()
        
        print "(Graph.addPUNodeAdvancedNew)", pUNode
        
        
    def addUTNode(self, aUTNode):
        '''Adds aUTNode to self.nodes
        adds aUTNode's relation to the SGOMS_Model
        adds aUTNode's UT to the SGOMS_Model
        
        aUTNode should be a UTNode, with an instantiated relation'''
        
        self.nodes.append(aUTNode)
        self.sGOMS.pUxUTRelationList.append(aUTNode.pUxUTRelation)
        self.sGOMS.addUnitTask(aUTNode.pUxUTRelation.unitTask)
        
        self.update()
        
        print "(Graph.addUTNode)", aUTNode
        
    def addUTNodeAdvanced(self, aLabel, aPoint):
        '''Creates new UTNode, with aLabel and aPoint as the label and point of the UTNode
        Creates a blank UnitTask and PUxUTRelation, the Unit Task will be fed to the PUxUTRelation
        The PUxUTRelation will be fed to the UTNode, and added to SGOMS
        The UTNode will be added to self.nodes
        
        By default, this function creates a unique UT to be fed to the relation and SGOMS Model
        '''
        
        
        unitTask = UnitTask(aLabel)
        relation = self.sGOMS.addPUxUTRelationReturnSelf(unitTask)  ##This returns the new relation and stores it
        
        self.sGOMS.addUnitTask(relation.unitTask)   ## Adds the new UT to the list of Unit Tasks
        
        ## Add the new node
        uTNode = UTNode(aLabel, aPoint, None, relation)
        
        self.nodes.append(uTNode)
        
        self.update()
        
        print "(Graph.addUTNodeAdvanced)", uTNode
    
    def addUTNodeAdvancedNew(self, aUnitTask, aPoint):
        '''Creates new UTNode,
        Creates a new PUxUTRelation and adds it to SGOMS, aUnitTask is fed to the PUxUTRelation
        aUnitTask is added to SGOMS
        The PUxUTRelation is fed to the UTNode, the UTNode is added to self.nodes
        
        aUnitTask should be a UnitTask
        aPoint should be a Point
        '''
        
        ## Add a new PUxUTRelation to the SGOMS_Model
        relation = self.sGOMS.addPUxUTRelationReturnSelf(aUnitTask)  ##This returns the new relation and stores it in the variable
        
        ## Adds the new UT to the list of Unit Tasks
        ## As of v1.0, duplicate Unit Tasks are allowed in SGOMS_Model,
        ## Future versions may wish to exclude duplicates
        self.sGOMS.addUnitTask(relation.unitTask)   
        
        ## Add the new node
        uTNode = UTNode(aUnitTask.ID, aPoint, None, relation)
        
        self.nodes.append(uTNode)
        
        self.update()
        
        print "(Graph.addUTNodeAdvancedNew)", uTNode
        
    def addMNodeAdvancedNew(self, aMethod, aPoint):
        '''Creates new MNode,
        Creates a new UTxMRelation and adds it to SGOMS, aMethod is fed to the UTxMRelation
        aMethod is added to SGOMS
        The newly created UTxMRelation is fed to the MNode
        The MNode is added to self.nodes
        
        aMethod should be a Method
        aPoint should be a Point
        '''
        
        relation = self.sGOMS.addUTxMRelationReturnSelf(aMethod)  ##This returns the new relation and stores it
        
        self.sGOMS.addMethod(relation.method)   ## Adds the new Method to the list of methods
        
        ## Add the new node
        mNode = MNode(aMethod.ID, aPoint, None, relation)
        
        self.nodes.append(mNode)
        
        self.update()
        
        print "(Graph.addMNodeAdvancedNew)", mNode
    
    def addONodeAdvancedNew(self, anOperator, aPoint):
        '''Creates new ONode,
        Creates a new MxORelation and adds it to SGOMS, anOperator is fed to the MxORelation
        anOperator is added to SGOMS
        The newly created MxORelation is fed to the ONode
        The ONode is added to self.nodes
        
        anOperator should be an Operator
        aPoint should be a Point
        '''
        
        relation = self.sGOMS.addMxORelationReturnSelf(anOperator)  ##This returns the new relation and stores it
        
        self.sGOMS.addOperator(relation.operator)   ## Adds the new Operator to the list of operators
        
        ## Add the new node
        oNode = ONode(anOperator.ID, aPoint, None, relation)
        
        self.nodes.append(oNode)
        
        self.update()
        
        print "(Graph.addONodeAdvancedNew)", oNode
    
    def addEdge(self, startNode, endNode):
        '''Adds an edge to the Nodes' incident edges
        
        startNode should be a Node
        endNode should be a Node'''
        
        print "(Graph.addEdge)"
        
        anEdge = Edge(startNode, endNode)
        
        startNode.addIncidentEdge(anEdge)
        endNode.addIncidentEdge(anEdge)
        
        self.update()
        
            
    def deleteEdge(self, theEdge):
        '''Deletes the parameter edge from the nodes that contain it
        
        theEdge should be an Edge'''
        
        theEdge.startNode.incidentEdges.remove(theEdge)
        theEdge.endNode.incidentEdges.remove(theEdge)
        
        self.update()
        
    def deleteNode(self, theNode):
        '''Deletes the parameter node, and all of its incident edges
        
        If theNode is a PUNode, delete the PU from the SGOMS model
        If theNode is a UTNode, delete the relation from the SGOMS model, and the relation's UT
        If theNode is an MNode, delete the relation from the SGOMS model, and the relation's Method
        If theNode is an ONode, delete the relation from the SGOMS model, and the relation's Operator
        
        ^Future versions of code may wish to delete the UT, Method or Operator under only certain conditions,
        such as if there is only one relation that points to the UT 
        (don't want to accidently create null pointers if two relations point to the same UT, and one is deleted)'''
        
        if isinstance(theNode, PUNode):
            #self.deletePUNode()
            self.sGOMS.planningUnitList.remove(theNode.planningUnit)
            
        if isinstance(theNode, UTNode):
            #self.deleteUTNode()
            self.sGOMS.unitTaskList.remove(theNode.pUxUTRelation.unitTask)
            self.sGOMS.pUxUTRelationList.remove(theNode.pUxUTRelation)
            
        if isinstance(theNode, MNode):
            #self.deleteUTNode()
            self.sGOMS.methodList.remove(theNode.uTxMRelation.method)
            self.sGOMS.uTxMRelationList.remove(theNode.uTxMRelation)
            
        if isinstance(theNode, ONode):
            #self.deleteUTNode()
            self.sGOMS.operatorList.remove(theNode.mxORelation.operator)
            self.sGOMS.mxORelationList.remove(theNode.mxORelation)
        
        for edge in theNode.incidentEdges:
            edge.otherEndFrom(theNode).incidentEdges.remove(edge)
        self.nodes.remove(theNode)
        
        self.update()
        
    def nodeAt(self, p):
        '''Return the first node in which point p is contained, if none, return None
        Used primarily as a helper to handle mouseClick events 
        
        p should be a Point'''

        for node in self.nodes:
            #FDO print "(Graph.nodeAt) Node: ", node.label
            c = node.location ##This returns a point
            
            ## Check to see what kind of node it is to determine whether the point is contained by the node
            ## (Different types of nodes have different dimensions)
            if isinstance(node, PUNode):
                ## We are calculating the square of the distance for x and y coordinates to avoid negatives
                dx = (p.x - c.x) * (p.x - c.x)
                dy = (p.y - c.y) * (p.y - c.y)
                ## If the parameter point was within the boundaries of the PUNode, return the PUNode
                if dx <= (int(PUNode.WIDTH/2) * int(PUNode.WIDTH/2)) and \
                    dy <= (int(PUNode.HEIGHT/2) * int(PUNode.HEIGHT/2)):
                    print "(Graph.nodeAt) returning PUNode ", node.label
                    return node
            
            ## Calculate the square of the distance from the node point and the click point
            ## This formula is for circles, so x and y don't matter
            d = (((p.x - c.x) * (p.x - c.x)) + ((p.y - c.y) * (p.y - c.y)))
            
            if isinstance(node, UTNode):
                ## If the parameter point was within the boundaries of the UTNode, return the UTNode                
                if d <= (UTNode.RADIUS * UTNode.RADIUS):
                    print "(Graph.nodeAt) returning UTNode ", node.label
                    return node
                
            if isinstance(node, MNode):
                ## If the parameter point was within the boundaries of the MNode, return the MNode                
                if d <= (MNode.RADIUS * MNode.RADIUS):
                    print "(Graph.nodeAt) returning MNode ", node.label
                    return node
                
            if isinstance(node, ONode):
                ## If the parameter point was within the boundaries of the UTNode, return the UTNode                
                if d <= (ONode.RADIUS * ONode.RADIUS):
                    print "(Graph.nodeAt) returning ONode ", node.label
                    return node

            if isinstance(node, Node):
                ## If the parameter point was within the boundaries of the Node, return the Node
                if d <= (Node.RADIUS * Node.RADIUS):  ##If some point is within the radius of the node:
                    print "(Graph.nodeAt) returning node ", node.label
                    return node
        #FDO print"(Graph.nodeAt) returning None"
        return None
    
    def edgeAt(self, p):
        '''Return the first edge in which point p is near the midpoint; if none, return null
        
        p should be a Point'''
        
        mX = 0
        mY = 0
        
        for e in self.returnEdges():
            #FDO print "(Graph.edgeAt) edges ", e.label
            mX = (e.startNode.location.x +
                  e.endNode.location.x) / 2
            
            mY = (e.startNode.location.y +
                  e.endNode.location.y) / 2
                  
            distance = (p.x - mX) * (p.x - mX) + (p.y - mY) * (p.y - mY)
            
            ## Selecting a node requires clicking close to the midpoint (within a Node Radius)
            if distance <= (Node.RADIUS * Node.RADIUS):     
                print "(Graph.edgeAt) click was near midpoint of edge ", e.label
                return e
            
        #FDO print "(Graph.edgeAt) click was not near midpoint of edge"
        return None
    
    def update(self):
        '''Update method for the graph
        
        calls update() on all nodes'''
        
        print "***** (Graph.update) *****"
        
        for node in self.nodes:
            node.updateOrder()
        
        for node in self.nodes:
            node.updateEverythingButOrder()
            
        self.sGOMS.printModelContentsAdvanced()
        
    def draw(self, aPen):
        '''Draws the graph - i.e. tell all nodes and edges to draw themselves
        
        aPen should be a Graphics object'''
        
        edges = self.returnEdges()
        
        for edge in edges:  #Draw the edges first
            edge.draw(aPen)
            
        for node in self.nodes: #Draw the nodes second
            node.draw(aPen)
            
    def printGraph(self):
        '''Prints the graph, including all of the nodes'''
        
        print "@@@@@ Graph.printGraph @@@@@"
        print self.label, "(", len(self.nodes), ",", len(self.returnEdges()), ")"
        for node in self.nodes:
            print node
            
        print "@@@@@ Graph.printGraph Completed @@@@@"
        
    def saveTo(self, theFileName):
        '''Saves the graph to a selected file'''
        
        ## This is taken from http://www.onlamp.com/pub/a/python/2002/04/11/jythontips.html?page=2
        print "(Graph.saveTo) Saving to file:", theFileName
        
        outFile = io.FileOutputStream(theFileName)
        outStream = io.ObjectOutputStream(outFile)
        outStream.writeObject(self)
        outFile.close()
        
        print "(Graph.saveTo) Save complete"
        
    def loadFrom(self, theFileName):
        '''Loads a graph from a selected file'''
        
        print "(Graph.loadFrom) Loading from file:", theFileName
        
        ## This is taken from http://www.onlamp.com/pub/a/python/2002/04/11/jythontips.html?page=2
        inFile = io.FileInputStream(theFileName)
        inStream = util.PythonObjectInputStream(inFile) ## Note Python Utilities use; different from standard Java IO
        
        newGraph = inStream.readObject()
        print "(Graph.loadFrom) Printing graph"
        newGraph.printGraph()
        
        print "(Graph.loadFrom) Returning new graph"
        return newGraph
        
        
#####
## The GUI front-end related stuff (the view/controller classes)
#####

class DialogClientInterface:
    '''An interface for dealing with custom dialog boxes
    
    This comes from a Java tutorial, which implements interfaces; interfaces work a bit differently in Python
    Nevertheless, GraphEditorFrame inherits from DialogCilentInterface, and implements these methods'''
    
    def __init__(self):
        pass
    
    def dialogFinished(self):
        '''Specifies the behaviour for closing the dialog box when data is entered and should be kept
        Each implementation of a DialogClientInterface will overrite this method'''
        
        pass
    
    def dialogCancelled(self):
        '''Specifies the behaviour for closing the dialog box when data should be discarded
        Each implementation of a DialogClientInterface will overwrite this method'''
        
        pass 

class SGOMSDialogPanel(JPanel):
    '''The main panel that belongs to SGOMSDialog
    Specifies the text fields etc. for creating/editing a new SGOMS Unit 
    (i.e. a PlanningUnit, UnitTask, Method, or Operator)
    (This panel only contains fields for a name, firing conditions (5 fields), and behaviour (5 fields))
    The panel uses a GridBagLayout
    
    Can be used as a template for other dialog panels (e.g. UnitTaskSimpleDialogPanel)
    This panel is generic enough to handle creating all 4 of the SGOMS unit types, so it
    is used by SGOMSDialog to fill in the name, firing conditions, and behaviour of all 4 SGOMS unit types'''
    
    def __init__(self, theSGOMSUnit):
        '''Initializes the SGOMSDialogPanel with an SGOMS unit (either a PlanningUnit, UnitTask, Method, or Operator)
        as amodel that can feed it inputs
        
        theSGOMSUnit should be a PlanningUnit, UnitTask, Method, or Operator'''
        
        super(SGOMSDialogPanel, self).__init__()
        
        ## Store the SGOMSUnit for modifying 
        self.sGOMSUnit = theSGOMSUnit
        
        
        ## Note: while version 1.0 has a hard-coded set of 5 firing condition and behaviour entries,
        ## the panel was meant to be able to handle adding more entries on the fly at runtime (via a button-press or something).
        ## Due to lack of time, this was never implemented, but the components are mostly there to implement it.
        ## This is why I keep a list of things and iterate through them when adding them, rather than simply hard-coding 
        ## 5 unique behaviour text entries for example. Theoretically, one could keep adding new entries to the lists 
        ## at runtime, but I leave that to the enterprising programmer to figure that out.
        
        ## Note: version 1.3 has hard-coded 10 firing condition and behaviour text entries
        
        ## Keep track of a list of the JLabel components added to the panel
        self.jLabels = []
        #self.jLabelsCounter = 0  ## Maintain a counter to be used for the gridx, gridy etc.
        
        ## Keep track of the name text entries
        self.nameTextEntries = []
        #self.nameTextEntriesCounter = 0
        
        ## Keep track of the firing condition text entries
        self.firingConditionTextEntries = []
        
        ## Keep track of a list of the Behaviour text entries
        self.behaviourTextEntries = []
        
        ## Create the Labels, entries etc. and store them in the components list
        
        ## Create The Labels
        self.nameLabel = JLabel("Enter Name: ")
        self.firingConditionsLabel = JLabel("Specify Firing Conditions: ")
        self.behaviourLabel = JLabel("Specify Behaviours: ")
        
        ## Add the Labels to the components list
        self.jLabels.append(self.nameLabel)
        self.jLabels.append(self.firingConditionsLabel)
        self.jLabels.append(self.behaviourLabel)
        
        ## Create The Text Entries, set the default text, and add them to their respective component lists
        ## There is only one nameEntry, so no need for a loop
        ## nameVar is the default string that appears in the text field upon startup
        if self.sGOMSUnit.ID == None:
            nameVar = "Name"
        else:
            nameVar = self.sGOMSUnit.ID
        
        self.nameEntry = JTextField(nameVar, 50)    ## Default column width = 50 char
        self.nameTextEntries.append(self.nameEntry)
        
        ## Make 5 firing condition text entries and add them to the components list
        for x in range(1, 11):
            
            ## If there is no corresponding firing condition in the SGOMS unit, set the string to an empty string
            if len(self.sGOMSUnit.firingConditions) < x:    ## x is 1 to start
                firingConditionVar = ""     ## firingConditionVar is the default text to be shown in the text box
            else:
            ## If there is a corresponding firing condition in the SGOMS unit, show the firing condition string in the text box
                firingConditionVar = self.sGOMSUnit.firingConditions[x-1]   ## x is 1 to start; index 0 will be x-1 at start
            
            firingConditionEntry = JTextField(firingConditionVar, 50)
            
            self.firingConditionTextEntries.append(firingConditionEntry) 
                        
        ## Make 5 behaviour text entries and add them to the components list
        for x in range(1, 11):
            
            if len(self.sGOMSUnit.behaviour) < x:    ## x is 1 to start
                behaviourVar = ""
            else:
                behaviourVar = self.sGOMSUnit.behaviour[x-1]   ## x is 1 to start; index 0 will be x-1 at start
            
            behaviourEntry = JTextField(behaviourVar, 50)
            
            self.behaviourTextEntries.append(behaviourEntry)               
        
        ## Set the layout manager and add the components to the panel according to the layout constraints
        self.layout = GridBagLayout()
        #self.constraints = GridBagConstraints()
        self.setLayout(self.layout)
            
        ## Add the 3 labels to the gridBagLayout:
        
        ## The name label
        constraints = GridBagConstraints()
        
        constraints.gridx = 0  ## gridx = column# (always 0 for the Labels)
        constraints.gridy = 0   ## gridy = row# (the name label is always at 0)
            
        ## Could tinker with these later...
        constraints.gridwidth = 1;
        constraints.gridheight = 1;
        constraints.weightx = 1; ## grow horizontally
        constraints.weighty = 0; ## don't grow vertically
        constraints.anchor = GridBagConstraints.WEST;
            
        self.add(self.nameLabel, constraints)
        
        
        ## The firing conditions label
        constraints = GridBagConstraints()
        
        constraints.gridx = 0  ## gridx = column# (always 0 for the Labels)
        constraints.gridy = 1   ## gridy = row# (the firing conditions label is always at 1)
            
        ## Could tinker with these later...
        constraints.gridwidth = 1;
        constraints.gridheight = 1;
        constraints.weightx = 1; ## grow horizontally
        constraints.weighty = 0; ## don't grow vertically
        constraints.anchor = GridBagConstraints.WEST;
            
        self.add(self.firingConditionsLabel, constraints)
        
        
        ## The behaviour label
        constraints = GridBagConstraints()
        
        constraints.gridx = 0  ## gridx = column# (always 0 for the Labels)
        constraints.gridy = len(self.firingConditionTextEntries) + 1   ## gridy = row# - Take into account the nameLabel and FC labels
            
        ## Could tinker with these later...
        constraints.gridwidth = 1;
        constraints.gridheight = 1;
        constraints.weightx = 1; ## grow horizontally
        constraints.weighty = 0; ## don't grow vertically
        constraints.anchor = GridBagConstraints.WEST;
            
        self.add(self.behaviourLabel, constraints)
        
                
        ## Add the name text entry to the gridBagLayout (only one, so no need for a loop)
        constraints = GridBagConstraints()
            
        constraints.gridx = 1  ## gridx = column# (always 1 for the text entries)
        constraints.gridy = 0   ## gridy = row# (always 0 for the name text entry)
            
        ## Could tinker with these later...
        constraints.gridwidth = 1
        constraints.gridheight = 1
        constraints.weightx = 1 ## grow horizontally
        constraints.weighty = 0 ## don't grow vertically
        constraints.anchor = GridBagConstraints.WEST
            
        self.add(self.nameEntry, constraints)
               
        ## Add the firing condition text entries to the gridBagLayout (created 5 above)
        self.firingConditionTextEntriesCounter = 0
        
        for textEntry in self.firingConditionTextEntries:
            constraints = GridBagConstraints()
            
            constraints.gridx = 1  ## gridx = column# (always 1 for the text entries)
            constraints.gridy = self.firingConditionTextEntriesCounter +1   ## gridy = row# (equal to the # of previous components)
            
            ## Could tinker with these later...
            constraints.gridwidth = 1
            constraints.gridheight = 1
            constraints.weightx = 1 ## grow horizontally
            constraints.weighty = 0 ## don't grow vertically
            constraints.anchor = GridBagConstraints.WEST
            
            self.add(textEntry, constraints)
            
            self.firingConditionTextEntriesCounter += 1    ## The counter keeps track of where to put the component (row #)
        
        #FDO print "(SGOMSDialogPanel.init) firing condition text entries successfully added to the panel"
        
        ## Add the behaviour text entries to the gridBagLayout (created 5 above)
        self.behaviourTextEntriesCounter = 0
        
        for textEntry in self.behaviourTextEntries:
            constraints = GridBagConstraints()
            
            constraints.gridx = 1  ## gridx = column# (always 1 for the text entries)
            
            ## gridy = row# (equal to the # of previous components)
            constraints.gridy = len(self.firingConditionTextEntries) + 1 + self.behaviourTextEntriesCounter 
            
            ## Could tinker with these later...
            constraints.gridwidth = 1
            constraints.gridheight = 1
            constraints.weightx = 1 ## grow horizontally
            constraints.weighty = 0 ## don't grow vertically
            constraints.anchor = GridBagConstraints.WEST
            
            self.add(textEntry, constraints)
            
            self.behaviourTextEntriesCounter += 1    ## The counter keeps track of how many have been added already
            
        #FDO print "(SGOMSDialogPanel.init) behaviour text entries successfully added to the panel"
        
        print "(SGOMSDialogPanel.__init__) panel initiation completed"
        
class SGOMSDialog(JDialog):
    '''The dialog that comes up when you create a new SGOMS node
    A generic template class for creating new SGOMS nodes (i.e. a Planning Unit, Unit Task, Method, Operator)
    Each of the SGOMS dialogs will be based on this template,
    As of version 1.0 the template is generic enough to create each of the 4 SGOMS unit types'''
    
    def __init__(self, theOwner = None, theTitle = "Create New SGOMS Node", isModal = True, theSGOMSUnit = None, thePoint = None):
        '''Initializes the SGOMSDialog
        
        theOwner is the client application that caused the dialog to open, must be a Frame of some sort (i.e. GraphEditorFrame)
        theTitle specifies the title of the pop-up window
        isModal specifies whether the window must be dealt with before other actions can happen 
        (True = must be dealt with)
        theSGOMSUnit is the generic object that will be modified by the dialog (i.e. a PlanningUnit, UnitTask, Method, or Operator)
        thePoint should be the point where you want the new node to be located, it should be a Point'''
        
        print "SGOMSDialog Initiated"
        
        super(SGOMSDialog, self).__init__(theOwner, theTitle, isModal, windowClosing=self.cancelButtonPressed)
        
        self.dialogOwner = theOwner
        self.title = theTitle
        self.modal = isModal
        self.sGOMSUnit = theSGOMSUnit
        self.point = thePoint
        
        self.okButton = JButton("OK", actionPerformed=self.okButtonPressed)     ## Button label, behaviour
        self.cancelButton = JButton("Cancel", actionPerformed=self.cancelButtonPressed) ## Button label, behaviour
        
        ## Note to self: 
        ## Frames by default are BorderLayout, you should make a main panel that contains everything, and has a GridBagLayout
        ## And then add the main panel to the frame with the .add method
        ## See: http://docs.oracle.com/javase/tutorial/uiswing/components/toplevel.html#contentpane
        ## Also see: http://docs.oracle.com/javase/tutorial/uiswing/layout/using.html
        
        ## Create the main content panel which will act as the content pane, and set the layout to gridbag layout        
        self.contentPane = JPanel()
        layout = GridBagLayout()    ## self.layout gives an error for some reason
        self.contentPane.setLayout(layout)
        
        ## Create a little panel at the bottom to contain the okButton and cancelButton
        self.buttonPanel = JPanel()
        self.buttonPanel.setLayout(FlowLayout(FlowLayout.RIGHT))
        self.buttonPanel.add(self.okButton)
        self.buttonPanel.add(self.cancelButton)
        
        ## This is the panel that contains the text fields etc.
        self.sGOMSDialogPanel = SGOMSDialogPanel(self.sGOMSUnit)       
        
        #FDO print "(SGOMSDialog.init) about to set the constraints for SGOMSDialogPanel"
        
        ## Set the constraints for the SGOMSDialogPanel, and add it to the frame
        constraints = GridBagConstraints()
        constraints.gridx = 0
        constraints.gridy = 0
        constraints.gridwidth = 1
        constraints.gridheight = 1
        constraints.weightx = 1 ## grow horizontally
        constraints.weighty = 1 ## grow vertically
        constraints.anchor = GridBagConstraints.WEST
        #self.layout.setConstraints(self.SGOMSDialogPanel, self.constraints)

        self.contentPane.add(self.sGOMSDialogPanel, constraints)
        
        #FDO print "(SGOMSDialog.init) Constraints for SGOMSDialogPanel set successfully, and added"
        
        ## Set the constraints for the buttonPanel, and add it to the frame
        constraints = GridBagConstraints()
        
        constraints.gridx = 0
        constraints.gridy = 1
        constraints.gridwidth = 1
        constraints.gridheight = 1
        constraints.weightx = 1 ## grow horizontally
        constraints.weighty = 1 ## grow vertically
        constraints.anchor = GridBagConstraints.WEST
        #self.layout.setConstraints(self.buttonPanel, self.constraints)
        #self.add(self.buttonPanel, self.constraints)
        self.contentPane.add(self.buttonPanel, constraints)
        
        #FDO print "(SGOMSDialog.init) Constraints for buttonPanel set successfully, and added"
        
        ## set the frame's content pane to be the panel we've just been populating
        ## From: http://docs.oracle.com/javase/tutorial/uiswing/components/toplevel.html#contentpane
        self.setContentPane(self.contentPane)
        
        #self.add(self.contentPane)
        self.pack()     ## This makes the frame the minimum size required to fit all of the components
        self.setVisible(True)
        
    def okButtonPressed(self, event):
        '''Defines what happens when the ok button is pressed
        
        Modifies the SGOMSUnit, based on the info entered into the dialog box,
        (e.g. adds name, behaviour, and firing conditions)
        and passes the SGOMSUnit to the owner frame'''
        
        print "(SGOMSDialog.okButtonPressed())"
        
        ##theID="Unit Task", theFiringConditions=None, theBehaviour=None):
        ## The first text entry is the name, the next five are the firing conditions, the next five are the behaviours
        self.sGOMSUnit.ID = self.sGOMSDialogPanel.nameEntry.getText()  ## Set the ID
        
        ## Reset the firingConditions, and repopulate them with what is in the text entries
        del self.sGOMSUnit.firingConditions[:]        
        for textEntry in self.sGOMSDialogPanel.firingConditionTextEntries:
            textVar = textEntry.getText()
            if textVar == "":   ## Don't append empty strings to the firing conditions 
                pass
            else:            
                self.sGOMSUnit.firingConditions.append(textVar)  ## Add the firing conditions set in the text entries
        
        ## Reset the behaviours, and repopulate them with what is in the text entries
        del self.sGOMSUnit.behaviour[:]
        for textEntry in self.sGOMSDialogPanel.behaviourTextEntries:
            textVar = textEntry.getText()
            if textVar == "":   ## Don't append empty strings to the behaviours 
                pass
            else:            
                self.sGOMSUnit.behaviour.append(textVar)  ## Add the behaviours set in the text entries
        
        self.owner.dialogFinished(self.sGOMSUnit, self.point)
        print "SGOMSDialog disposed"
        self.dispose()
        
    def cancelButtonPressed(self, event):
        '''Defines what happens when the cancel button is pressed'''
        
        print "(SGOMSDialog.cancelButtonPressed())"      
        self.owner.dialogCancelled()
        print "SGOMSDialog disposed"
        self.dispose()

class SGOMSEditDialog(SGOMSDialog):
    '''The dialog that comes up when you edit an existing SGOMS node
    
    Essentially identical to SGOMSDialog, but has different behaviour when 'ok' is pressed,
    No new node is created, but the edited SGOMSUnit is updated'''
    
    def __init__(self, theOwner = None, theTitle = "Edit SGOMS Unit", isModal = True, theSGOMSUnit = None, thePoint = None):
        '''Initializes the SGOMSEditDialog
        
        theOwner is the client application that caused the dialog to open, must be a Frame of some sort (i.e. GraphEditorFrame)
        theTitle specifies the title of the pop-up window
        isModal specifies whether the window must be dealt with before other actions can happen 
        (True = must be dealt with)
        theSGOMSUnit is the generic object that will be modified by the dialog (i.e. a PlanningUnit, UnitTask, Method, or Operator)
        thePoint should be the point where you want the new node to be located, it should be a Point'''
        
        print "SGOMSEditDialog Initiating..."
        
        super(SGOMSEditDialog, self).__init__(theOwner, theTitle, isModal, theSGOMSUnit, thePoint)
        
        print "...SGOMSEditDialog Initiated"
        
    def okButtonPressed(self, event):
        '''Defines what happens when the ok button is pressed
        
        Modifies the SGOMSUnit, based on the info entered into the dialog box,
        (e.g. adds name, behaviour, and firing conditions)
        and passes the SGOMSUnit to the owner frame via the method owner.editDialogFinished'''
        
        print "(SGOMSEditDialog.okButtonPressed())"
        
        ##theID="Unit Task", theFiringConditions=None, theBehaviour=None):
        ## The first text entry is the name, the next five are the firing conditions, the next five are the behaviours
        self.sGOMSUnit.ID = self.sGOMSDialogPanel.nameEntry.getText()  ## Set the ID
        
        ## Reset the firingConditions, and repopulate them with what is in the text entries
        del self.sGOMSUnit.firingConditions[:]        
        for textEntry in self.sGOMSDialogPanel.firingConditionTextEntries:
            textVar = textEntry.getText()
            if textVar == "":   ## Don't append empty strings to the firing conditions 
                pass
            else:            
                self.sGOMSUnit.firingConditions.append(textVar)  ## Add the firing conditions set in the text entries
        
        ## Reset the behaviours, and repopulate them with what is in the text entries
        del self.sGOMSUnit.behaviour[:]
        for textEntry in self.sGOMSDialogPanel.behaviourTextEntries:
            textVar = textEntry.getText()
            if textVar == "":   ## Don't append empty strings to the behaviours 
                pass
            else:            
                self.sGOMSUnit.behaviour.append(textVar)  ## Add the behaviours set in the text entries
        
        self.owner.editDialogFinished(self.sGOMSUnit)
        print "SGOMSDialog disposed"
        self.dispose()

class GraphEditorPanel(JPanel, MouseListener, MouseMotionListener, KeyListener):
    '''The main drawing panel for the user interface'''
    
    def __init__(self, aGraph = None, aFrame = None):
        '''Initializes the GraphEditorPanel
        
        aGraph should be a Graph
        aFrame should be the frame that contains the GraphEditorPanel'''
        
        super(GraphEditorPanel, self).__init__()
        
        ##Store the Graph
        #if aGraph == None:
        #    self.graph = Graph()
        #else:
        #    self.graph = aGraph
        
        ## ^ The panel should not have a graph of its own, it should always refer to the frame's graph 
        ## Store the owner frame
        self.frame = aFrame
        
        ## Set the background colour
        self.setBackground(Color.white)
            
        ##Store a variable to keep track of a node being dragged
        self.dragNode = None
        self.elasticEndLocation = None  ## Variable to store location for edge dragging
        
        ## Variables for handling dragging of edges
        self.dragEdge = None    
        self.dragPoint = None
        
        ## Sets the border to be a loweredBevelBorder
        self.setBorder(BorderFactory.createLoweredBevelBorder())
        
        ## Add popup menus to the panel to handle right-clicking
        self.popupMenu = JPopupMenu()
        self.editItem = JMenuItem("Edit Node", actionPerformed=self.onEditNode)
        self.popupMenu.add(self.editItem)
        
        ## Global variable to handle right-clicking and editing nodes
        ## Stores the node that was right-clicked on for later editing
        self.editNode = None
        
        #self.setLayout(None)
        #self.setSize(600, 400)
        
        ## Add the event handlers
        self.addEventHandlers()
        
    def addEventHandlers(self):
        '''Adds all event handlers to the GUI'''
        
        self.addMouseListener(self)
        self.addMouseMotionListener(self)
        self.addKeyListener(self)
        
    def removeEventHandlers(self):
        '''Removes all event handlers from the GUI'''
        
        self.removeMouseListener(self)
        self.removeMouseMotionListener(self)
        self.removeKeyListener(self)
            
    def mouseClicked(self, event):
        '''Defines what happens when the mouse is double-clicked, or right clicked
        
        Either selects a Node or Edge, or creates a new kind of Node (if double-clicked)
        Brings up a popup menu for editing nodes if right-clicked on a Node'''
        
        ## On a double-click
        if (event.getClickCount() == 2):
            
            #FDO print "(mouseClicked) at (", event.getX(), ",", event.getY(), ")"
            aNode = self.frame.graph.nodeAt(event.getPoint()) ##Find the node where the click happened
            
            if aNode == None:   ##If there was no node, check to see if it was an edge
                anEdge = self.frame.graph.edgeAt(event.getPoint())
                if anEdge == None: ##If no edge and no node clicked, create a new node
                    
                    ## Check to see which kind of SGOMS unit is selected (set by the RadioButtons in GraphEditorFrameButtonPanel)
                    if self.frame.graph.selectedSGOMSType == "PLANNING_UNIT":
                        print "(GraphEditorPanel.mouseClicked) create new PUNode"
                        ## (self, theOwner = None, theTitle = "Create New SGOMS Node", isModal = True, theSGOMSUnit = None, thePoint = None):
                        pU = PlanningUnit("PlanningUnit_" + str(len(self.frame.graph.sGOMS.planningUnitList)+1))
                        dialog = SGOMSDialog(self.frame, "Create New Planning Unit", True, pU, event.getPoint())
                    
                    if self.frame.graph.selectedSGOMSType == "UNIT_TASK":
                        print "(GraphEditorPanel.mouseClicked) create new UTNode"
                        uT = UnitTask("UnitTask_" + str(len(self.frame.graph.sGOMS.unitTaskList)+1))
                        dialog = SGOMSDialog(self.frame, "Create New Unit Task", True, uT, event.getPoint())
                        
                    if self.frame.graph.selectedSGOMSType == "METHOD":
                        print "(GraphEditorPanel.mouseClicked) create new MNode"
                        m = Method("Method_" + str(len(self.frame.graph.sGOMS.methodList)+1))
                        dialog = SGOMSDialog(self.frame, "Create New Method", True, m, event.getPoint())
                        
                    if self.frame.graph.selectedSGOMSType == "OPERATOR":
                        print "(GraphEditorPanel.mouseClicked) create new ONode"
                        o = Operator("Operator_" + str(len(self.frame.graph.sGOMS.operatorList)+1))
                        dialog = SGOMSDialog(self.frame, "Create New Operator", True, o, event.getPoint())
                          
                else:
                    anEdge.toggleSelected() ##If the click happened near an edge, select it
            else:   ## If there was a node that was clicked, select it
                aNode.toggleSelected()
                            
        # We have changed the model, so now we update the graph
        self.update()
            
    def mousePressed(self, event):
        '''Defines what happens when the mouse is pressed
        
        Used in tandem with mouseDragged to either move objects around, or make new edges'''
        
        ## Find where the click occurred, return the node the click happened in
        aNode = self.frame.graph.nodeAt(event.getPoint())     ## Returns none by default
        #FDO print "(mousePressed) location = ", event.getX(), ",", event.getY()
        if aNode != None:
            #If we pressed on a node, store it in the dragNode variable
            self.dragNode = aNode
            print "(mousePressed) Node to be dragged = ", self.dragNode.label
        ##If the click was in an edge (i.e. not in a node), store the dragEdge variables
        else:
            self.dragEdge = self.frame.graph.edgeAt(event.getPoint()) ## Returns None by default
        
        ## Keep track of the eventPoint (for dragging edges, and multiple nodes)
        self.dragPoint = event.getPoint()
            
    def mouseDragged(self, event):
        '''Defines what happens when the mouse is dragged'''
        
        #FDO print "(mouseDragged)"
        ## Behaviour for dragging nodes
        if self.dragNode != None:   ## If there is a node to drag from (set in mousePressed)
            if self.dragNode.selected == True:  ## If the node is selected
                ## Drag each selected node
                for n in self.frame.graph.returnSelectedNodes():
                    n.location.translate(event.getPoint().x - self.dragPoint.x,
                                         event.getPoint().y - self.dragPoint.y)
                self.dragPoint = event.getPoint()
                #FDO print "(mouseDragged) location of node = ", self.dragNode.location.x, ",", self.dragNode.location.y
            else:   ## If no node, store the point for edge creation
                self.elasticEndLocation = event.getPoint()
        
        ##Behaviour for dragging Edges (moves both attached nodes)
        if self.dragEdge != None:
            if self.dragEdge.selected == True:
                ##Translate the startNode and endNode
                self.dragEdge.startNode.location.translate(event.getPoint().x - self.dragPoint.x, 
                                                           event.getPoint().y - self.dragPoint.y)
                self.dragEdge.endNode.location.translate(event.getPoint().x - self.dragPoint.x,
                                                         event.getPoint().y - self.dragPoint.y)
                self.dragPoint = event.getPoint()
        
        ## If there is no dragNode or dragEdge, translate all of the nodes
        if self.dragNode == None and self.dragEdge == None:
            #FDO print "(GraphEditorPanel.mouseDragged), no dragNode or dragEdge; Translate everything"
            for node in self.frame.graph.nodes:
                node.location.translate(event.getPoint().x - self.dragPoint.x,
                                         event.getPoint().y - self.dragPoint.y)
            self.dragPoint = event.getPoint()
        ## We have changed the model, so now update
        self.update()
            
    def mouseReleased(self, event):
        '''Defines what happens when the mouse is released'''
        
        #FDO print "(mouseReleased)"
        
        ##Check to see if we have let go on a node
        aNode = self.frame.graph.nodeAt(event.getPoint())
        
        ## If so make a new edge between the dragNode and the node we let go on
        if aNode != None and aNode != self.dragNode:
            self.frame.graph.addEdge(self.dragNode, aNode);
        
        ## Handle right-clicking by bringing up a popup menu to edit the Node selected
        ## Only provide a popup menu if the release was on top of a Node                
        if SwingUtilities.isRightMouseButton(event):
            if isinstance(aNode, Node):
                print "!!!!!!! Right-Click Detected, isRightMouseButton, mouseReleased !!!!!"
                self.editNode = aNode
                self.popupMenu.show(event.getComponent(), event.getX(), event.getY())
        
        ##Refresh the panel either way
        self.dragNode = None
        self.update()
            
    def keyPressed(self, event):
        '''Defines what happens when a keyboard key is pressed'''
        
        if event.getKeyCode() == KeyEvent.VK_DELETE:
            print "(GraphEditorPanel.keyPressed) DELETE pressed"
            
            ## Remove selected edges
            for e in self.frame.graph.returnSelectedEdges():
                self.frame.graph.deleteEdge(e)
            
            ## Remove selected nodes
            for n in self.frame.graph.returnSelectedNodes():
                self.frame.graph.deleteNode(n)
                #FDO for node in self.graph.nodes:
                    #FDO print node.label
            self.update()       
    
    def onEditNode(self, event):
        '''Specifies what happens when the 'edit node' popup menu item is clicked on
        
        Brings up an SGOMSEditDialog whose fields are filled in by the contents of the SGOMS Node
        so that they can be edited'''
        
        print "!!!!!!!!!!!!! (GraphEditorPanel.onEditNode) Edit node pressed !!!!!!!!!!!!!!!!!"
        
        #theSource = event.getSource()
        #theComponent = theSource.getComponent()
        #print theSource
        #print theComponent
        #theNode = self.graph.nodeAt(event.getSource().getPoint())
        
        if isinstance(self.editNode, PUNode):
            sGOMSUnit = self.editNode.planningUnit
        
        if isinstance(self.editNode, UTNode):
            sGOMSUnit = self.editNode.pUxUTRelation.unitTask
            
        if isinstance(self.editNode, MNode):
            sGOMSUnit = self.editNode.uTxMRelation.method
            
        if isinstance(self.editNode, ONode):
            sGOMSUnit = self.editNode.mxORelation.operator
            
        ## theOwner = None, theTitle = "Create New SGOMS Node", isModal = True, theSGOMSUnit = None, thePoint = None
        dialog = SGOMSEditDialog(self.frame, "Edit SGOMS Node", True, sGOMSUnit, self.editNode.location)
        
        ## Reset the editNode at the end of the function
        self.editNode = None
    
    def paintComponent(self, aPen):
        '''This is the method responsible for displaying the graph
        
        aPen should be a Graphics object'''
                
        #######
        #This is the workaround for a Jython bug which doesn't allow
        #for calling super(...) directly for the paintComponent method
        #The syntax normally would be: super(GraphEditorPanel, self).paintComponent(aPen)
        #But this throws an exception, because the paintComponent method is protected in Java
        #See: http://sourceforge.net/p/jython/mailman/message/9129532/
        #Also see: http://bugs.jython.org/issue1540
        #######
        
        self.super__paintComponent(aPen)    ## This is the workaround here (note weird syntax)
        
        self.frame.graph.draw(aPen)
        
        ##If you are dragging from an unselected node, draw a line
        if self.dragNode != None:
            if self.dragNode.selected == False:
                #FDO print "(paintComponent) draw elastic line"               
                aPen.drawLine(self.dragNode.location.x, self.dragNode.location.y,
                              self.elasticEndLocation.location.x, self.elasticEndLocation.location.y)
        
    def update(self):
        '''Repaints the GraphEditorPanel based on the model (graph)'''
        
        print "(GraphEditorPanel.update) Begin Graphics Update"
        self.requestFocus()
        self.removeEventHandlers()
        self.repaint()
        self.addEventHandlers()

class GraphEditorFrameButtonPanel(JPanel):
    '''A panel that contains a few Radio buttons for creating PUs, UTs, etc.
    This is on the main frame, next to the drawing panel'''
    
    def __init__(self, aGraph = None, aFrame = None):
        '''Initializes the ButtonPanel
        
        aGraph should be a Graph
        aFrame should be a JFrame, the owner of the ButtonPanel, to keep as a reference'''
        
        super(GraphEditorFrameButtonPanel, self).__init__()
        
        ##Store the Graph
        #if aGraph == None:
        #    self.graph = Graph()
        #else:
        #    self.graph = aGraph
            #self.setBackground(Color.white)
            
        ## ^ The panel should not have a graph of its own, it should always refer to the frame's graph 
        
        ## Store the owner frame
        self.frame = aFrame
                
        ##Set the layout
        self.setLayout(BoxLayout(self, BoxLayout.PAGE_AXIS))    ## Managing container, vertical orientation
        
        #self.createButtons()
        self.createRadioButtons()
        
        #self.setSize(100,400)
                
    def createRadioButtons(self):
        '''Creates a series of radio buttons and places them onto the JPanel'''
        
        ## A buttongroup is required to contain the radio buttons
        self.buttonGroup = ButtonGroup()
        
        ## Create the radio buttons, with their names and behaviour
        self.planningUnitButton = JRadioButton("Planning Unit", actionPerformed = self.planningUnitButtonSelected)
        self.unitTaskButton = JRadioButton("Unit Task", actionPerformed = self.unitTaskButtonSelected)
        self.methodButton = JRadioButton("Method", actionPerformed = self.methodButtonSelected)
        self.operatorButton = JRadioButton("Operator", actionPerformed = self.operatorButtonSelected)
        
        ## Add the radio buttons to the button group
        self.buttonGroup.add(self.planningUnitButton)
        self.buttonGroup.add(self.unitTaskButton)
        self.buttonGroup.add(self.methodButton)
        self.buttonGroup.add(self.operatorButton)
        
        ## Add the radio buttons to the panel
        self.add(self.planningUnitButton)
        self.add(self.unitTaskButton)
        self.add(self.methodButton)
        self.add(self.operatorButton)
        
    def planningUnitButtonSelected(self, event):
        '''Specifies what happens when the radio button planningUnitButton is selected
        
        Toggles the graph.selectedSGOMSType to be "PLANNING_UNIT", allowing for the creation of new PUNodes in the Graph'''
        
        self.frame.graph.selectedSGOMSType = "PLANNING_UNIT"
        
        print "(ButtonPanel.planningUnitButtonSelected) selectedSGOMSType = ", self.frame.graph.selectedSGOMSType
        
    def unitTaskButtonSelected(self, event):
        '''Specifies what happens when the radio button unitTaskButton is selected
        
        Toggles the graph.selectedSGOMSType to be "UNIT_TASK", allowing for the creation of new UTNodes in the Graph'''
        
        self.frame.graph.selectedSGOMSType = "UNIT_TASK"
        
        print "(ButtonPanel.unitTaskButtonSelected) selectedSGOMSType = ", self.frame.graph.selectedSGOMSType
        
    def methodButtonSelected(self, event):
        '''Specifies what happens when the radio button methodButton is selected
        
        Toggles the graph.selectedSGOMSType to be "METHOD", allowing for the creation of new MNodes in the Graph'''
        
        self.frame.graph.selectedSGOMSType = "METHOD"
        
        print "(ButtonPanel.methodButtonSelected) selectedSGOMSType = ", self.frame.graph.selectedSGOMSType
        
    def operatorButtonSelected(self, event):
        '''Specifies what happens when the radio button operatorButton is selected
        
        Toggles the graph.selectedSGOMSType to be "OPERATOR", allowing for the creation of new ONodes in the Graph'''
        
        self.frame.graph.selectedSGOMSType = "OPERATOR"
        
        print "(ButtonPanel.operatorButtonSelected) selectedSGOMSType = ", self.frame.graph.selectedSGOMSType
                  
        
class GraphEditorFrame(JFrame, DialogClientInterface):
    '''A view which holds a GraphEditorPanel, a GraphEditorFrameButtonPanel, and a few menu items
    This is the main frame that the GUI is comprised of
    '''
    
    def __init__(self, theTitle = "Title", theGraph = None):
        '''Initializes the GraphEditorFrame
        
        theTitle should be a string
        theGraph should be a Graph'''
        
        if theGraph == None:
            self.graph = Graph()
        else:
            self.graph = theGraph
        
        ## These are the JPanels
        self.editor = GraphEditorPanel(theGraph, self)   ## The drawing panel
        self.buttonPanel = GraphEditorFrameButtonPanel(theGraph, self)  ## The RadioButton Panel
             
        
        ## Code for adding the panel components
        self.setLayout(None)
        
        self.buttonPanel.setSize(100,200)
        self.buttonPanel.setLocation(5,10)
        self.add(self.buttonPanel)
        
        #preferredSize = Dimension(600,800)
        #self.editor.setPreferredSize(preferredSize)
        
        self.editor.setSize(1000,600)
        self.editor.setLocation(110,10)
        self.add(self.editor)
             
        ## Add the menu Items
        menubar = JMenuBar()
        
        ## The file menu
        fileMenu = JMenu("File")
        
        ## The Export to ACT-R  Menu Item
        fileExport = JMenuItem("Export To ACT-R",
            actionPerformed=self.exportToACTR)
        fileExport.setToolTipText("Convert Current Graph Into an ACT-R Readable Model")
        fileMenu.add(fileExport)
        
        ## The save to file Menu Item
        fileSave = JMenuItem("Save As",
                             actionPerformed=self.saveGraph)
        fileSave.setToolTipText("Save current model to a selected file")
        fileMenu.add(fileSave)
        
        ## The load from file Menu Item
        fileLoad = JMenuItem("Load",
                             actionPerformed=self.loadGraph)
        fileLoad.setToolTipText("Load a model from a selected file")
        fileMenu.add(fileLoad)

        ## The help menu
        menubar.add(fileMenu)

        helpMenu = JMenu("Help")
        helpItem = JMenuItem("More Information", actionPerformed=self.moreInformationSelected)
        helpMenu.add(helpItem)
        
        menubar.add(helpMenu)
        
        self.setJMenuBar(menubar)


        ## Add the title and other basic frame operations
        self.setTitle(theTitle)
        self.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)
        #self.pack()
        self.setSize(1200, 700)
        self.setVisible(True)
        
        print "GraphEditorFrame Initiated"
            
    def dialogFinished(self, theSGOMSUnit, thePoint):
        '''Specifies what to do when an SGOMSDialog dialog box ends successfully
        Adds the newly created SGOMSUnit to the graph
        
        theSGOMSUnit should be a PlanningUnit, UnitTask, Method, or Operator
        thePoint should be a Point (where you want the node to be located)'''
        
        print "(GraphEditorFrame.dialogFinishedGeneric)"
        
        ## If theSGOMSUnit is a PlanningUnit
        if isinstance(theSGOMSUnit, PlanningUnit):
            self.graph.addPUNodeAdvancedNew(theSGOMSUnit, thePoint)
            self.editor.update()
            
        ## If theSGOMSUnit is a UnitTask:
        if isinstance(theSGOMSUnit, UnitTask):
            self.graph.addUTNodeAdvancedNew(theSGOMSUnit, thePoint)
            self.editor.update()
            
        ## If theSGOMSUnit is a Method:
        if isinstance(theSGOMSUnit, Method):
            self.graph.addMNodeAdvancedNew(theSGOMSUnit, thePoint)
            self.editor.update()
            
        ## If theSGOMSUnit is an Operator:
        if isinstance(theSGOMSUnit, Operator):
            self.graph.addONodeAdvancedNew(theSGOMSUnit, thePoint)
            self.editor.update()
            
        self.graph.printGraph()
        self.graph.sGOMS.printModelContentsAdvanced()
            
    def editDialogFinished(self, theSGOMSUnit):
        '''Specifies what to do when an SGOMSEditDialog dialog box ends successfully
        updates the editor
        
        theSGOMSUnit should be a PlanningUnit, UnitTask, Method, or Operator
        '''
        
        self.graph.update()
        self.editor.update()
        print "(GraphEditorFrame.editDialogFinished)"
        
        self.graph.printGraph()
        self.graph.sGOMS.printModelContentsAdvanced()
        
    def dialogCancelled(self):
        '''Specifies the behaviour for closing the dialog box when data should be discarded
        Essentially, nothing will happen when cancel is pressed
        '''
        print "(GraphEditorFrame.dialogCancelled)"
        pass
    
    def exportToACTR(self, event):
        '''Exports the Graph to an ACT-R readable python file
        
        This is an event handler for the file -> Export to ACT-R command
        Opens a JFileChooser for choosing a save location
        Calls SGOMS_Model.outputToACTR(filename)
        event is the event object passed by the menu item'''
        
        print "(GraphEditorFrame.exportToACTR) Called"
        
        chooseFile = JFileChooser()
        theFilter = FileNameExtensionFilter(".py", ["py"])
        chooseFile.addChoosableFileFilter(theFilter)

        ret = chooseFile.showDialog(self, "Export")

        if ret == JFileChooser.APPROVE_OPTION:
            theFile = chooseFile.getSelectedFile()
            theFileName = theFile.getCanonicalPath()
            
            #FDO print "(GraphEditorFrame.exportToACTR), theFile =", theFile
            print "(GraphEditorFrame.exportToACTR) Selected Path = ", theFileName
        
            self.graph.sGOMS.outputToACTR(theFileName)
        
        else:
            print "(GraphEditorFrame.exportToACTR) dialog cancelled"
            
    def saveGraph(self, event):
        '''The event handler for the file -> save function
        
        Saves the contents of the graph to a selected file
        calls self.graph.saveTo(file)'''
        
        chooseFile = JFileChooser()
        theFilter = FileNameExtensionFilter(".txt", ["txt"])
        chooseFile.addChoosableFileFilter(theFilter)

        ret = chooseFile.showDialog(self, "Save As")

        if ret == JFileChooser.APPROVE_OPTION:
            theFile = chooseFile.getSelectedFile()
            theFileName = theFile.getCanonicalPath()
            
            print "(GraphEditorFrame.saveGraph) Selected Path = ", theFileName
        
            self.graph.saveTo(theFileName)
        
        else:
            print "(GraphEditorFrame.saveGraph) dialog cancelled"      
        
    def loadGraph(self, event):
        '''The event handler for the file -> load function
        
        Loads the contents of the graph from a selected file
        calls self.graph.loadFrom(file)
        Updates the GraphEditorFrame and GraphEditorPanel to display the new graph'''
        
        chooseFile = JFileChooser()
        theFilter = FileNameExtensionFilter(".txt", ["txt"])
        chooseFile.addChoosableFileFilter(theFilter)

        ret = chooseFile.showDialog(self, "Load")

        if ret == JFileChooser.APPROVE_OPTION:
            theFile = chooseFile.getSelectedFile()
            theFileName = theFile.getCanonicalPath()
            
            #FDO print "(GraphEditorFrame.exportToACTR), theFile =", theFile
            print "(GraphEditorFrame.loadGraph) Selected Path = ", theFileName
        
            newGraph = self.graph.loadFrom(theFileName) ## Returns the loaded graph
            
            print"(GraphEditorFrame.loadGraph) printing graph and SGOMS Model:"
            newGraph.printGraph()
            newGraph.sGOMS.printModelContentsAdvanced()
            
            print "(GraphEditorFrame.loadGraph) setting new Graph"
            self.graph = newGraph
            self.editor.graph = newGraph
        
        else:
            print "(GraphEditorFrame.loadGraph) dialog cancelled"
                
        self.editor.update()
        
    def moreInformationSelected(self, event):
        '''Brings up a window providing more information about the GUI
        (Links to the documentation)
        
       This is an event handler for the Help --> More Information menu
       event is the event object passed by the menu item'''
        
        print "(GraphEditorFrame.aboutSelected) Called"
        
        JOptionPane.showMessageDialog(self, "Documentation can be found at: \nhttps://github.com/CarletonCognitiveModelingLab/SGOMS_GUI",
            "Documentation", JOptionPane.INFORMATION_MESSAGE)
     

## Code that runs the GUI

#map1 = Graph("SGOMS Test")
#frame = GraphEditorFrame("SGOMS_GUI_1.1", map1)

#map1 = Graph("SGOMS Test")
frame = GraphEditorFrame("SGOMS_GUI_1.2")


#print frame.graph
#print frame.graph.SGOMS

#map1.SGOMS.printModelContentsAdvanced()


