import numpy, scipy, io, base64
from scipy.integrate import quad
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import numpy as np


def getDelta(a, b, c, d):
    return (c + d - a - b) / a

# def Zsolver(aDash, bDash):
#     coeff = [1, bDash - 1, aDash - 3 * bDash**2 - 2 * bDash, -aDash * bDash + bDash**2 + bDash**3]
#     return np.roots(coeff)

# def C0(Y0, P, To, Tc, Pc, Psat, acentric):
#     R = 8.314
#     w = -1 - np.log10(Psat / Pc)
#     Tr = To / Tc
#     omega = 0.37464 + 1.54226 * acentric - 0.26992 * acentric**2
#     a = (0.45724 * (Tc**2 * R**2) / Pc) * (1 + omega * (1 - np.sqrt(Tr)))**2
#     b = 0.07780 * R * Tc / Pc
#     aDash = a * P / (R * To)**2
#     bDash = b * P / (R * To)

#     Zreal = [z.real for z in Zsolver(aDash, bDash) if np.isreal(z)]
#     if len(Zreal) == 1:
#         Z = Zreal[0]
#     else:
#         Z = min(Zreal)
#     return (Y0 * P) / (R * To * Z)


def integrate(rev, iso, Ca0, Cb0, V0, Y0, coeffs, DeltaHo, Keqr,
              CpA, CpB, CpC, CpD, To, Tr, Kr, xLimit, Ea):
    x = numpy.linspace(0, xLimit, 100)  # Ensure x is a scalar when passed
    y = numpy.zeros(len(x))  # Array to store integral results

    # Define a wrapper function for 1/rateFunction
    def integrand(x_val, rev, iso, Ca0, Cb0, V0, Y0, coeffs, DeltaHo, Keqr,
                  CpA, CpB, CpC, CpD, To, Tr, Kr, Ea):
        rate = rateFunction(rev, iso, Ca0, Cb0, V0, Y0, coeffs, DeltaHo, Keqr,
                            CpA, CpB, CpC, CpD, To, Tr, Kr, x_val, Ea)
        return 1 / rate if rate != 0 else float('inf')  # Avoid division by zero

    for i in range(len(x)):  # Loop over x values
        try:
            # Integrate 1/rateFunction from 0 to x[i]
            y[i] = V0*Y0*quad(integrand, 0, x[i], args=(rev, iso, Ca0, Cb0, V0, Y0, coeffs,
                                                  DeltaHo, Keqr, CpA, CpB, CpC, CpD,
                                                  To, Tr, Kr, Ea))[0]
        except ZeroDivisionError:
            y[i] = numpy.nan  # Handle ZeroDivisionError in integration
        except Exception as e:
            print(f"Error at x = {x[i]}: {e}")  # Print other errors
            y[i] = numpy.nan  # Handle any other errors

    return x, y  # Return x and corresponding results




def Tnew_NonIsothermal(DeltaHo, coeffs, CpA, CpB, CpC, CpD, To, Tr, x):
    DeltaCp = -CpA - coeffs[1]/coeffs[0] * CpB + coeffs[2]/coeffs[0] * CpC + coeffs[3]/coeffs[0] * CpD
    DeltaH = DeltaHo + DeltaCp * (To - Tr)
    return To - (DeltaH * x) / CpA

def kconstant(To, Tr, Kr, Keqr, DeltaH, Ea):
    R = 8.314  # J/mol·K
    k = Kr * np.exp((-Ea / R) * (1.0/To - 1.0/Tr))
    Keq = Keqr * np.exp(-DeltaH / R * (1.0/To - 1.0/Tr))
    return k, Keq

