import math
class MLPlay:
    def __init__(self, player):
        self.player = player
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        self.car_vel = 0
        self.car_pos = ()
        self.lane=-1
        self.mode=0
        self.prepose=0
        self.dangerous=False
        self.tt=2
        self.lane_center = [35, 105, 175, 245, 315, 385, 455, 525, 595] #lane to move
        pass

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """

        if scene_info["status"] != "ALIVE":
            return "RESET"
        lane_car=[999,999,999,999,999,999,999,999,999]
        self.car_pos = scene_info[self.player]
        task=0
        front_car_speed=15
        if len(self.car_pos)==0:
            return["SPEED"]

        for car in scene_info["cars_info"]:
            if car["id"]==self.player_no:
                self.car_vel = car["velocity"]
                if self.lane==-1 :
                    self.lane=(self.car_pos[0]-35)//70 
                elif (self.car_pos[0]-35)%70==0:
                    self.prepose=(self.car_pos[0]-35)//70 
            elif -55<self.car_pos[1]-car["pos"][1]<360+self.car_vel*1.5 +(self.car_pos[1]-380)//2: 
                Distance=self.car_pos[1]-car["pos"][1] 
                if car["id"]<5 and -20<car["pos"][0]-self.car_pos[0]<20 and -40<Distance<80:                    
                    lane_car[self.prepose]=Distance
                    self.dangerous=True
                    if car["pos"][0]-self.car_pos[0]>0:
                        task=-1
                    else:
                        task=1
                if lane_car[(car["pos"][0]-35)//70]>Distance:
                    lane_car[(car["pos"][0]-35)//70]=Distance
                    
                #same lane
                if -25<self.car_pos[0]-car["pos"][0]<25 and  car["id"]>5:
                    if front_car_speed>=car["velocity"]:
                        front_car_speed=car["velocity"]     
        #print(lane_car,"lane",self.lane,"prepose",self.prepose,self.car_pos, front_car_speed ,self.car_vel,,self.dangerous)
        
        if self.tt!=2:
            self.tt+=1
            return["BRAKE"]
        if self.dangerous:
            self.dangerous=False 
            if task==-1 and self.prepose!=0 :
                 if lane_car[self.prepose-1]>300:
                    return ["MOVE_LEFT"]
            elif task==1 and self.prepose!=8:
                if lane_car[self.prepose+1]>300:
                     return ["MOVE_RIGHT"]
            else:
                return ["BRAKE"]
        
        

        # CHANGE LANE 999
        elif lane_car[self.lane]==999:              
            if self.lane>=6 and lane_car[self.lane-1]==999:
                    self.lane=self.lane-1
            elif self.lane<=2 and lane_car[self.lane+1]==999:
                self.lane=self.lane+1
        # right side most
        elif self.prepose==8 :
            if lane_car[7]>=250 :
                if lane_car[8]<500 or -20<lane_car[7]-lane_car[8]<100:
                    self.lane=7
                    self.prepose=8                    
            elif front_car_speed<self.car_vel and lane_car[8]<150:
                return["BRAKE"]

        # left side most
        elif self.prepose==0:
            if lane_car[1]>=250:
                if lane_car[0]<500 or -20<lane_car[1]-lane_car[0]<100:
                    self.lane=1
                    self.prepose=0                         
            elif front_car_speed<self.car_vel and lane_car[0]<150:
                return["BRAKE"]

        else:
            if lane_car[self.prepose+1]>lane_car[self.prepose]>0:
                if self.lane==7 and lane_car[6]>450:
                    self.lane=self.prepose-1                   
                else:
                    self.lane=self.prepose+1

            if lane_car[self.prepose-1]>=lane_car[self.prepose]>0:
                if self.prepose==1 and lane_car[2]>450 or lane_car[self.prepose-1]<lane_car[self.prepose+1]:
                    self.lane=self.prepose+1 
                else:
                    self.lane=self.prepose-1

            elif lane_car[self.lane]<lane_car[self.prepose]:
                tmp=self.lane
                self.lane=self.prepose
                self.prepose=tmp
                self.tt=-1
                return["BRAKE"]


        # retrun value        
        if self.car_pos[0]>self.lane_center[self.lane] :   
            if 10<lane_car[self.prepose]<135+self.car_vel*2-front_car_speed and front_car_speed<=self.car_vel :    
                return ["BRAKE", "MOVE_LEFT"]
            elif 10<lane_car[self.prepose]<100 and front_car_speed<=self.car_vel:
                return ["BRAKE"]
            else:
                return ["SPEED", "MOVE_LEFT"]
        elif self.car_pos[0]<self.lane_center[self.lane]:
            if 10<lane_car[self.prepose]<135+self.car_vel*2-front_car_speed and front_car_speed<=self.car_vel:    
                return ["BRAKE", "MOVE_RIGHT"]
            elif 10<lane_car[self.prepose]<100 and front_car_speed<=self.car_vel:
                return ["BRAKE"]
            else:
                return ["SPEED", "MOVE_RIGHT"]
        else: 
            if 10<lane_car[self.prepose]<130+self.car_vel*2-front_car_speed  and front_car_speed<=self.car_vel:
                return ["BRAKE"]
            else:        
                return ["SPEED"]               
        return ["SPEED"] 


    def reset(self):
        """
        Reset the status
        """
        pass

    
