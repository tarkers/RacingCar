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
        self.ori=0
        self.prepose=0
        self.test="none"
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
        coin_numbers=[0,0,0,0,0,0,0,0,0]
        player_place=[0,0,0,0,0,0,0,0,0]
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
                    self.prepose=self.lane
                elif (self.car_pos[0]-35)%70==0:
                    self.prepose=(self.car_pos[0]-35)//70 
            elif -55<self.car_pos[1]-car["pos"][1]<360+self.car_vel*1.5 +(self.car_pos[1]-380)//3 : 
                Distance=self.car_pos[1]-car["pos"][1] 
                if car["id"]<5 :
                    if  abs(car["pos"][0]-self.car_pos[0])<50 and -20<Distance<70+self.car_vel-car["velocity"]:
                        if self.car_pos[0]>car["pos"][0]:
                            lane_car[self.prepose-1]=Distance
                        else:
                            lane_car[self.prepose+1]=Distance
                        self.dangerous=True
                        if car["pos"][0]-self.car_pos[0]>0:
                            task=-1
                        else:
                            task=1    
                tmp_car=0 
                pos=-1 
                
                for w in self.lane_center:
                    pos+=1
                    if -20<=(car["pos"][0]-w)<=20:
                       break
                
                if lane_car[pos]>Distance :
                    if car["id"]<5 and (car["pos"][0]-35)%70==0:
                        player_place[(car["pos"][0]-35)//70]=1
                    else:
                        lane_car[pos]=Distance
                    
                #same lane
                if -25<self.car_pos[0]-car["pos"][0]<25 and  car["id"]>5:
                    if front_car_speed>=car["velocity"]:
                        front_car_speed=car["velocity"]     
        # print(lane_car,"lane",self.lane,"prepose",self.prepose,self.car_pos, front_car_speed ,self.car_vel,self.test,self.dangerous)
        have_coin=False
        for coin in scene_info["coins"]:
            if 0<=self.car_pos[1]-coin[1]<=400:
                coin_numbers[(coin[0]-25)//70]+=1
                have_coin=True
            
        if self.tt!=2:
            self.tt+=1
            self.test="BRAKE"
            return["BRAKE"]

        elif self.dangerous:
            self.test="danger" 
            self.dangerous=False
            if task==-1 and self.prepose!=0 and lane_car[self.prepose]>150:
                 if self.car_pos[0]-self.lane_center[self.prepose-1]>25 or lane_car[self.prepose-1]>300:
                    return ["SPEED","MOVE_LEFT"]
            elif task==1 and self.prepose!=8  and lane_car[self.prepose]>150:
                if self.lane_center[self.prepose+1]-self.car_pos[0]>25 or lane_car[self.prepose+1]>300:
                     return ["SPEED","MOVE_RIGHT"]
            else:
                if task==-1:
                    self.test="BRAKE---"
                    return ["BRAKE","MOVE_LEFT"]
                else:
                    return ["BRAKE","MOVE_RIGHT"]
        coin_side=False
        for i in range(8):
            if coin_numbers[i]>0:
                if i>self.prepose:
                    coin_side=True
                else:
                    coin_side=False
                break
        # print(coin_side)
        # CHANGE LANE 999
        if lane_car[self.lane]>=200 and have_coin==True:          
            if self.lane>=1 and lane_car[self.lane-1]>=200 and not coin_side:
                if coin_numbers[self.lane]==0:
                    self.lane=self.lane-1
            elif self.lane<=7 and lane_car[self.lane+1]>=200 and coin_side:
                if coin_numbers[self.lane]==0:
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

        # change lane
        else :
            if lane_car[self.prepose+1]>lane_car[self.prepose]>0:
                if self.lane==7 and lane_car[6]>450 or lane_car[6]<-45:
                    self.lane=self.prepose-1                   
                else:
                    self.lane=self.prepose+1

            if lane_car[self.prepose-1]>lane_car[self.prepose]>0:
                if self.prepose==1 and lane_car[2]>450 or lane_car[2]<-45 or lane_car[self.prepose-1]<lane_car[self.prepose+1]:
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
            # print(self.lane)
            self.test="left"   
            if 10<lane_car[self.prepose]<135+self.car_vel*2-front_car_speed and front_car_speed<self.car_vel :    
                return ["BRAKE", "MOVE_LEFT"]
            elif 10<lane_car[self.prepose]<110+self.car_vel-front_car_speed  and front_car_speed<self.car_vel:
                return ["BRAKE"]
            else:
                return ["SPEED", "MOVE_LEFT"]
        elif self.car_pos[0]<self.lane_center[self.lane]:
            self.test="right" 
            if 10<lane_car[self.prepose]<135+self.car_vel*2-front_car_speed and front_car_speed<self.car_vel:    
                return ["BRAKE", "MOVE_RIGHT"]
            elif 10<lane_car[self.prepose]<110+self.car_vel-front_car_speed and front_car_speed<self.car_vel:
                return ["BRAKE"]
            else:
                return ["SPEED", "MOVE_RIGHT"]
        else: 
            if 10<lane_car[self.prepose]<133+self.car_vel*2-front_car_speed  and front_car_speed<self.car_vel: 
                return ["BRAKE"]
            else:
                self.test="SPEED"
                self.prepose=self.lane
                return["SPEED"]
                         
                    
        self.test="SPEED---"       
        return ["SPEED"] 


    def reset(self):
        """
        Reset the status
        """
        pass
