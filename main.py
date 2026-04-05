import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import re
import pdfplumber
class lesson:
    word = []
    _下标 = 0

    def create(self):
        # 获取文件路径
        f = filedialog.askopenfilename(title="选取PDF成绩单，本程序将计算绩点均分", filetypes=[("PDF", ".pdf")])
        # 检查用户是否选择了文件
        if not f:
            messagebox.showinfo("提示","没有选择文件")
            exit()
        try:
            with pdfplumber.open(f) as pdf:
                # 检查PDF文件是否有页面
                if len(pdf.pages) == 0:
                    messagebox.showinfo("提示","PDF文件没有页面")
                    exit()
                # 提取第一页的文本
                text = pdf.pages[0].extract_text()
        except Exception as e:
            messagebox.showinfo("提示",f"打开PDF时出错: {e}")
        pattern = r'.*?\s+\d+(?:\.\d+)?\s+(?:\d+|[\u4e00-\u9fa5]+)\s'
        matches = re.findall(pattern, text)
        f = open("cal.txt", "w", encoding="utf-8")
        for match in matches:
            if match[0] == "☆" or match[0] == "绩" or match[0] == "▲":
                continue
            line = match.strip()
            line = line.split(" ")
            if len(line) == 4:
                if "学年" in line[0]:
                    f.write(f"{line[1]} {line[2]} {line[3]}\n")
                    continue
                else:
                    f.write(f"{line[0]} {line[1]} {line[2]}\n")
                    continue
            if "\n" not in match:
                f.write(match+"\n")
            else:
                f.write(match)
        f.close()
    def find(self,n):
        i = 0
        for li in self.word:
            if li[0] == n:
                self._下标=i
                return True
            i += 1
        return False

    # 读取文件内容，以列表形式存储，打印
    def readlogin(self):
        i = 0
        try:
            f = open("cal.txt", "r", encoding="utf-8")
        except FileNotFoundError:
            self.create()
            f = open("cal.txt", "r", encoding="utf-8")
        l = f.readlines()
        f.close()
        for line in l:
            if line.isspace():
                return
            line = line.strip()
            line=line.split(" ")
            self.word.append(line)
            i += 1

    # 修改特定课程的学分，成绩等信息
    def change(self,str1,str2,str3):
        if not self.find(str1):
            messagebox.showinfo("提示","未找到对应课程")
        else:
            self.word[self._下标][0] = str1
            self.word[self._下标][1] = str2
            self.word[self._下标][2] = str3

    # 删除特定课程
    def dele(self,st):
        if not self.find(st):
            messagebox.showinfo("提示","未找到对应课程")
        else:
            self.word.remove(self.word[self._下标])
            messagebox.showinfo("提示","删除完成")

    # 添加课程
    def add(self,str1,str2,str3):
        if self.find(str1):
            messagebox.showinfo("提示", "课程已存在")
            return
        if str1=="" or str2=="" or str3==" "or str1.isspace() or str2.isspace() or str3.isspace() :
            messagebox.showinfo("提示", "课程信息不能为空")
            return
        lis = [str1, str2, str3]
        self.word.append(lis)
        messagebox.showinfo("提示","添加完成")

    def write(self):
        f = open("cal.txt", "w", encoding="utf-8")
        for li in self.word:
            f.write(li[0]+" " + li[1]+" " + li[2]+" " + "\n")
        f.close()

    def transf(self,n):
        dic={"优": 95, "良":85,"中":75,"及格":65,"不及格":0,"缺":0}
        num = dic.get(n,n)
        try:
            return float(num)#type:ignore
        except ValueError:
            return 0.0


    def checkscore(self, n):
        def a(x):
            if 6<=x<=9:
                return 0.8
            elif 3<=x<=5:
                return 0.5
            else:
                return 0
        num = self.transf(n)
        if num == 100:
            return 4.8
        elif num<60:
            return 0
        else:
            return int(num/10)-5+a(num%10)

    def cal(self):
        sumc = 0
        sumsc = 0
        sumj = 0
        for li in self.word:
            sumc += float(li[1])
            sumsc += float(li[1]) * self.transf(li[2])
            sumj += float(li[1]) * self.checkscore(li[2])
        messagebox.showinfo("计算结果",f"首修平均分：{sumsc / sumc:.3f}\n\n首修平均绩点：{sumj / sumc:.3f}")
item=lesson()
root=tk.Tk()
root.title("4.8绩点计算")
root.geometry("1000x500+300+200")

