def refacto_dette(dette_toref, leverage_toref):
    dette = []
    leverage = []
    for dett in dette_toref:
        if dett == "-":
            dette.append(0)
        else:
            dette.append(dett)
    for lev in leverage_toref:
        try:
            leverage.append(float(lev[:-1].replace(',', '.')))
        except:
            leverage.append(lev)
    return dette, leverage

def croissance(ls_check):
        ls_croi = []
        el_prec = ls_check[0]
        for element in ls_check:
            if el_prec < element:
                ls_croi.append(True)
            else:
                ls_croi.append(False)
            el_prec = element
        decroi = ls_croi.count(False)
        croi = ls_croi.count(True)
        return croi, decroi