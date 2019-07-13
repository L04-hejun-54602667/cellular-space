import tkinter as tk
from PIL import Image, ImageTk
import serial

bg_color='black'
font_color='green'
font_color2='purple'
font_color3='yellow'
font_size=15 

#for page three#
count=0 #counting the number of clicking button
button_list=['click me!', 'i touch the alive cell','i touch the alive cell again','i touch the alive cell again','try again']
serialPort='/dev/cu.usbmodem14301'
baudRate=9600       


class Base():
    def __init__(self,master):
        self.root = master
        self.root.config()
        self.root.title('How to play the game?')
        self.root.geometry('600x600') #size of the window
        
        Introduction(self.root)  #initial page, the home page      
                
class Introduction():   #mainpage
    def __init__(self,master):
        
        self.master = master
        self.master.config()
        self.Introduction = tk.Frame(self.master,bg=bg_color,width=600, height=600)
        self.Introduction.pack()
        self.Introduction.pack_propagate(0)  # fixed size

        #title: the name of the game, color: yellow
        label1 = tk.Label(self.Introduction, text = "+CELLULAR SPACE+",font=('Verdana',font_size,'normal'),bg=bg_color, fg=font_color3)
        label1.pack(padx=5, pady=50)

        #text: introduction, color: purple
        label2 = tk.Label(self.Introduction, text = " This is a Man vs. Machine interactive tangible simulation \n game based on a discrete model of cellular automaton \n and inspired by British mathematician John Conway’s Life. ",
                          font=('Verdana',font_size,'normal'),bg=bg_color, fg=font_color2, height = 10)
        label2.pack(pady=20)

        #guide, color: green
        label3 = tk.Label(self.Introduction, text = " Now click 'Next' to start the tutorial! ",
                          font=('Verdana',font_size,'normal'),bg=bg_color, fg=font_color)
        label3.pack(pady=1)

        #next
        button = tk.Button(self.Introduction,text='NEXT', font=('Verdana',font_size,'normal'), bg='gray',bd=0,command=self.goPageOne)
        button.pack(side='top',pady=40)
        
    def goPageOne(self,):    
        self.Introduction.destroy() #destroy the current page   
        PageOne(self.master)      
 
    
    
class PageOne():  
    def __init__(self,master):
        self.master = master
        self.master.config()
        self.PageOne = tk.Frame(self.master,bg=bg_color,width=600, height=600)
        self.PageOne.pack()
        self.PageOne.pack_propagate(0)

        #image
        label_img=tk.Label(self.PageOne,image= tkImage1,bd=20)
        label_img.pack(side='top',pady=20)

        #text
        label1 = tk.Label(self.PageOne, text = " In this orthogonal grid with algorithm driven cells,\n you will become a self-sufficiency cell attempting \n to move circumvent the dynamic group of alive cells by \n using tangible joystick to control the movement of \n your cell. don’t wait for the pattern become stable,\n because +CELLULAR SPACE+ will punish you! ",
                          font=('Verdana',font_size,'normal'),bg=bg_color, fg=font_color)
        label1.pack(side='top')

        button_frame=tk.Frame(self.PageOne,bg=bg_color)
        button_frame.pack(side='bottom',pady=20) 

        #go back
        button1 = tk.Button(button_frame,text='back',font=('Verdana',font_size,'normal'), bg='gray',bd=0,command=self.back)
        button1.pack(side='left',padx=20)
        #go next
        button1 = tk.Button(button_frame,text='next',font=('Verdana',font_size,'normal'), bg='gray',bd=0,command=self.nextPage)
        button1.pack(side='right',padx=20)


    def back(self):
        self.PageOne.destroy()
        Introduction(self.master)
        
    def nextPage(self):
        self.PageOne.destroy()
        PageTow(self.master)
 
class PageTow():  
    def __init__(self,master):
        self.master = master
        self.master.config()
        self.PageTow = tk.Frame(self.master,bg=bg_color,width=600, height=600)
        self.PageTow.pack()
        self.PageTow.pack_propagate(0)

        #image
        label_img=tk.Label(self.PageTow,image= tkImage2, bd=20)
        label_img.pack(side='top',pady=20)

        #text
        label1 = tk.Label(self.PageTow, text = " Three modes (easy, mid, hard) are provided for you \n with different speeds of cellular reproduction. \n Before the next iteration, the blinking cells indicate the \n position where new alive cells will be reproduced soon.\n The blinking cells will help you to foreseen the next \nfew minutes and help you to decide your next movement. ",
                          font=('Verdana',font_size,'normal'),bg=bg_color, fg=font_color)
        label1.pack(side='top')
        
        button_frame=tk.Frame(self.PageTow,bg=bg_color)
        button_frame.pack(side='bottom',pady=20)

        #go back
        button1 = tk.Button(button_frame,text='back',font=('Verdana',font_size,'normal'), bg='gray',bd=0,command=self.back)
        button1.pack(side='left',padx=20)
        #go next
        button1 = tk.Button(button_frame,text='next',font=('Verdana',font_size,'normal'), bg='gray',bd=0,command=self.nextPage)
        button1.pack(side='right',padx=20)


    def back(self):
        self.PageTow.destroy()
        PageOne(self.master)
        
    def nextPage(self):

        self.PageTow.destroy()
        PageThree(self.master)
        

