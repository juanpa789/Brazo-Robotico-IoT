#####Robot SCARA bajo el entorno IoT#########
#############################################
Anexo B Código fuente Python en Raspberry pi.
from dash import Dash, html, Input, Output, ctx, dcc
import numpy as np
import plotly.express as px
import time
import RPi.GPIO as GPIO
import math
import time
from RpiMotorLib import RpiMotorLib

app = Dash(__name__)
######paramentros del robot##################
#############################################
L1 = 89.2
L2 = 89.2
x1=0
y1=0
x=[]
y=[]
#############################################
#grafica
###area de trabajo
for i in range(0,100): # media vuelta
    for j in range(0,200): #una vuelta
        q2 = i*1.8 - 90 # desde -90 hasta 90 para completar 2 cuadrantes
        q3 = j*1.8 - 90        
        q2=q2*math.pi/180
        q3=q3*math.pi/180
        x1 = L1*math.cos(q2) + L2*math.cos(q3) 
        y1 = L1*math.sin(q2) + L2*math.sin(q3) 
        x1 = int(x1)
        y1 = int(y1) 
        if x1 > 59:   
           x1=round(x1)  #redondeo a un decimal
           y1=round(y1)  #redondeo a un decimal
           x.append(x1)   #colocar datos en lista
           y.append(y1)   #colocar datos en lista
#mostrar figura
fig = px.scatter(x=x,y=y)
fig.update_traces(marker_size=3)
################################
app.layout = html.Div([
        html.H3('ROBOT TIPO SCARA'),
        dcc.Graph(id='Graph1',figure=fig,style={"width": "40%"}), 
        html.P("X1"), 
        dcc.Input(id="xv1", type="number", min="60", max="178", step="1", value="178"),
        html.P("X2"), 
        dcc.Input(id="xv2", type="number", min="60", max="178", step="1", value="178"),
        html.P("Nro de Ciclos:"), 
        dcc.Input(id="ciclo", type="number", min="1", max="5", step="1", value="1"),
        html.Button('INICIAR', id='iniciar', n_clicks=0),
        html.Div(children="callback not executed", id="output"),
        html.Div(children="callback not executed", id="output1"),
        
        html.Div([
        html.P("Y1"),
  
        dcc.Dropdown(id='yv1',
        options = [],
        placeholder = "intr.. Y1",
        multi = True,
        value = [],
        style={"width": "30%"}),
        html.P("Y2"),
        
        dcc.Dropdown(id='yv2',
        options = [],
        placeholder = "intr.. Y2",
        multi = True,
        value = [],
        style={"width": "30%"}),
        
        html.P("Z1"),
        dcc.Input(id="zv1", type="number", min="-100", max="0", step="5", value="0"),
        html.P("Z2"),
        dcc.Input(id="zv2", type="number", min="-100", max="0", step="5", value="0"),
        ],style= {'display': 'none'})
        ])   
        
@app.callback(
    Output("output", "children"),
    Input("xv1", "value"),
    Input("xv2", "value"),
)
def inicio(xv1,xv2):

 df = [x,y]
 df = np.asarray(df)
 df1 = np.array(x)
 a = np.where(df1 == int(xv1))
 a = np.asarray(a)
 tam = np.shape(a)
 tam = np.asarray(tam)
 ndr = tam[1]
    
 a2 = np.where(df1 == int(xv2))
 a2 = np.asarray(a2)
 tam2 = np.shape(a2)
 tam2 = np.asarray(tam2)
 ndr2 = tam2[1]
 
 q=[]
 q2=[]           
 for j in range(ndr2):
    qwe = df[1,a2[0,j]]
    q2.append(qwe)
    q2 = set(q2)
    q2 = sorted(q2)
 
 for i in range(ndr):
    qwe = df[1,a[0,i]]
    q.append(qwe)
    q = set(q)
    q = sorted(q)    
    
 return html.Div([
        
        html.P("Y1"),
        
        dcc.Dropdown(id='yv1',
        options = q ,
        placeholder = "intr.. Y1",
        value = q[0],
        style={"width": "30%"}),
        html.P("Y2"),
        
        dcc.Dropdown(id='yv2',
        options = q2 ,
        placeholder = "intr.. Y2",
        value = q2[0],
        style={"width": "30%"}),
        
        html.P("Z1"),
        dcc.Input(id="zv1", type="number", min="-100", max="0", step="5", value="0"),
        html.P("Z2"),
        dcc.Input(id="zv2", type="number", min="-100", max="0", step="5", value="0"),
        html.P(msg),       
        ])
        
