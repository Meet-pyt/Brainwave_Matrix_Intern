from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import sqlite3
import os
import email_pass
import smtplib
import time
class Login_System:
    def __init__(self,root):
        self.root=root
        self.root.title("Login System | GUI Interfce| Webcode")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#fafafa")
        #===Variables===#
        self.employeeId=StringVar()
        self.password=StringVar()
        self.var_otp=StringVar()
        self.var_new_pass=StringVar()
        self.var_conf_pass=StringVar()
        self.otp=''

        #====Images===#
        self.phone_image=ImageTk.PhotoImage(file='images/phone.png')
        self.lbl_phone_image=Label(self.root,image=self.phone_image,bd=0).place(x=200,y=50)

        #===Login Frame===#
        login_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        login_frame.place(x=650,y=90,width=350,height=460)

        title=Label(login_frame,text="Login System",font=("Elephant",30,"bold"),bg="white").place(x=0,y=30,relwidth=1)

        lbl_empid=Label(login_frame,text="Employee ID",font=("Andalus",15),bg="white",fg="#767171").place(x=50,y=100)
        txt_employeeId=Entry(login_frame,textvariable=self.employeeId,font=("times new roman",15),bg="#ECECEC").place(x=50,y=140,width=250)

        lbl_pass=Label(login_frame,text="Password",font=("Andalus",15),bg="white",fg="#767171").place(x=50,y=200)
        txt_pass=Entry(login_frame,textvariable=self.password,show="*",font=("times new roman",15),bg="#ECECEC").place(x=50,y=240,width=250)

        btn_login=Button(login_frame,command=self.login,text="Log In",cursor="hand2",font=("Arial Rounded MT Bold",15),bg="#00B0F0",activebackground="#00B0F0",fg="white",activeforeground="white").place(x=50,y=300,width=250,height=35)

        hr=Label(login_frame,bg="lightgray").place(x=50,y=370,width=250,height=2)

        or_=Label(login_frame,text="OR",bg="white",fg="lightgray",font=("times new roman",15,"bold")).place(x=150,y=355)

        btn_forget=Button(login_frame,text="Forget Password?",command=self.forgot_window,font=("times new roman",13),bg="white",fg="#00759E",bd=0,cursor="hand2",activebackground="white",activeforeground="#00759E").place(x=100,y=390)
        

        #===Animation Image===#
        self.im1=ImageTk.PhotoImage(file="images/im1.png")
        self.im2=ImageTk.PhotoImage(file="images/im2.png")
        self.im3=ImageTk.PhotoImage(file="images/im3.png")

        self.lbl_change_image=Label(self.root,bg="white")
        self.lbl_change_image.place(x=367,y=153,width=240,height=428)

        self.animate()
#=====================ALL FUNCTIONS=====================================================================================================================================================================================================================#
    def animate(self):
        self.im=self.im1
        self.im1=self.im2
        self.im2=self.im3
        self.im3=self.im
        self.lbl_change_image.config(image=self.im)
        self.lbl_change_image.after(2000,self.animate)



    def login(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.employeeId.get()=="" or self.password.get()=="":
                messagebox.showerror('Error',"All fileds are required",parent=self.root)
            else:
                cur.execute("select utype from employee where eid=? AND pass=?",(self.employeeId.get(),self.password.get()))
                user=cur.fetchone()
                if user==None:
                    messagebox.showerror('Error',"Invalid USERNAME/PASSWORD",parent=self.root)
                else:
                    if user[0]=="Admin":
                        self.root.destroy() 
                        os.system("python dashborad.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def forgot_window(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.employeeId.get()=="":
                messagebox.showerror('Error',"Employee ID must be requried",parent=self.root)
            else:
                cur.execute("select email from employee where eid=?",(self.employeeId.get(),))
                email=cur.fetchone()
                if email==None:
                    messagebox.showerror('Error',"Invalid Employee ID ,try again!!!",parent=self.root)
                else:
                    chk=self.send_email(email[0])
                    if chk=='f':
                        messagebox.showerror("Error","Connecton Error,try after some time!!!",parent=self.root)
                    else:
                        self.forgot_win=Toplevel(self.root)
                        self.forgot_win.title('RESET PASSWORD')
                        self.forgot_win.geometry('400x350+500+100')
                        self.forgot_win.focus_force()

                        title=Label(self.forgot_win,text='Reset Password',font=('goudy old style',15,"bold"),bg="#3f51b5",fg="white").pack(side=TOP,fill=X)
                        lbl_reset=Label(self.forgot_win,text="Enter OTP sent on Registerd Email",font=("times new roman",15)).place(x=20,y=60)
                        txt_reset=Entry(self.forgot_win,textvariable=self.var_otp,font=("times new roman",15),bg="lightyellow").place(x=20,y=100,width=250,height=30)

                        self.btn_reset=Button(self.forgot_win,text="SUBMIT",command=self.validate_otp,cursor="hand2",font=("times new roman",15),bg="lightblue")
                        self.btn_reset.place(x=280,y=100,width=100,height=30)


                        lbl_new_pass=Label(self.forgot_win,text="New Password",font=("times new roman",15)).place(x=20,y=160)
                        txt_new_pass=Entry(self.forgot_win,textvariable=self.var_new_pass,font=("times new roman",15),bg="lightyellow").place(x=20,y=190,width=250,height=30)

                        lbl_conf_pass=Label(self.forgot_win,text="Confirm Pasword",font=("times new roman",15)).place(x=20,y=225)
                        txt_conf_pass=Entry(self.forgot_win,textvariable=self.var_conf_pass,font=("times new roman",15),bg="lightyellow").place(x=20,y=255,width=250,height=30)

                        self.btn_update=Button(self.forgot_win,text="UPDATE",command=self.update_password,cursor="hand2",state=DISABLED,font=("times new roman",15),bg="lightblue")
                        self.btn_update.place(x=150,y=300,width=100,height=30)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


    def update_password(self):
        if self.var_new_pass.get()=="" or self.var_conf_pass.get()=="":
            messagebox.showerror('Error',"Password is required!!!",parent=self.forgot_win)
        elif self.var_new_pass.get()!=self.var_conf_pass.get():
            messagebox.showerror('Error',"New password And Confirm password should be same",parent=self.forgot_win)
        else:
            con=sqlite3.connect(database=r'ims.db')
            cur=con.cursor()
            try:
                cur.execute("Update employee SET pass=? where eid=?",(self.var_new_pass.get(),self.employeeId.get()))
                con.commit()
                messagebox.showinfo('Success',"Password Updated Successfully",parent=self.forgot_win)
                self.forgot_win.destroy()
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


    def validate_otp(self):
        if int(self.otp)==int(self.var_otp.get()):
            self.btn_update.config(state=NORMAL)
            self.btn_reset.config(state=DISABLED)
        else:
            messagebox.showerror('Error',"Invalid OTP, Try Again!!!",parent=self.forgot_win)
        

    def send_email(self,to_):
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        email_= email_pass.email_
        pass_=email_pass.pass_

        s.login(email_,pass_)

        self.otp=int(time.strftime("%H%M%S"))+int(time.strftime("%S"))

        subj='IMS-Reset Password OTP'
        msg=f'Dear Sir/Mam,\n\nYour Reset OTP is {str(self.otp)}.\n\nWith Regards,\nIMS Team'
        msg="Subject:{}\n\n{}".format(subj,msg)
        s.sendmail(email_,to_,msg)
        chk=s.ehlo()
        if chk[0]==250:
            return 's'
        else:
            return 'f'
    
root=Tk()
obj=Login_System(root)
root.mainloop()