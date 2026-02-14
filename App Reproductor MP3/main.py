from tkinter import Button, Label,Tk,filedialog, ttk, Frame, PhotoImage
import pygame
import mutagen

pygame.mixer.init()
pygame.mixer.init(frequency=44100)
cancion_actual =''
direcion = ''

def abrir_archivo():
	global direcion, pos, n,cancion_actual
	pos = 0
	n = 0
	direcion = filedialog.askopenfilenames(initialdir ='/', 
											title='Escoger la cancion(es)', 
										filetype=(('mp3 files', '*.mp3*'),('All files', '*.*')))
	n = len(direcion)
	cancion_actual = direcion[pos]

	nombre_cancion = cancion_actual.split('/')
	nombre_cancion = nombre_cancion[-1]

lista = []
for i in range(50,200,10):
	lista.append(i)

def iniciar_reproduccion():
	global cancion_actual, direcion, pos, n, actualizar

	cancion_actual = direcion[pos]
	nombre_cancion = cancion_actual.split('/')
	nombre_cancion = nombre_cancion[-1]
	nombre['text']= nombre_cancion

	time = pygame.mixer.music.get_pos()
	x = int(int(time)*0.001)
	tiempo['value']= x  #posicion de la cancion

	y = float(int(volumen.get())*0.1)
	pygame.mixer.music.set_volume(y)
	nivel['text']= int(y*100)

	audio = mutagen.File(cancion_actual)	
	log = audio.info.length
	minutos, segundos = divmod(log, 60)

	minutos, segundos = int(minutos), int(segundos)
	tt = minutos*60 + segundos
	tiempo['maximum']= tt  # tiempo total de la cancion
	texto['text']= str(minutos) + ":" + str(segundos)
	
	actualizar = ventana.after(100 , iniciar_reproduccion)

	if x == tt:
		ventana.after_cancel(actualizar)
		texto['text']= "00:00"
		if pos != n:
			pos = pos + 1
			ventana.after(100 , iniciar_reproduccion)
			pygame.mixer.music.play()
		if pos == n:
			pos = 0

def iniciar():
	global cancion_actual
	pygame.mixer.music.load(cancion_actual)
	pygame.mixer.music.play()
	iniciar_reproduccion()

def retroceder():
	global pos,n
	if pos >0:
		pos = pos-1
	else:
		pos = 0
	cantidad['text'] = str(pos)+'/'+str(n)

def adelantar():
	global pos, n
	if pos == n-1:
		pos = 0
	else:
		pos = pos + 1
	cantidad['text'] = str(pos)+'/'+str(n)

def stop():
	global actualizar
	pygame.mixer.music.stop()
	ventana.after_cancel(actualizar)  

def pausa():
	global actualizar
	pygame.mixer.music.pause()
	ventana.after_cancel(actualizar)

def continuar():
	pygame.mixer.music.unpause()
	ventana.after(100 , iniciar_reproduccion)

ventana =Tk()
ventana.title('Reproductor MP3')
ventana.iconbitmap('icono.png')
ventana.config(bg='black')
ventana.resizable(0,0)

frame2 = Frame(ventana, bg='black', width=600, height=500)
frame2.grid(column=0,row=1, sticky='nsew')

frame1 = Frame(ventana, bg='black', width=600, height=50)
frame1.grid(column=0,row=1, sticky='nsew')

estilo1 = ttk.Style()
estilo1.theme_use('clam')
estilo1.configure("Horizontal.TProgressbar", foreground='red', background='black',troughcolor='DarkOrchid1',
																bordercolor='white',lightcolor='#970BD9', darkcolor='black')

tiempo = ttk.Progressbar(frame1, orient= 'horizontal', length = 390, mode='determinate',style="Horizontal.TProgressbar")
tiempo.grid(row=0, columnspan=8, padx=5)

texto = Label(frame1, bg='black', fg='green2', width=5)
texto.grid(row=0,column=8)

nombre = Label(frame1, bg='black', fg='white', width=55)
nombre.grid(column=0, row=1, columnspan=8, padx=5)

cantidad = Label(frame1, bg='black', fg='green2')
cantidad.grid(column=8, row=1)

imagen1  = PhotoImage(file ='folder.png')
imagen2  = PhotoImage(file ='play.png')
imagen3  = PhotoImage(file ='pause.png')
imagen4 = PhotoImage(file ='repeat.png')
imagen5 = PhotoImage(file ='stop.png')
imagen6 = PhotoImage(file ='prev.png')
imagen7 = PhotoImage(file ='next.png')

boton1 = Button(frame1, image= imagen1, command= abrir_archivo)
boton1.grid(column=0, row=2, pady=10)

boton2 = Button(frame1, image= imagen2, bg='green', command=iniciar)
boton2.grid(column=2, row=2, pady=10)

boton3 = Button(frame1,image= imagen3, bg='red', command=stop)
boton3.grid(column=3, row=2, pady=10)

boton4 = Button(frame1,image= imagen4, bg='blue', command=pausa)
boton4.grid(column=5, row=2, pady=10)

boton5 = Button(frame1, image= imagen5, bg='blue2',command=continuar)
boton5.grid(column=6, row=2, pady=10)

atras = Button(frame1, image= imagen6, bg='yellow',command= retroceder)
atras.grid(column=1, row=2, pady=10)

adelante = Button(frame1, image= imagen7, bg='yellow',command=adelantar)
adelante.grid(column=4, row=2, pady=10)

volumen = ttk.Scale(frame1, to = 10, from_ =0, orient='horizontal',length=90, style= 'Horizontal.TScale')
volumen.grid(column=7, row=2)

style = ttk.Style()
style.configure("Horizontal.TScale", bordercolor='green2', troughcolor='black', background= 'green2', 
	foreground='green2',lightcolor='green2',darkcolor='black')  

nivel = Label(frame1, bg='black', fg='green2', width=3)
nivel.grid(column=8,row=2)

ventana.mainloop()