@app.callback(
    Output("output1", "children"),
    Input("xv1", "value"),
    Input("xv2", "value"),
    Input("yv1", "value"),
    Input("yv2", "value"),
    Input("zv1", "value"),
    Input("zv2", "value"),
    Input("ciclo", "value"),
    Input("iniciar", "n_clicks"),
)
#####algoritmo de funcionamiento
def proceso(xv1,xv2,yv1,yv2,zv1,zv2,ciclo,iniciar):
 asd = ["PROCESO STAND BY"] #sin moviemiento
 if "iniciar" == ctx.triggered_id:
####declaracion de pines
#define GPIO pins
    GPIO_pins = (14, 15, 18)
#variable articular q1 (z)
    direction1 = 17
    step1 = 27
#variable articular q2
    direction2 = 20       # Direction -> GPIO Pin
    step2 = 21      # Step -> GPIO Pin
#variable articular q3
    direction3 = 5
    step3 = 6
######################
#pin electroiman
    ELE = 25
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ELE, GPIO.OUT)
#Inicializando en 0
    GPIO.output(ELE, GPIO.LOW)
#datos y parametros del brazo
#dimensiones de los eslabones
    L1 = 89.2 # eslabon 1 en mm
    L2 = 89.2   # eslabon 2 en mm
###################################
    mymotortest1 = RpiMotorLib.A4988Nema(direction1, step1, GPIO_pins, "A4988")
    mymotortest2 = RpiMotorLib.A4988Nema(direction2, step2, GPIO_pins, "A4988")
    mymotortest3 = RpiMotorLib.A4988Nema(direction3, step3, GPIO_pins, "A4988")
