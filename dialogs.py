import sys
import hashlib
import webbrowser
import tkinter as tk
from tkinter import simpledialog, colorchooser, messagebox

from database import User, Score

is_windows = sys.platform == 'win32'
if is_windows:
    import winsound


class BaseDialog(simpledialog.Dialog):
    def __init__(self, parent, title, app=None):
        self.parent = parent
        if app:
            self.app = app

        super(BaseDialog, self).__init__(self.parent, title)

    def buttonbox(self):
        pass


class ChangePasswordDialog(BaseDialog):
    def __init__(self, parent, app):
        self.show_pass_state = tk.StringVar()
        self.old_password = tk.StringVar()
        self.new_password = tk.StringVar()
        self.confirm_pass = tk.StringVar()
        super(ChangePasswordDialog, self).__init__(parent, 'Change Password', app)

    def body(self, frame):
        tk.Label(frame, text='Old Password:').grid(row=0, column=1, pady=5)
        tk.Entry(frame, textvariable=self.old_password).grid(row=0, column=2, pady=5)

        tk.Label(frame, text='New Password:').grid(row=1, column=1, pady=5)
        tk.Entry(frame, show='*', textvariable=self.new_password).grid(row=1, column=2, pady=5)

        tk.Label(frame, text='Confirm password:').grid(row=2, column=0, columnspan=2, pady=5)
        self.confirm_pass_field = tk.Entry(frame, show='*', textvariable=self.confirm_pass)
        self.confirm_pass_field.grid(row=2, column=2, pady=5)

        self.show_pass_state.set('*')
        tk.Checkbutton(frame, text='Show password', variabl=self.show_pass_state, onvalue='', offvalue='*',
                       command=lambda *args: self.confirm_pass_field.config(show=self.show_pass_state.get())).grid(
            row=3, column=0, columnspan=2, pady=3)

        tk.Button(frame, text='Change Password', width=15, command=self.change_password).grid(row=3, column=2, pady=5)

        self.geometry('270x150')
        self.resizable(False, False)
        if is_windows:
            winsound.MessageBeep()

        return frame

    def change_password(self):
        old_password = self.old_password.get()
        new_password = self.new_password.get()
        confirm_pass = self.confirm_pass.get()
        if self.app.user.password == hashlib.sha256(old_password.encode()).hexdigest():
            if new_password == confirm_pass:
                new_password = hashlib.sha256(new_password.encode()).hexdigest()
                self.app.user.password = new_password
                self.app.user.save()
                messagebox.showinfo('Change Password', 'Your password successfully changed!')
            else:
                messagebox.showwarning('ERROR', 'Passwords not match!')
        else:
            messagebox.showwarning('ERROR', 'Your password is incorrect!')


class ChangeUsernameDialog(BaseDialog):
    def __init__(self, parent, app, variable=None):
        self.variable = variable  # variable for change username in manage account dialog after change username
        self.user_var = tk.StringVar()
        super(ChangeUsernameDialog, self).__init__(parent, 'Change Username', app)

    def body(self, frame):
        tk.Label(self, text='New Username:').place(x=20, y=15)
        tk.Entry(self, textvariable=self.user_var).place(x=115, y=17)
        tk.Button(self, text='Change', width=12, command=self.change_username).place(x=130, y=50)

        self.geometry('270x90')
        self.resizable(False, False)
        self.bind('<Return>', lambda _: self.change_username())
        if is_windows:
            winsound.MessageBeep()

        return frame

    def change_username(self):
        new_user = self.user_var.get()
        old_username = self.app.user.username
        if new_user.strip():
            if new_user != old_username:
                if self.variable:
                    self.variable.set(new_user)
                self.app.user.username = new_user
                self.app.user.save()
                messagebox.showinfo('Change Username', f'Your username changed from {old_username} to {new_user}')
            else:
                messagebox.showwarning('ERROR', "You can't change your username to the current username!")
        else:
            messagebox.showwarning('ERROR', 'Username field is empty!')