def rateFunction(rev, iso, Ca0, Cb0, V0, Y0, coeffs, DeltaHo, Keqr, CpA, CpB, CpC, CpD, To, Tr, Kr, x, Ea):
    # Calculate the temperature based on whether it's isothermal or not
    Tnew = To if iso else Tnew_NonIsothermal(DeltaHo, coeffs, CpA, CpB, CpC, CpD, To, Tr, x)
    
    # Calculate rate constants
    k, K = kconstant(Tnew, Tr, Kr, Keqr, DeltaHo, Ea)
    
    # Get delta value (assumed to be related to stoichiometry)
    delta = getDelta(*coeffs)
    
    # Avoid division by zero in the concentration calculations
    if (1 + Y0 * x * delta) == 0:
        return 0  # Avoid zero division
    
    # Calculate concentrations
    CA = Ca0 * (1 - x) / (1 + Y0 * x * delta)
    CB = Ca0 * (Cb0 / Ca0 - coeffs[1] / coeffs[0] * x) / (1 + Y0 * x * delta)
    CC = Ca0 * (coeffs[2] / coeffs[0]) * x / (1 + Y0 * x * delta)
    CD = Ca0 * (coeffs[3] / coeffs[0]) * x / (1 + Y0 * x * delta)
    
    # If the reaction is reversible, use the reversible rate law
    if rev:
        return k * ((CA ** coeffs[0]) * (CB ** coeffs[1]) - (CC ** coeffs[2]) * (CD ** coeffs[3]) / K)
    else:
        return k * (CA ** coeffs[0]) * (CB ** coeffs[1])


def cstrCalculateIsothermal(rev, iso, Ca0, Cb0, V0, Y0, coeffs, DeltaHo, Keqr,
                            CpA, CpB, CpC, CpD, To, Tr, Kr, xLimit, Ea):
    Tnew = To if iso else Tnew_NonIsothermal(DeltaHo, coeffs, CpA, CpB, CpC, CpD, To, Tr, xLimit)
    k, K = kconstant(Tnew,Tr, Kr, Keqr, DeltaHo, Ea)
    delta = getDelta(*coeffs)

    CA = Ca0 * (1 - xLimit) / (1 + Y0 * xLimit * delta)
    CB = Ca0 * (Cb0 / Ca0 - coeffs[1]/coeffs[0] * xLimit) / (1 + Y0 * xLimit * delta)
    CC = Ca0 * (coeffs[2]/coeffs[0]) * xLimit / (1 + Y0 * xLimit * delta)
    CD = Ca0 * (coeffs[3]/coeffs[0]) * xLimit / (1 + Y0 * xLimit * delta)

    if rev:
        rate = k * ((CA**coeffs[0]) * (CB**coeffs[1]) - (CC**coeffs[2]) * (CD**coeffs[3]) / K)
    else:
        rate = k * (CA**coeffs[0]) * (CB**coeffs[1])
    volume = V0*Y0 * xLimit / rate if rate != 0 else 0

    return volume, {
        "Final Concentration of A in moles/cubic meter": CA,
        "Final Concentration of B in moles/cubic meter": CB,
        "Final Concentration of C in moles/cubic meter": CC,
        "Final Concentration of D in moles/cubic meter": CD,
        "Final Rate": rate
    }
