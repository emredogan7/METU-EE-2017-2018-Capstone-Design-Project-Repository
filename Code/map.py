class Map:
    'Map class for mapping the maze Directions'
    Map_Array = []      # Mapping array
    Last = 0
    Index = 0           # Shows where the robot is
    Direction = 1       # 1 for moving Forward
                        # -1 for moving Backward

    def __init__(self):
        print "Robot started to move! \n"

    def Turn_Right(self) :
        print "Robot is turning right! \n"
        Map.Index = Map.Index + Map.Direction
        if Map.Direction == 1 and Map.Index > Map.Last :
            Map.Map_Array.append('R')
            Map.Last = Map.Last + 1

    def Turn_Left(self) :
        print "Robot is turning left! \n"
        Map.Index = Map.Index + Map.Direction
        if Map.Direction == 1 and Map.Index > Map.Last :
            Map.Map_Array.append('L')
            Map.Last = Map.Last + 1


    def Change_Direction(self) :
        print "Robot's direction is changed, now! \n"
        Map.Direction = Map.Direction * ( -1 )

    def printo(self):
        print "Map Array : ", Map.Map_Array
        print "Current, Last, Direction : ", Map.Index, Map.Last, Map.Direction, "\n"

    def Move_Forward(self) :
        print "Robot is moving forward! \n"
        Map.Index = Map.Index + Map.Direction
        if Map.Direction == 1 and Map.Index > Map.Last :
            Map.Map_Array.append('F')
            Map.Last = Map.Last + 1

    def Autonomous(self) :
        if Map.Direction == 1 :
            if Map.Index < Map.Last :
                print "Autonomous mode"
                if Map.Index < 0 :
                    self.Move_Forward()
                else:
                    if Map.Map_Array[Map.Index] == 'F' :
                        self.Move_Forward()
                    elif Map.Map_Array[Map.Index] == 'R' :
                        self.Turn_Right()
                    elif Map.Map_Array[Map.Index] == 'L' :
                        self.Turn_Left()
            elif Map.Index > Map.Last:
                print "Error: 55"
            else:
                print "Can't Autonomous"
        else:
            print "Autonomous mode"
            if Map.Index <= 0 :
                print "Robot is not in maze anymore!"
                self.Move_Forward()
            else:
                Map.Index -= 1
                if Map.Map_Array[Map.Index] == 'F' :
                    self.Move_Forward()
                elif Map.Map_Array[Map.Index] == 'L' :
                    self.Turn_Right()
                elif Map.Map_Array[Map.Index] == 'R' :
                    self.Turn_Left()
                else :
                    print "Error:70"
                Map.Index += 1




robot = Map()
robot.printo()

robot.Turn_Right()
robot.printo()

robot.Turn_Left()
robot.printo()

robot.Move_Forward()
robot.printo()

robot.Turn_Left()
robot.printo()

robot.Turn_Right()
robot.printo()

robot.Autonomous()
robot.printo()

robot.Change_Direction()
robot.printo()

robot.Autonomous()
robot.printo()

robot.Autonomous()
robot.printo()
robot.Autonomous()
robot.printo()
robot.Autonomous()
robot.printo()
robot.Autonomous()
robot.printo()
robot.Autonomous()
robot.printo()
robot.Autonomous()
robot.printo()
robot.Autonomous()
robot.printo()
robot.Change_Direction()
robot.printo()
robot.Autonomous()
robot.printo()
robot.Autonomous()
robot.printo()
robot.Autonomous()
robot.printo()
robot.Autonomous()
robot.printo()
robot.Autonomous()
robot.printo()
robot.Autonomous()
robot.printo()
robot.Autonomous()
robot.printo()
robot.Autonomous()
robot.printo()
robot.Autonomous()
robot.printo()
robot.Autonomous()
robot.printo()