class PageThree():  
    def __init__(self,master):
        self.master = master
        self.master.config()
        self.PageThree = tk.Frame(self.master,bg=bg_color,width=600, height=600)
        self.PageThree.pack()
        self.PageThree.pack_propagate(0)

        #serial 
        self.ser=serial.Serial(serialPort,baudRate,timeout=0.5)  

        #text
        label1 = tk.Label(self.PageThree, text = " Don’t be too scared! You will have three chances \n to achieve the destination! Your health bar will be shown as LED light. ",
                          font=('Verdana',font_size,'normal'),bg=bg_color, fg=font_color)
        label1.pack(side='top',pady=30)
        label2 = tk.Label(self.PageThree, text = " Look at the LED on your left hand side, that is the health bar. \n now try to click the botton see what happen!",
                          font=('Verdana',font_size,'normal'),bg=bg_color, fg=font_color2)
        label2.pack(side='top',pady=30)
        
        def change():
            global count
            count=count+1        
            if count==5:
                count=1
            print(count)
            button_change['text']=button_list[count]
            if count == 0:
                self.ser.write(b'3')
                change_label['text']='click me' #the text below the button 
            elif count==1: 
                self.ser.write(b'3')
                change_label['text']='what if I touch an alive cell?' #change the text
            elif count==2:
                self.ser.write(b'2')
                change_label['text']='what if I touch it again?'
            elif count==3:
                self.ser.write(b'1')
            elif count==4:
                self.ser.write(b'0')
                change_label['text']='you fail'
            
    
        
        self.ser.write(b'3') 
        button_change = tk.Button(self.PageThree, text='click me!', font=('Verdana',font_size,'normal'),width=30, bg='gray', bd=0 , command=change)
        button_change.pack(side='top',pady=20)

        #the text below the button
        change_label = tk.Label(self.PageThree, text='click to start the game',font=('Verdana',font_size,'normal'),bg=bg_color, fg=font_color)
        change_label.pack(side='top')
        
        button_frame=tk.Frame(self.PageThree,bg=bg_color)
        button_frame.pack(side='bottom',pady=20)

        #go back
        button1 = tk.Button(button_frame,text='back',font=('Verdana',font_size,'normal'), bg='gray',bd=0,command=self.back)
        button1.pack(side='left',padx=20)
        #go next
        button1 = tk.Button(button_frame,text='next',font=('Verdana',font_size,'normal'), bg='gray',bd=0,command=self.nextPage)
        button1.pack(side='right',padx=20)


    def back(self):
        global count
        count = 0 #recalculate if go back
        self.ser.close()
        self.PageThree.destroy()
        PageTow(self.master)
        
    def nextPage(self):
        global count
        count = 0 #recalculate if go next
        self.ser.close()
        self.PageThree.destroy()
        PageFour(self.master)


class PageFour():  
    def __init__(self,master):
        self.master = master
        self.master.config()
        self.PageFour = tk.Frame(self.master, bg=bg_color,width=600, height=600 )
        self.PageFour.pack()
        self.PageFour.pack_propagate(0)
        
        label1 = tk.Label(self.PageFour, text = "Now let’s start!",
                          font=('Verdana',30,'bold'),bg=bg_color, fg=font_color)
        label1.pack(side='top',pady=60 )
        
        
        button_frame=tk.Frame(self.PageFour,bg=bg_color)
        button_frame.pack(side='bottom',pady=20)

        #go back
        button1 = tk.Button(button_frame,text='back',font=('Verdana',font_size,'normal'), bg='gray',bd=0,command=self.back)
        button1.pack(side='left',padx=20)
        #go to home page
        button1 = tk.Button(button_frame,text='home page',font=('Verdana',font_size,'normal'), bg='gray',bd=0,command=self.nextPage)
        button1.pack(side='right',padx=20)

    def back(self):
        self.PageFour.destroy()
        PageThree(self.master)
        
    def nextPage(self):
        self.PageFour.destroy()
        Introduction(self.master)


if __name__=="__main__":
    
    pilImage1 = Image.open("1.jpg")   # read img
    pilImage1= pilImage1.resize((400, 300))
    
    pilImage2 = Image.open("2.jpg")  
    pilImage2= pilImage2.resize((400, 300))

    root = tk.Tk()
    
    tkImage1 = ImageTk.PhotoImage(image=pilImage1)
    tkImage2 = ImageTk.PhotoImage(image=pilImage2)

    Base(root)
    root.mainloop()