def pfrCalculateIsothermal(rev, iso, Ca0, Cb0, V0, Y0, coeffs, DeltaHo, Keqr,
                            CpA, CpB, CpC, CpD, To, Tr, Kr, xLimit, Ea):
    # Set temperature based on isothermal condition or non-isothermal
    Tnew = To if iso else Tnew_NonIsothermal(DeltaHo, coeffs, CpA, CpB, CpC, CpD, To, Tr, xLimit)
    
    # Calculate rate constant and equilibrium constant
    k, K = kconstant(Tnew, Tr, Kr, Keqr, DeltaHo, Ea)
    delta = getDelta(*coeffs)
    
    # Calculate concentrations based on xLimit
    CA = Ca0 * (1 - xLimit) / (1 + Y0 * xLimit * delta)
    CB = Ca0 * (Cb0 / Ca0 - coeffs[1] / coeffs[0] * xLimit) / (1 + Y0 * xLimit * delta)
    CC = Ca0 * (coeffs[2] / coeffs[0]) * xLimit / (1 + Y0 * xLimit * delta)
    CD = Ca0 * (coeffs[3] / coeffs[0]) * xLimit / (1 + Y0 * xLimit * delta)

    # Determine rate depending on whether the reaction is reversible or not
    if rev:
        rate = k * ((CA**coeffs[0]) * (CB**coeffs[1]) - (CC**coeffs[2]) * (CD**coeffs[3]) / K)
    else:
        rate = k * (CA**coeffs[0]) * (CB**coeffs[1])
    
    # Integrate to get volume and reaction history
    x, y = integrate(rev, iso, Ca0, Cb0, V0, Y0, coeffs, DeltaHo, Keqr,
              CpA, CpB, CpC, CpD, To, Tr, Kr, xLimit, Ea)
    
    # Calculate final concentrations at xLimit
    x_val = xLimit
    CA_final = Ca0 * (1 - x_val) / (1 + Y0 * x_val * delta)
    CB_final = Ca0 * (Cb0 / Ca0 - (coeffs[1] / coeffs[0]) * x_val) / (1 + Y0 * x_val * delta)
    CC_final = Ca0 * (coeffs[2] / coeffs[0]) * x_val / (1 + Y0 * x_val * delta)
    CD_final = Ca0 * (coeffs[3] / coeffs[0]) * x_val / (1 + Y0 * x_val * delta)

    # Calculate final rate based on the final concentration
    finalRate = rateFunction(rev, iso, Ca0, Cb0, V0, Y0, coeffs, DeltaHo, Keqr, CpA, CpB, CpC, CpD, To, Tr, Kr, xLimit, Ea)

    # Return results: Final volume, concentrations, and final rate
    return (y[-1], {"Concentration of A": CA_final, "Concentration of B": CB_final, "Concentration of C": CC_final, "Concentration of D": CD_final, "Final Rate": finalRate})



def cstrPlotIsothermal(rev, iso, Ca0, Cb0, V0, Y0, coeffs, DeltaHo, Keq,
                       CpA, CpB, CpC, CpD, To, Tr, Kr, xLimit, Ea):
    x = np.linspace(0, xLimit, 100)
    ca, cb, cc, cd, inv_rate,T,k_values,Keq_values = map(lambda _: np.zeros_like(x), range(8))
    delta = getDelta(*coeffs)

    for i in range(len(x)):
        inv_rate[i] = 1 / rateFunction(rev, iso, Ca0, Cb0, V0, Y0, coeffs, DeltaHo, Keq,
                                       CpA, CpB, CpC, CpD,To, Tr, Kr, x[i], Ea)
        ca[i] = Ca0 * (1 - x[i]) / (1 + Y0 * x[i] * delta)
        cc[i] = Ca0 * (coeffs[2]/coeffs[0] * x[i]) / (1 + Y0 * x[i] * delta)
        cb[i] = 0 if coeffs[1] == 0 else Ca0 * (Cb0 / Ca0 - coeffs[1]/coeffs[0] * x[i]) / (1 + Y0 * x[i] * delta)
        cd[i] = 0 if coeffs[3] == 0 else Ca0 * (coeffs[3]/coeffs[0]) * x[i] / (1 + Y0 * x[i] * delta)

        try:
            T[i] = To + (-1 * DeltaHo) * x[i] / CpA if CpA != 0 else To
        except Exception as e:
            T[i] = To
        k, K = kconstant(T[i], Tr, Kr, Keq, DeltaHo, Ea)
        k_values[i] = k
        Keq_values[i] = K

    def plot_base64(x, y, xlabel, ylabel, title):
        plt.clf()
        plt.plot(x, y)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        return base64.b64encode(buf.getvalue()).decode()

    return (
        plot_base64(x, inv_rate, "Conversion", "1/Rate", "1/Rate vs Conversion"),
        plot_base64(x, ca, "Conversion", "Concentration of A", "A vs Conversion"),
        plot_base64(x, cb, "Conversion", "Concentration of B", "B vs Conversion"),
        plot_base64(x, cc, "Conversion", "Concentration of C", "C vs Conversion"),
        plot_base64(x, cd, "Conversion", "Concentration of D", "D vs Conversion"),
        plot_base64(x, T, "Conversion", "temperature", "T vs Conversion"),
        plot_base64(x, k_values, "Conversion", "Rate Constant", "Rate Constant vs Conversion"),
        plot_base64(x, Keq_values, "Conversion", "Equilibrium Constant", "Equilibrium Constant vs Conversion")

    )

