from __future__ import division

import numpy as np

from bokeh.layouts import row, widgetbox
from bokeh.models import CustomJS, Slider
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models.widgets import Select


alfa = 0.5
beta = 0.5
r = 0.5
b = 0.5
k = 6

xx = np.linspace(0, 1, 100)
yy = np.linspace(0, 1, 100)

Y, X = np.meshgrid(xx, yy)

#Hacer la malla triangular
for i in range(0, len(xx)):
    for j in range(0, len(yy)):
        if X[i][j] + Y[i][j] > 1:
            X[i][j] = 0
            Y[i][j] = 0


x0 = X[::2, ::2].flatten()
y0 = Y[::2, ::2].flatten()

#Ecuaciones importantes
varX = r+(((1-alfa*y0)**k)-r)*x0 + (1-r-x0-y0)*y0
varY = (1-(1-alfa*y0)**k)*x0 + ((x0+y0)*(1-b)*(1-beta*x0)**k)*y0

xm = varX
ym = varY

dis = np.sqrt((xm-x0)**2+(ym-y0)**2)

x1 = (xm-x0)/(20*dis)+x0
y1 = (ym-y0)/(20*dis)+y0

source = ColumnDataSource(data=dict(x0=x0, y0=y0, x1=x1, y1=y1))

#Plot
plot = figure(x_range=(0, 1), y_range=(0, 1), x_axis_label='H', y_axis_label='C',
              title="Retrato de fases")
plot.segment('x0', 'y0', 'x1', 'y1', source=source, line_width=1)

# Función en JS que se activa cuando cambia el slider
callback = CustomJS(args=dict(source=source), code="""
    var data = source.data;
    var sel = select.value;
    var xm = [];
    var ym = [];
    var dis = [];
    x0 = data['x0'];
    y0 = data['y0'];
    x1 = data['x1'];
    y1 = data['y1'];

    var alfa = alfa.value;
    var beta = beta.value;
    var r = r.value;
    var b = b.value;
    var k = k.value;

    if(sel == 'Compartmental model'){
        for (i = 0; i < x0.length; i++) {
            xm[i] = r-r*x0[i]+(1-r)*y0[i]-Math.pow(y0[i],2)-(1+alfa)*x0[i]*y0[i]+x0[i];
            ym[i] = -(1+b)*y0[i]+Math.pow(y0[i],2)+(1+alfa-beta)*x0[i]*y0[i]+y0[i]

            dis[i] = Math.sqrt(Math.pow((xm[i] - x0[i]), 2) + Math.pow((ym[i] - y0[i]), 2));

            x1[i] = (xm[i] - x0[i]) / (20 * dis[i]) + x0[i];
            y1[i] = (ym[i] - y0[i]) / (20 * dis[i]) + y0[i];
        }
    }else if(sel == 'Compartmental ecd'){
        for (i = 0; i < x0.length; i++) {
            xm[i] = r-r*x0[i]+(1-x0[i]-y0[i]-r)*y0[i]-alfa*k*x0[i]*y0[i]+x0[i];
            ym[i] = alfa*k*x0[i]*y0[i]-(x0[i]+y0[i])*b*y0[i]-(x0[i]+y0[i])*(1-b)*beta*k*x0[i]*y0[i]-y0[i]*(1-x0[i]-y0[i])+y0[i]

            dis[i] = Math.sqrt(Math.pow((xm[i] - x0[i]), 2) + Math.pow((ym[i] - y0[i]), 2));

            x1[i] = (xm[i] - x0[i]) / (20 * dis[i]) + x0[i];
            y1[i] = (ym[i] - y0[i]) / (20 * dis[i]) + y0[i];
        }
    }else{
        for (i = 0; i < x0.length; i++) {
            xm[i] = r + (Math.pow((1 - alfa * y0[i]), k) - r) * x0[i] + (1 - r - x0[i] - y0[i]) * y0[i];
            ym[i] = (1 - Math.pow((1 - alfa * y0[i]),k)) * x0[i] + ((x0[i] + y0[i]) * (1 - b) * (Math.pow((1 - beta * x0[i]),k))) * y0[i];

            dis[i] = Math.sqrt(Math.pow((xm[i] - x0[i]), 2) + Math.pow((ym[i] - y0[i]), 2));

            x1[i] = (xm[i] - x0[i]) / (20 * dis[i]) + x0[i];
            y1[i] = (ym[i] - y0[i]) / (20 * dis[i]) + y0[i];
        }
    }
    source.trigger('change');
""")

select = Select(title="Option:", value="foo", options=["Simplified version", "Compartmental model", 'Compartmental ecd'], callback=callback)
callback.args['select'] = select

#Set up all the sliders
alfa_slider = Slider(start=0, end=1, value=alfa, step=.01, title="Alfa", callback=callback)
callback.args["alfa"] = alfa_slider

beta_slider = Slider(start=0, end=1, value=beta, step=.01, title="Beta", callback=callback)
callback.args["beta"] = beta_slider

b_slider = Slider(start=0, end=1, value=b, step=.01, title="b", callback=callback)
callback.args["b"] = b_slider

r_slider = Slider(start=0, end=1, value=r, step=.01, title="r", callback=callback)
callback.args["r"] = r_slider

k_slider = Slider(start=0.5, end=8, value=k, step=.5, title="k", callback=callback)
callback.args["k"] = k_slider

output_file("slider.html", title="Retrato de fases")

layout = row(
    plot,
    widgetbox(select, alfa_slider, beta_slider, b_slider, r_slider, k_slider),
)
show(layout)