def show_details(event):
    E1.delete(0, tk.END)
    E2.delete(0, tk.END)
    E3.delete(0, tk.END)
    selected_item = listb.selection()[0]  # 获取当前选中的项
    item_data = listb.item(selected_item, 'values')  # 获取该项的值
    E1.insert(0,item_data[0])
    E2.insert(0, item_data[1])
    E3.insert(0, item_data[2])


def open_file():
    with open("cal.txt", 'r',encoding="UTF-8") as file:
        content.delete('1.0', tk.END)
        content.insert(tk.END, file.read())


def paste_text():
    clipboard_text = root.clipboard_get()
    content.insert(tk.END, clipboard_text)

def write_file():
    s = content.get("1.0", tk.END)
    if s.isspace():
        messagebox.showinfo("提示","操作违规")
        return
    with open("cal.txt", 'w',encoding="UTF-8") as file:
        file.write(s)
        content.delete('1.0',tk.END)
    upade()

def create_listbox(root, columns):
    listbox = ttk.Treeview(root, columns=columns, show='headings')
    for col in columns:
        listbox.heading(col, text=col)
        listbox.column(col, width=150, anchor='center')
    return listbox
def populate_listbox(listbox, rows):
    for row in rows:
        listbox.insert('', 'end', values=row)

columns = ['学科', '学分', '成绩']
listb = create_listbox(root, columns)
listb.bind('<ButtonRelease-1>',show_details)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=listb.yview)  # 创建纵向滚动条，绑定到TreeView的垂直滚动
scrollbar.pack(side="left",fill="y")
listb.config(yscrollcommand=scrollbar.set)
def upade():
    for it in listb.get_children():
        listb.delete(it)
    item.word.clear()
    item.readlogin()
    populate_listbox(listb, item.word)


def btnone():
    if E1.get().isspace():
        messagebox.showinfo("提示","课程信息不能为空")
        return
    item.dele(E1.get())
    item.write()
    upade()
    E1.delete(0, tk.END)
    E2.delete(0, tk.END)
    E3.delete(0, tk.END)


def btntwo():
    item.add(E1.get(),E2.get(),E3.get())
    item.write()
    upade()
    E1.delete(0, tk.END)
    E2.delete(0, tk.END)
    E3.delete(0, tk.END)


def btnthree():
    item.change(E1.get(),E2.get(),E3.get())
    item.write()
    upade()
    E1.delete(0, tk.END)
    E2.delete(0, tk.END)
    E3.delete(0, tk.END)
def a():
    item.create()
    upade()
upade()
listb.pack(side='left',fill='both')
L1 = ttk.Label(text="学科")
L1.pack()
L1.place(x=500,y=50)
E1 = ttk.Entry()
E1.pack()
E1.place(x=550,y=50)
L2 = ttk.Label(text="学分")
L2.pack()
L2.place(x=500,y=100)
E2 = ttk.Entry()
E2.pack()
E2.place(x=550,y=100)
L3 = ttk.Label(text="成绩")
L3.pack()
L3.place(x=500,y=150)
E3 = ttk.Entry()
E3.pack()
E3.place(x=550,y=150)
content = tk.Text(root, width=30,height=35)
content.pack(fill='y',expand=True)
content.place(x=800,y=0)
bar = ttk.Scrollbar(root, orient="vertical", command=content.yview)  # 创建纵向滚动条，绑定到TreeView的垂直滚动
bar.pack(side="right",fill="y")
content.config(yscrollcommand=bar.set)
btn1=ttk.Button(root,text="删除",command=btnone)
btn2=ttk.Button(root,text="添加",command=btntwo)
btn3=ttk.Button(root,text="修改",command=btnthree)
btn1.pack()
btn1.place(x=475,y=250)
btn2.pack()
btn2.place(x=575,y=250)
btn3.pack()
btn3.place(x=675,y=250)
paste_button = ttk.Button(root, text="粘贴", command=paste_text)
paste_button.pack()
paste_button.place(x=575,y=350)
menubar = tk.Menu(root)
root.config(menu=menubar)
file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="操作", menu=file_menu)
file_menu.add_command(label="打开文件", command=open_file)
file_menu.add_separator() # 添加分隔符
file_menu.add_command(label="保存文件", command=write_file)
file_menu.add_separator() # 添加分隔符
file_menu.add_command(label="计算", command=item.cal)
file_menu.add_separator() # 添加分隔符
file_menu.add_command(label="选取成绩单", command=a)
root.mainloop()