def calculate_result(form_data, session):
    reactor = session.get('reactor_type')
    reversible = session.get('reversibility') == 'rev'
    isothermal = session.get('thermal') == 'isothermal'

    try:
        ca0 = float(form_data['ca0'])
        cb0 = float(form_data['cb0'])
        v0 = float(form_data['v0'])
        y0 = float(form_data['y0'])
        Kr = float(form_data['Kr'])
        keq = float(form_data['keq'])
        Tr = float(form_data.get('Tr', 1))
        To = float(form_data.get('To', 1))
        DeltaHo = float(form_data.get('DeltaHo', 0))
        Ea = float(form_data.get('Ea', 0))
        CpA = float(form_data.get('cpA', 1))
        CpB = float(form_data.get('cpB', 1))
        CpC = float(form_data.get('cpC', 1))
        CpD = float(form_data.get('cpD', 1))
        xLimit = float(form_data.get('x', 1))

        coeffs = [
            float(form_data['ra']),
            float(form_data['rb']),
            float(form_data['rc']),
            float(form_data['rd'])
        ]

        if not (0 <= xLimit <= 1):
            return {"product": "x must be between 0 and 1"}
        if not (0 <= To <= 10000):
            return {"product": "Reaction is not feasible at this temperature"}
        if not (0 <= Tr <= 10000):
            return {"product": "Reaction is not feasible at this temperature"}
        if not (0 <= v0):
            return {"product": "Volume must be greater than 0"}
        if not (0 <= y0 <= 1):
            return {"product": "mole fraction of Y must be between 0 and 1"}
        if not (0 <= ca0 <= 10000):
            return {"product": "Invalid Input "}
        if not (0 <= cb0 <= 10000):
            return {"product": "Invalid Input "}   

    except Exception as e:
        return {"product": f"Error: {e}"}

    #  Perform calculation based on reactor type
    if reactor == 'pfr':
        volume, concs = pfrCalculateIsothermal(reversible, isothermal, ca0, cb0, v0, y0, coeffs, DeltaHo,keq,
                            CpA, CpB, CpC, CpD, To, Tr, Kr, xLimit, Ea
        )

        return {
            "product": abs(volume),
            "outputFactors": concs,
            "plot_url": "",  # Optional: Add plotting function for PFR if needed
            "plot_ca": "",
            "plot_cb": "",
            "plot_cc": "",
            "plot_cd": "",
            "plot_T": "",
            "plot_k": "",
            "plot_Keq": ""
        }

    else:  # Default: CSTR
        volume, concs = cstrCalculateIsothermal(
            reversible, isothermal, ca0, cb0, v0, y0, coeffs,
            DeltaHo, keq, CpA, CpB, CpC, CpD, To, Tr, Kr, xLimit, Ea
        )

        plots = cstrPlotIsothermal(
            reversible, isothermal, ca0, cb0, v0, y0, coeffs,
            DeltaHo, keq, CpA, CpB, CpC, CpD, To, Tr, Kr, xLimit, Ea
        )

        return {
            "product": abs(volume),
            "outputFactors": concs,
            "plot_url": plots[0],
            "plot_ca": plots[1],
            "plot_cb": plots[2],
            "plot_cc": plots[3],
            "plot_cd": plots[4],
            "plot_T": plots[5],
            "plot_k": plots[6],
            "plot_Keq": plots[7]
        }