class ManageAccountDialog(BaseDialog):
    def __init__(self, parent, app):
        self.user_var = tk.StringVar()
        super(ManageAccountDialog, self).__init__(parent, 'Manage Account', app)

    def body(self, frame):
        self.user_var.set(self.app.user.username)
        if self.user_var.get() == 'Default':
            status = 'disabled'
        else:
            status = 'normal'

        tk.Label(frame, text='Username:').grid(row=0, column=1)
        tk.Label(frame, textvariable=self.user_var).grid(row=0, column=2)

        tk.Button(frame, text='Change username', state=status, width=15,
                  command=lambda: ChangeUsernameDialog(self.parent, self.app, self.user_var)).grid(
            row=1, column=3, pady=5)
        tk.Button(frame, text='Change password', state=status, width=15,
                  command=lambda: ChangePasswordDialog(self.parent, self.app)).grid(row=2, column=3, pady=5)
        tk.Button(frame, text='Reset scores', state=status, width=15,
                  command=self.reset_scores).grid(row=1, column=0, pady=5)
        tk.Button(frame, text='Delete account', state=status, width=15,
                  command=self.delete_account).grid(row=2, column=0, pady=5)

        self.resizable(False, False)
        if is_windows:
            winsound.MessageBeep()

        return frame

    def reset_scores(self):
        submit = messagebox.askokcancel('Reset Scores', 'Are you sure to reset all scores?')
        if submit:
            Score.delete().where(Score.user == self.app.user).execute()
            self.app.best_score.set(0)
            messagebox.showinfo('Reset Scores', 'Reset all your scores successfully!')

    def delete_account(self):
        submit = messagebox.askokcancel('Delete Account', 'Are you sure to delete your account?')
        if submit:
            User.delete().where(User.username == self.app.user.username).execute()
            self.app.change_user('Default')
            self.destroy()
            messagebox.showinfo('Delete account', 'Delete your account successfully!')

class SignupDialog(BaseDialog):
    def __init__(self, parent, app):
        self.show_pass_state = tk.StringVar()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.password.trace('w', lambda *args: self.check_confirm())
        self.confirm_pass = tk.StringVar()
        self.confirm_pass.trace('w', lambda *args: self.check_confirm())
        super(SignupDialog, self).__init__(parent, 'Sign up', app)

    def body(self, frame):
        tk.Label(frame, text='Username:').grid(row=0, column=1, pady=5)
        tk.Entry(frame, textvariable=self.username).grid(row=0, column=2, pady=5)

        tk.Label(frame, text='Password:').grid(row=1, column=1, pady=5)
        tk.Entry(frame, show='*', textvariable=self.password).grid(row=1, column=2, pady=5)

        tk.Label(frame, text='Confirm password:').grid(row=2, column=0, columnspan=2, pady=5)
        self.confirm_pass_field = tk.Entry(frame, show='*', textvariable=self.confirm_pass)
        self.confirm_pass_field.grid(row=2, column=2, pady=5)

        self.show_pass_state.set('*')
        tk.Checkbutton(frame, text='Show password', variabl=self.show_pass_state, onvalue='', offvalue='*',
                       command=lambda *args: self.confirm_pass_field.config(show=self.show_pass_state.get())).grid(
            row=3, column=0, columnspan=2, pady=3)

        self.state_label = tk.Label(frame)
        self.state_label.grid(row=3, column=2, pady=3)

        tk.Button(frame, text='Sign in', width=10, command=self.signin).grid(
            row=4, column=0, columnspan=2, pady=5)
        self.signup_btn = tk.Button(frame, text='Sign up', width=10, state='disabled', command=self.signup)
        self.signup_btn.grid(row=4, column=2, pady=5)

        self.geometry('270x180')
        self.resizable(False, False)
        if is_windows:
            winsound.MessageBeep()

        return frame

    def signup(self):
        username = self.username.get()
        password = self.password.get()
        password = hashlib.sha256(password.encode()).hexdigest()
        for user in User.select():
            if user.username == username:
                messagebox.showwarning('Invalid user!', 'User already exists!')
                break
        else:
            User(username=username, password=password, snake_head_color='black', snake_body_color='grey').save()
            messagebox.showinfo('Sign up', 'Your account successfully created! \nnow you most login')

    def check_confirm(self):
        password = self.password.get()
        confirm_password = self.confirm_pass.get()
        if password == confirm_password:
            self.state_label.config(text='match!', fg='green')
            self.signup_btn.config(state='normal')
        else:
            self.state_label.config(text='not match!', fg='red')
            self.signup_btn.config(state='disabled')

    def signin(self):
        self.destroy()
        SigninDialog(self.parent, self.app)