################################
    x = xv1
    y = yv1
    z = zv1
    #como los datos llegan en tipo str convertimos a int para operar con ellos
    x = int(x)
    y = int(y)
    z = int(z)
    #datos para p2
    x2 = xv2
    y2 = yv2
    z2 = zv2
    #como los datos llegan en tipo str convertimos a int para operar con ellos
    x2 = int(x2)
    y2 = int(y2)
    z2 = int(z2)
    
    numerov = ciclo

    print("x =",x)
    print("y =",y)
    print("z =",z)
    
    print("x2 =",x2)
    print("y2 =",y2)
    print("z2 =",z2)
    ##########################################
    #cinemtica directa para p1
    #calculo de parametros del robot x y
    D = (x*x+y*y+L1*L1-L2*L2)/(2*L1*(x*x+y*y)**(1/2))
    print("D =",D)
    print("parte1 de q2 =",math.atan2(y,x))
    print("numeredor =",(1-D*D)**(1/2))
    
    if (y>0):
         
        q2 = math.atan2(y,x)-math.atan2(((1-D*D)**(1/2)),D)
    else:
        q2 = math.atan2(y,x)-math.atan2((-(1-D*D)**(1/2)),D)
    
    q3 = math.atan2((y-L1*math.sin(q2)),(x-L1*math.cos(q2)))
    ##########################################
    #calculos de parametros cinematica inversa
    q1 = 45*z # 360 grdos/8 mm (husillo 8 mm por revolucion)
    p1 = q1/1.8 # pasos del motor
    #conversion de radianes a grados 
    q2 = q2*180/math.pi
    p2 = q2/1.8 # pasos segundo parametro
    #para la tercera varible articular
    q3 = q3*180/math.pi  
    p3 = q3/1.8 
    ##########################################
    #cinemtica directa para p2
    #calculo de parametros del robot x y
    D2 = (x2*x2+y2*y2+L1*L1-L2*L2)/(2*L1*(x2*x2+y2*y2)**(1/2))
    
    if (y2>0):
    
        q20 = math.atan2(y2,x2)-math.atan2(((1-D2*D2)**(1/2)),D2)
    else:    
        q20 = math.atan2(y2,x2)-math.atan2((-(1-D2*D2)**(1/2)),D2)
    
    q30 = math.atan2((y2-L1*math.sin(q20)),(x2-L1*math.cos(q20)))
    
    ##########################################
    #calculos de parametros cinematica inversa
    q10 = 45*z2 # 360 grdos/8 mm (husillo 8 mm por revolucion)
    p10 = q10/1.8 # pasos del motor
    #conversion de radianes a grados 
    q20 = q20*180/math.pi
    p20 = q20/1.8 # pasos segundo parametro
    #para la tercera varible articular
    q30 = q30*180/math.pi  
    p30 = q30/1.8
    
    #sentido de giro para las variables articulares deacuerdo a los puntos trazados
    #para P1    
    # q2 ----> q3 ----> q1
    print("")
    print("iniciando")
    time.sleep(1.1)
    
    if (p2>0):
        #print("para P1 EJECUTANDO q2")
        mymotortest2.motor_go(True, "Full" , round(p2/0.3149), .002, False, .05)
    else: 
        mymotortest2.motor_go(False, "Full" , round(abs(p2/0.3149)), .002, False, .05) 
        #print("para P1 EJECUTANDO q2")
    #tiempo entre eslabones
    time.sleep(0.5)
    #######################
    if (p3>0):
        mymotortest3.motor_go(False, "Full" , round(p3/0.3149), .002, False, .05)
    else: 
        mymotortest3.motor_go(True, "Full" , round(abs(p3/0.3149)), .002, False, .05)
    #tiempo entre eslabones
    time.sleep(0.5)
    
    if (p1>0):
        mymotortest1.motor_go(True, "Full" , round(p1), .002, False, .05)
    else: 
        mymotortest1.motor_go(False, "Full" , round(abs(p1)), .002, False, .05)        
    
    for i in range(int(numerov)):
          
          print("posicion P1")
          
          time.sleep(0.7)
          #activar el electroiman E = 1
          GPIO.output(ELE, GPIO.HIGH)
          #############################
          time.sleep(0.7)
    
          # q100 ----> q200 ----> q300 : PARA P2
          #operaciones para el segundo movimiento para pasar de P1 a P2
          p100 = p10 - p1
          p200 = p20 - p2
          p300 = p30 - p3
          
          #time.sleep(0.5)
          if (z > z2):
              if (p200>0):
                  mymotortest2.motor_go(True, "Full" , round(p200/0.3149), .002, False, .05)
              else: 
                  mymotortest2.motor_go(False, "Full" , round(abs(p200/0.3149)), .002, False, .05)         
              time.sleep(0.5)
          
              if (p300>0):
                  mymotortest3.motor_go(False, "Full" , round(p300/0.3149), .002, False, .05)
              else: 
                  mymotortest3.motor_go(True, "Full" , round(abs(p300/0.3149)), .002, False, .05)
              time.sleep(0.5)
              
              if (p100>0):
                  mymotortest1.motor_go(True, "Full" , round(p100), .002, False, .05)
              else: 
                  mymotortest1.motor_go(False, "Full" , round(abs(p100)), .002, False, .05)
          else:
          
          
              if (p100>0):
                  mymotortest1.motor_go(True, "Full" , round(p100), .002, False, .05)
              else: 
                  mymotortest1.motor_go(False, "Full" , round(abs(p100)), .002, False, .05)              
          
              time.sleep(0.5)
          
              if (p200>0):
                  mymotortest2.motor_go(True, "Full" , round(p200/0.3149), .002, False, .05)
              else: 
                  mymotortest2.motor_go(False, "Full" , round(abs(p200/0.3149)), .002, False, .05)             
          
              time.sleep(0.5)
          
              if (p300>0):
                  mymotortest3.motor_go(False, "Full" , round(p300/0.3149), .002, False, .05)
              else: 
                  mymotortest3.motor_go(True, "Full" , round(abs(p300/0.3149)), .002, False, .05)
          
          print("posicion P2")
          
          time.sleep(0.7)
          #activar el electroiman E = 0
          #print("electroiman desactivado")
          GPIO.output(ELE, GPIO.LOW)
          #############################
          time.sleep(0.7)
          if (i != int(numerov)-1):
              #volviendo a P1
              # -q100 ----> -q200 ----> -q300
              if (z < z2):
                  if (p200>0):
                      mymotortest2.motor_go(False, "Full" , round(p200/0.3149), .002, False, .05)
                  else:
                      mymotortest2.motor_go(True, "Full" , round(abs(p200/0.3149)), .002, False, .05)    
                  
                  time.sleep(0.5)
                  
                  if (p300>0):
                      mymotortest3.motor_go(True, "Full" , round(p300/0.3149), .002, False, .05)
                  else: 
                      mymotortest3.motor_go(False, "Full" , round(abs(p300/0.3149)), .002, False, .05)
              
                  time.sleep(0.5)
                  
                  if (p100>0):
                      mymotortest1.motor_go(False, "Full" , round(p100), .002, False, .05)
                  else: 
                      mymotortest1.motor_go(True, "Full" , round(abs(p100)), .002, False, .05)
                 
              else:        
                      
                  if (p100>0):
                      mymotortest1.motor_go(False, "Full" , round(p100), .002, False, .05)
                  else: 
                      mymotortest1.motor_go(True, "Full" , round(abs(p100)), .002, False, .05)              
              
                  time.sleep(0.5)
              
                  if (p200>0):
                      mymotortest2.motor_go(False, "Full" , round(p200/0.3149), .002, False, .05)
                  else: 
                      mymotortest2.motor_go(True, "Full" , round(abs(p200/0.3149)), .002, False, .05)
              
                  time.sleep(0.5)
              
                  if (p300>0):
                      mymotortest3.motor_go(True, "Full" , round(p300/0.3149), .002, False, .05)
                  else: 
                      mymotortest3.motor_go(False, "Full" , round(abs(p300/0.3149)), .002, False, .05)
    
    #al finalnizar los ciclos volvemos a la posicion inicial               
    # -q10 ----> -q20 ----> -q30
    time.sleep(0.5)
    
    if (p10>0):
        mymotortest1.motor_go(False, "Full" , round(p10), .002, False, .05)
    else: 
        mymotortest1.motor_go(True, "Full" , round(abs(p10)), .002, False, .05)       
    time.sleep(0.5)
    
    if (p20>0):
        mymotortest2.motor_go(False, "Full" , round(p20/0.3149), .002, False, .05)
    else: 
        mymotortest2.motor_go(True, "Full" , round(abs(p20/0.3149)), .002, False, .05)       
    time.sleep(0.5)
    
    if (p30>0):
        mymotortest3.motor_go(True, "Full" , round(p30/0.3149), .002, False, .05)
    else: 
        mymotortest3.motor_go(False, "Full" , round(abs(p30/0.3149)), .002, False, .05)
    
    print("posicion inicial")
    print("Proceso finalizado")
    asd = ["P1","(",xv1,",",yv1,",",zv1,")","P2","(",xv2,",",yv2,",",zv2,")"]
    return html.Div(asd)

if __name__ == '__main__':
    app.debug = True
    app.run_server(host="0.0.0.0")
