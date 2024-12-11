# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 14:29:03 2024

@author: SamuelBrambila
"""

from tkinter import *
import re

class aplicacion():
    def __init__(self):
        self.raiz = Tk()
        self.raiz.geometry('800x500')
        self.raiz.resizable(width=False,height=False)
        self.raiz.title('Expresiones regulares')
        label = Label(self.raiz,text="Validación de expresiones regulares")
        label.pack(side=TOP)
        
        self.textos = Frame(self.raiz)
        self.textos.pack(side=TOP)
        self.frameDeAbajo = Frame(self.raiz)
        self.frameDeAbajo.pack(side=BOTTOM)
        
        Label(self.textos, text="Dirección IPv4:").grid(row=0, column=0, padx=10, pady=5, sticky=W)
        Label(self.textos, text="Correo electrónico:").grid(row=1, column=0, padx=10, pady=5, sticky=W)
        Label(self.textos, text="Número de teléfono:").grid(row=2, column=0, padx=10, pady=5, sticky=W)
        Label(self.textos, text="Código postal:").grid(row=3, column=0, padx=10, pady=5, sticky=W)
        
        self.t1=Entry(self.textos,width=40)
        self.t1.grid(row=0,column=1,padx=10,pady=10)
        self.t2=Entry(self.textos,width=40)
        self.t2.grid(row=1,column=1)
        self.t3=Entry(self.textos,width=40)
        self.t3.grid(row=2,column=1)
        self.t4=Entry(self.textos,width=40)
        self.t4.grid(row=3,column=1)
        
        self.b1=Button(self.textos,text='Validar',command=lambda:self.validar(1))
        self.b1.grid(row=0,column=2,padx=10,pady=10)
        self.b2=Button(self.textos,text='Validar',command=lambda:self.validar(2))
        self.b2.grid(row=1,column=2,pady=10)
        self.b3=Button(self.textos,text='Validar',command=lambda:self.validar(3))
        self.b3.grid(row=2,column=2,pady=10)
        self.b4=Button(self.textos,text='Validar',command=lambda:self.validar(4))
        self.b4.grid(row=3,column=2,pady=10)
        
        self.l1=Label(self.textos,text='...')
        self.l1.grid(row=0,column=3)
        self.l2=Label(self.textos,text='...')
        self.l2.grid(row=1,column=3)
        self.l3=Label(self.textos,text='...')
        self.l3.grid(row=2,column=3)
        self.l4=Label(self.textos,text='...')
        self.l4.grid(row=3,column=3)
        
        # Text Area para contar palabras (función adicional)
        Label(self.textos, text="Ingrese texto para contar las palabras:").grid(row=4, column=0, padx=10, pady=5, sticky=W)
        self.text_area = Text(self.textos, height=5, width=40)
        self.text_area.grid(row=5, column=1, padx=10, pady=5)
        self.word_count_btn = Button(self.textos, text="Contar Palabras", command=self.contar_palabras)
        self.word_count_btn.grid(row=6, column=1, pady=10)
        self.word_count_label = Label(self.textos, text="Total palabras: 0")
        self.word_count_label.grid(row=6, column=2)

        # Checkboxes para negritas y cursivas (función adicional)
        self.bold_var = IntVar()
        self.italic_var = IntVar()
        self.bold_check = Checkbutton(self.textos, text="Negritas", variable=self.bold_var, command=self.aplicar_estilos)
        self.bold_check.grid(row=7, column=1, sticky=W)
        self.italic_check = Checkbutton(self.textos, text="Cursiva", variable=self.italic_var, command=self.aplicar_estilos)
        self.italic_check.grid(row=7, column=1, sticky=E)
        
        # Botones para cerrar ventana y limpiar lo ingresado en los campos de texto
        self.bsalir=Button(self.frameDeAbajo,text="Salir",command=self.raiz.destroy)
        self.bsalir.pack(side=LEFT, padx=10, pady=10)
        self.blimpiar=Button(self.frameDeAbajo,text="Limpiar",command=self.limpiar)
        self.blimpiar.pack(side=LEFT, padx=10, pady=10)
        
        self.raiz.mainloop()
        
    def limpiar(self):
        self.t1.delete(first=0, last='end')
        self.t2.delete(first=0, last='end')
        self.t3.delete(first=0, last='end')
        self.t4.delete(first=0, last='end')
        self.l1.config(fg='black', text='...')
        self.l2.config(fg='black', text='...')
        self.l3.config(fg='black', text='...')
        self.l4.config(fg='black', text='...')
        self.text_area.delete(1.0, 'end')
        self.word_count_label.config(text="Total palabras: 0")
        
    def validar(self,numero):
        if(numero==1):
            txtAValidar=self.t1.get()
            x=re.search("^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$",txtAValidar)
            if (x):
                self.l1.config(fg="green",text="IPv4 válida")
            else:
                self.l1.config(fg="red",text="IPv4 inválida")
        elif(numero==2):
            txtAValidar=self.t2.get()
            x=re.search("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$",txtAValidar)
            if (x):
                self.l2.config(fg="green",text="Correo válido")
            else:
                self.l2.config(fg="red",text="Correo inválido")
        elif(numero==3):
            txtAValidar=self.t3.get()
            x=re.search("^\\d{10}$",txtAValidar)
            if (x):
                self.l3.config(fg="green",text="Teléfono válido")
            else:
                self.l3.config(fg="red",text="Teléfono inválido")
        else:
            txtAValidar=self.t4.get()
            x=re.search("^\\d{5}$",txtAValidar)
            if (x):
                self.l4.config(fg="green",text="Código postal válido")
            else:
                self.l4.config(fg="red",text="Código postal inválido")
                
    def contar_palabras(self):
        # Contar palabras en el Text Area
        texto = self.text_area.get(1.0, END)
        palabras = len(texto.split())
        self.word_count_label.config(text=f"Total palabras: {palabras}")
        
    def aplicar_estilos(self):
        # Aplicar estilos a Entry
        bold = self.bold_var.get() == 1
        italic = self.italic_var.get() == 1
        
        # Estilo para el Entry
        if bold and italic:
            font_style = 'bold italic'
        elif bold:
            font_style = 'bold'
        elif italic:
            font_style = 'italic'
        else:
            font_style = 'normal'
        
        # Aplicar estilo a los Entry
        self.t1.config(font=(None, 10, font_style))
        self.t2.config(font=(None, 10, font_style))
        self.t3.config(font=(None, 10, font_style))
        self.t4.config(font=(None, 10, font_style))
        
        # Aplicar estilos al Text Area
        self.text_area.tag_configure('bold', font=('Helvetica', 10, 'bold'))
        self.text_area.tag_configure('italic', font=('Helvetica', 10, 'italic'))
        self.text_area.tag_configure('bold_italic', font=('Helvetica', 10, 'bold italic'))
        self.text_area.tag_configure('normal', font=('Helvetica', 10, 'normal'))
        
        # Determinar qué estilo aplicar en el Text Area
        self.text_area.tag_remove('bold', '1.0', 'end')
        self.text_area.tag_remove('italic', '1.0', 'end')
        self.text_area.tag_remove('bold_italic', '1.0', 'end')
        self.text_area.tag_remove('normal', '1.0', 'end')
        
        if bold and italic:
            self.text_area.tag_add('bold_italic', '1.0', 'end')
        elif bold:
            self.text_area.tag_add('bold', '1.0', 'end')
        elif italic:
            self.text_area.tag_add('italic', '1.0', 'end')
        else:
            self.text_area.tag_add('normal', '1.0', 'end')
            
app = aplicacion()