class SigninDialog(BaseDialog):
    def __init__(self, parent, app):
        self.user_var = tk.StringVar()
        self.pass_var = tk.StringVar()
        self.show_pass_state = tk.StringVar()
        super(SigninDialog, self).__init__(parent, 'Sign in', app)

    def body(self, frame):
        tk.Label(frame, text='Username:').grid(row=0, column=0, pady=5)
        tk.Entry(frame, textvariable=self.user_var).grid(row=0, column=1, pady=5)

        tk.Label(frame, text='Password:').grid(row=1, column=0, pady=5)
        self.pass_field = tk.Entry(frame, textvariable=self.pass_var, show='*')
        self.pass_field.grid(row=1, column=1, pady=5)
        self.show_pass_state.set('*')
        tk.Checkbutton(frame, text='Show password', variabl=self.show_pass_state, onvalue='', offvalue='*',
                       command=lambda *args: self.pass_field.config(show=self.show_pass_state.get())).grid(row=2,
                                                                                                           column=1,
                                                                                                           pady=5)

        tk.Button(frame, text='Sign up', width=10, command=self.signup).grid(row=3, column=0, pady=5)
        tk.Button(frame, text='Sign in', width=10, command=self.signin).grid(row=3, column=1, pady=5)

        self.geometry('250x150')
        self.resizable(False, False)
        if is_windows:
            winsound.MessageBeep()

        return frame

    def signin(self):
        username = self.user_var.get()
        password = self.pass_var.get()
        password = hashlib.sha256(password.encode()).hexdigest()
        try:
            user = User.get(username=username)
            if user.password == password:
                self.app.restart()
                self.app.change_user(user.username)
                messagebox.showinfo('Login', 'You successfully login!')

            else:
                messagebox.showwarning('Invalid password', 'Your password is incorrect!')

        except:
            messagebox.showwarning('Invalid user!', 'Please enter a valid user!')

    def signup(self):
        self.destroy()
        SignupDialog(self.parent, self.app)


class BestScoresDialog(BaseDialog):
    def __init__(self, parent, app):
        super(BestScoresDialog, self).__init__(parent, 'Best scores', app)

    def body(self, frame):
        list_box = tk.Listbox(frame)
        list_box.pack(side=tk.LEFT)
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        counter = 0

        for score in Score.select().where(Score.level == self.app.level.get()).order_by(Score.score.desc()):
            list_box.insert(tk.END, f' {score.user.username}: {score.score}')
            if counter > 20:
                break
            else:
                counter += 1

        list_box.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=list_box.yview)
        self.resizable(False, False)
        if is_windows:
            winsound.MessageBeep()

        return frame


