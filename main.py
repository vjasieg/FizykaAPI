import flask
import matplotlib as mpl
import math
import numpy as np
import matplotlib.pyplot as plot
from flask import send_file, request

app = flask.Flask(__name__)
app.config["DEBUG"] = True
mpl.use("Agg")


def calc_vt(amp, czas, faza_poczatkowa, okres_d):
    y = []
    omega = (2 * math.pi) / okres_d
    if not isinstance(czas, int) and not isinstance(czas, float):
        for val in czas:
            y.append(amp * omega * math.cos((omega * val) + faza_poczatkowa))
        return y
    else:
        return round(amp * omega * math.cos((omega * czas) + faza_poczatkowa), 5)


def calc_xt(amp, czas, okres_d):
    y = []
    omega = (2 * math.pi) / okres_d
    if not isinstance(czas, int) and not isinstance(czas, float):
        for val in czas:
            y.append(amp * math.cos(omega * val))
        return y
    else:
        return round(amp * math.cos(omega * czas), 5)


def calc_at(amp, czas, faza_poczatkowa, okres_d):
    y = []
    omega = (2 * math.pi) / okres_d
    if not isinstance(czas, int) and not isinstance(czas, float):
        for val in czas:
            y.append(-amp * (omega ** 2) * math.sin(omega * val + faza_poczatkowa))
        return y
    else:
        return round(-amp * (omega ** 2) * math.sin(omega * czas + faza_poczatkowa), 5)


@app.route('/wartosci_t', methods=['GET'])
def wartosci_t():
    args = {"amp": float(request.args.get('amp')), "okres": float(request.args.get('okres')), "czas": float(request.args.get('czas')), "faza": float(request.args.get('faza'))}
    if args["amp"] is not None and args["okres"] is not None and args["faza"] is not None and args["czas"] is not None:
        json = {
            "v(t)": calc_vt(args["amp"], args["czas"], args["faza"], args["okres"]),
            "x(t)": calc_xt(args["amp"], args["czas"], args["okres"]),
            "a(t)": calc_at(args["amp"], args["czas"], args["faza"], args["okres"])
        }
        return json
    else:
        return "podaj wartosci amp okres faza i czas"


@app.route('/wykres_v', methods=['GET'])
def wykres_v():
    args = {"amp": request.args.get('amp'), "okres": request.args.get('okres'), "faza": request.args.get('faza')}
    if args["amp"] is not None and args["okres"] is not None and args["faza"] is not None:
        time = np.arange(0, 20, 0.1)
        plot.plot(time, calc_vt(amp=float(args["amp"]), czas=time, faza_poczatkowa=float(args["faza"]), okres_d=float(args["okres"])))
        plot.title('Wykres v(t)')
        plot.xlabel('t (czas)')
        plot.ylabel('v (predkosc)')
        plot.grid(True, which='both')
        plot.axhline(y=0, color='k')
        plot.savefig('chart.png')
        plot.figure().clear()
        return send_file("chart.png")
    else:
        return "podaj: '?amp=' '&okres=' '&faza='"


@app.route('/wykres_x', methods=['GET'])
def wykres_x():
    args = {"amp": request.args.get('amp'), "okres": request.args.get('okres')}
    if args["amp"] is not None and args["okres"] is not None:
        time = np.arange(0, 20, 0.1)
        plot.plot(time, calc_xt(amp=float(args["amp"]), czas=time, okres_d=float(args["okres"])))
        plot.title('Wykres x(t)')
        plot.xlabel('t (czas)')
        plot.ylabel('x (wychylenie)')
        plot.grid(True, which='both')
        plot.axhline(y=0, color='k')
        plot.savefig('chart.png')
        plot.figure().clear()
        return send_file("chart.png")
    else:
        return "podaj: '?amp=' '&okres='"


@app.route('/wykres_a', methods=['GET'])
def wykres_a():
    args = {"amp": request.args.get('amp'), "okres": request.args.get('okres'), "faza": request.args.get("faza")}
    if args["amp"] is not None and args["okres"] is not None and args["faza"] is not None:
        time = np.arange(0, 20, 0.1)
        plot.plot(time, calc_at(amp=float(args["amp"]), czas=time, faza_poczatkowa=float(args["faza"]), okres_d=float(args["okres"])))
        plot.title('Wykres a(t)')
        plot.xlabel('t (czas)')
        plot.ylabel('a (przyśpieszenie)')
        plot.grid(True, which='both')
        plot.axhline(y=0, color='k')
        plot.savefig('chart.png')
        plot.figure().clear()
        return send_file("chart.png")
    else:
        return "podaj: '?amp=' '&okres=' '&faza='"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=25565)


