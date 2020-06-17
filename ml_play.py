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
        self.test="none"
        self.dangerous=False
        self.lane_center = [35, 105, 175, 245, 315, 385, 455, 525, 595,-1] #lane to move
        pass

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        lane_car=[999,999,999,999,999,999,999,999,999]
        self.car_pos = scene_info[self.player]
        task=0
        front_car_speed=15
        if len(self.car_pos)==0:
            return["SPEED"]
        # if self.prepose*70+35-self.car_pos[0]>30 or self.prepose*70+35-self.car_pos[0]<-30:
        #     self.prepose=self.lane
        for car in scene_info["cars_info"]:
            if car["id"]==self.player_no:
                self.car_vel = car["velocity"]
                if self.lane==-1 or (self.car_pos[0]-35)%70==0:
                   self.prepose= self.lane=(self.car_pos[0]-35)//70 

            elif -45<self.car_pos[1]-car["pos"][1]<350+self.car_vel*1.5:  
                Distance=self.car_pos[1]-car["pos"][1] 
                if car["id"]<5 and -15<car["pos"][0]-self.car_pos[0]<15 and -10<Distance<10:                    
                    lane_car[self.prepose]=Distance
                    self.dangerous=True
                    if car["pos"][0]-self.car_pos[0]>0:
                        task=-1
                    else:
                        task=1
                if lane_car[(car["pos"][0]-35)//70]>Distance:
                    lane_car[(car["pos"][0]-35)//70]=Distance
                    
                #same lane
                if -15<self.car_pos[0]-car["pos"][0]<15:
                    if front_car_speed>=car["velocity"]:
                        front_car_speed=car["velocity"]  
                        print(car["id"])    
        #print(lane_car,self.lane,self.prepose,self.car_pos[0], front_car_speed ,self.car_vel,self.test)
        if self.dangerous:
            self.test="BRAKE" 
            self.dangerous=False 
            if task==-1 and self.prepose!=0 :
                 if lane_car[self.prepose-1]>300:
                    self.lane=self.prepose-1
            elif task==1 and self.prepose!=8:
                if lane_car[self.prepose+1]>300:
                    self.lane=self.prepose+1
            else:
                return ["BRAKE"]
        #right side most
        if self.car_pos[0]==self.lane_center[8] :
            if lane_car[7]>=lane_car[8]:
                if lane_car[8]>500:
                 return["SPEED"]
                else:
                    self.lane=7
                    self.prepose=8    
            elif lane_car[7]>250:
                self.lane=7
                self.prepose=8     
            else:
                return["BRAKE"]
        #left side most
        elif self.car_pos[0]==self.lane_center[0] :
            if lane_car[1]>=lane_car[0]:
                if lane_car[0]>500:
                 return["SPEED"]
                else:
                    self.lane=1
                    self.prepose=0   
            elif lane_car[1]>250:
                self.lane=1
                self.prepose=0           
            else:
                return["BRAKE"]
        #CHANGE LANE
        elif lane_car[self.lane]!=999:   
            if self.car_pos[0]==self.lane_center[self.lane] :
                self.prepose=self.lane
                if lane_car[self.prepose+1]>lane_car[self.prepose]>0:                   
                    self.lane=self.prepose+1
                if lane_car[self.prepose-1]>=lane_car[self.prepose+1]>0: 
                   if self.prepose>=5 or lane_car[self.prepose+1]<300:
                        self.lane=self.prepose-1
            elif lane_car[self.prepose]>lane_car[self.lane]:
                 self.lane=self.prepose

        if scene_info["status"] != "ALIVE":
            return "RESET"

        if lane_car[self.prepose]<999:
            if self.car_pos[0]>self.lane_center[self.lane] :  
                self.test="left"    
                if 10<lane_car[self.prepose]<130+self.car_vel and front_car_speed<=self.car_vel :    
                    return ["BRAKE", "MOVE_LEFT"]
                else:
                    return ["SPEED", "MOVE_LEFT"]
            elif self.car_pos[0]<self.lane_center[self.lane]:
                self.test="right" 
                if 10<lane_car[self.prepose]<130+self.car_vel and front_car_speed<=self.car_vel:    
                    return ["BRAKE", "MOVE_RIGHT"]
                else:
                    return ["SPEED", "MOVE_RIGHT"]
            else: 
                if 10<lane_car[self.prepose]<130 and front_car_speed<=self.car_vel:
                    return ["BRAKE"]
                else:
                    self.test="SPEED"          
                    return ["SPEED"]          
        self.test="SPEED"       
        return ["SPEED"]     
        
    def reset(self):
        """
        Reset the status
        """
        pass

    