class SettingDialog(BaseDialog):
    def __init__(self, parent, app):
        self.need_restart = False
        self.level_var = tk.IntVar()
        super(SettingDialog, self).__init__(parent, 'Setting', app)

    def body(self, frame):
        self.level_var.set(self.app.level.get())
        self.head_color = self.app.snake.color['head']
        self.body_color = self.app.snake.color['body']

        tk.Label(self, text='Level:').place(x=20, y=20)
        tk.Scale(self, from_=1, to=3, variable=self.level_var, orient=tk.HORIZONTAL).place(x=65, y=2)

        tk.Label(self, text='Snake Head Color:').place(x=25, y=55)
        self.head_color_btn = tk.Button(self, bg=self.head_color, width=2, command=self.set_head_color)
        self.head_color_btn.place(x=135, y=55)

        tk.Label(self, text='Snake Body Color:').place(x=25, y=95)
        self.body_color_btn = tk.Button(self, bg=self.body_color, width=2, command=self.set_body_color)
        self.body_color_btn.place(x=135, y=95)

        tk.Button(self, text='Reset', width=10, command=self.reset).place(x=15, y=145)
        tk.Button(self, text='Apply', width=10, command=self.apply).place(x=105, y=145)

        self.geometry('200x200')
        self.resizable(False, False)
        self.bind('<Return>', lambda _: self.apply())
        self.bind('<Escape>', lambda _: self.reset())
        if is_windows:
            winsound.MessageBeep()

        return frame

    def apply(self):
        if self.level_var.get() != self.app.level.get():
            self.need_restart = True

        if self.need_restart and messagebox.askokcancel(
                'Restart Game', 'Are you sure to restart the game?(score will saved)'):
            self.app.restart()
            self.app.set_level(self.level_var.get())
            self.app.update_best_score()

        self.app.snake.change_head_color(self.head_color)
        self.app.snake.change_body_color(self.body_color)
        self.app.user.snake_head_color = self.app.snake.color['head']
        self.app.user.snake_body_color = self.app.snake.color['body']
        self.app.user.save()

    def set_head_color(self):
        self.head_color = colorchooser.askcolor(initialcolor=self.head_color)[1]
        self.head_color_btn.config(bg=self.head_color)

    def set_body_color(self):
        self.body_color = colorchooser.askcolor(initialcolor=self.body_color)[1]
        self.body_color_btn.config(bg=self.body_color)

    def reset(self):
        self.head_color = self.app.snake.color['head']
        self.body_color = self.app.snake.color['body']
        self.head_color_btn.config(bg=self.head_color)
        self.body_color_btn.config(bg=self.body_color)
        self.level_var.set(self.app.level.get())


class AboutDialog(BaseDialog):
    def __init__(self, parent):
        super(AboutDialog, self).__init__(parent, 'About us')

    def body(self, frame):
        tk.Label(self, text='This game made by Sina.f & Mohammad Amini').pack(pady=12)
        grid_options = {'row': 1, 'padx': 15, 'pady': 15}

        sina_frame = tk.LabelFrame(self, text='Sina.f')
        sina_frame.pack(fill=tk.X, pady=5)
        tk.Button(sina_frame, text='GitHub', width=8,
                  command=lambda: webbrowser.open('https://github.com/sina-programer')).grid(column=1, **grid_options)
        tk.Button(sina_frame, text='Instagram', width=8,
                  command=lambda: webbrowser.open('https://www.instagram.com/sina.programer')).grid(column=2,
                                                                                                    **grid_options)
        tk.Button(sina_frame, text='Telegram', width=8,
                  command=lambda: webbrowser.open('https://t.me/sina_programer')).grid(column=3, **grid_options)

        mohammad_frame = tk.LabelFrame(self, text='Mohammad Amini')
        mohammad_frame.pack(fill=tk.X, pady=15)
        tk.Button(mohammad_frame, text='GitHub', width=8,
                  command=lambda: webbrowser.open('https://github.com/mohammadaminY')).grid(column=1, **grid_options)
        tk.Button(mohammad_frame, text='Instagram', width=8,
                  command=lambda: webbrowser.open('https://www.instagram.com/insta_id')).grid(column=2, **grid_options)
        tk.Button(mohammad_frame, text='Telegram', width=8,
                  command=lambda: webbrowser.open('https://t.me/tel_id')).grid(column=3, **grid_options)

        self.geometry('300x240')
        self.resizable(False, False)
        if is_windows:
            winsound.MessageBeep()

        return frame
