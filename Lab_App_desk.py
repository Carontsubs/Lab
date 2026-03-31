import flet as ft
import numpy as np

def main(page: ft.Page):
    page.title = "Calculadora Lab"
    page.scroll = "adaptive"
    page.padding = 20

    vistes_dict = {}
    mv_list = []
    dil_list = []

    # --- FUNCIÓ DE NETEJA ---
    def netejar_camps(llista_camps, text_res):
        nonlocal mv_list, dil_list
        for camp in llista_camps:
            camp.value = ""
        
        if vistes_dict.get("9") and vistes_dict["9"]["col"].visible:
            mv_list = []
            list_mv_view.controls = []
            
        if vistes_dict.get("10") and vistes_dict["10"]["col"].visible:
            dil_list = []
            list_dil_view.controls = []
        
        if isinstance(text_res, ft.Text):
            text_res.value = ""
        elif isinstance(text_res, ft.Column):
            text_res.controls = []
        
        if llista_camps:
            llista_camps[0].focus()
        page.update()

    # --- TECLAT ---
    def on_keyboard(e: ft.KeyboardEvent):
        if e.key == "Backspace":
            for dades in vistes_dict.values():
                if dades["col"].visible:
                    netejar_camps(dades["camps"], dades["res"])
                    break
        elif e.key == "Enter":
            for dades in vistes_dict.values():
                if dades["col"].visible:
                    if dades == vistes_dict.get("9"): afegir_valor_mv(None)
                    elif dades == vistes_dict.get("10"): afegir_ingredient_dil(None)
                    else: dades["func_calc"](None)
                    break
    page.on_keyboard_event = on_keyboard

    # --- VISTES (1-10) ---
    
    # 1. ZINCATO
    txt_a_z, txt_e_z = ft.TextField(label="Conc. Zincato (gr/l)"), ft.TextField(label="Conc. Zn Original (gr/l)")
    txt_c_z, txt_b_z = ft.TextField(label="Conc. Desitjada (gr/l)"), ft.TextField(label="Volum final (ml)", value="1000")
    res_zincato = ft.Text(size=18, weight="bold", color="blue")
    def calc_zincato(e):
        try:
            d = ((float(txt_c_z.value)-float(txt_e_z.value))/(float(txt_a_z.value)-float(txt_e_z.value)))*(float(txt_b_z.value)/1000)
            res_zincato.value = f"RESULTAT: {round(d*1000, 1)} mL"; page.update()
        except: res_zincato.value = "Error"; page.update()
    col_zincato = ft.Column([ft.Text("ZINCATO", size=20, weight="bold"), txt_a_z, txt_e_z, txt_c_z, txt_b_z, ft.Row([ft.Button("Calcular", on_click=calc_zincato), ft.Button("Borrar", on_click=lambda _: netejar_camps([txt_a_z, txt_e_z, txt_c_z, txt_b_z], res_zincato))]), res_zincato], visible=True)
    vistes_dict["1"] = {"col": col_zincato, "camps": [txt_a_z, txt_e_z, txt_c_z, txt_b_z], "res": res_zincato, "func_calc": calc_zincato}

    # 2. ZIRCONI
    txt_abs_zr = ft.TextField(label="Absorbància Zr")
    res_zirconi = ft.Text(size=18, weight="bold", color="green")
    def calc_zirconi(e):
        try:
            b = float(txt_abs_zr.value)-0.296
            res_zirconi.value = f"RESULTAT: {round(((b*158.2)+0.4)*10)} ppm" if b>0 else "Abs <= 0"; page.update()
        except: res_zirconi.value = "Error"; page.update()
    col_zirconi = ft.Column([ft.Text("ZIRCONI", size=20, weight="bold"), txt_abs_zr, ft.Row([ft.Button("Calcular", on_click=calc_zirconi), ft.Button("Borrar", on_click=lambda _: netejar_camps([txt_abs_zr], res_zirconi))]), res_zirconi], visible=False)
    vistes_dict["2"] = {"col": col_zirconi, "camps": [txt_abs_zr], "res": res_zirconi, "func_calc": calc_zirconi}

    # 3. FLUX
    txt_edta_f, txt_agno3 = ft.TextField(label="mL de EDTA"), ft.TextField(label="mL de AgNO3")
    res_flux = ft.Column(spacing=2)
    def calc_flux(e):
        try:
            A, P = float(txt_edta_f.value), float(txt_agno3.value)
            b, c = A*13, (A*13)*2.085
            r = 1.509*((P*7.08)-(c*0.52))
            s = 2.55*(r/c)
            res_flux.controls = [ft.Text(f"Zn: {round(b,1)} | ZnCl2: {round(c,1)} | NH4Cl: {round(r,1)}"), ft.Text(f"Rel. Molar: {round(s,2)}")]; page.update()
        except: res_flux.controls = [ft.Text("Error")]; page.update()
    col_flux = ft.Column([ft.Text("FLUX", size=20, weight="bold"), txt_edta_f, txt_agno3, ft.Row([ft.Button("Calcular", on_click=calc_flux), ft.Button("Borrar", on_click=lambda _: netejar_camps([txt_edta_f, txt_agno3], res_flux))]), res_flux], visible=False)
    vistes_dict["3"] = {"col": col_flux, "camps": [txt_edta_f, txt_agno3], "res": res_flux, "func_calc": calc_flux}

    # 4. TASA ATAC
    h_pi, h_pf, h_hr = ft.TextField(label="Pes Inicial (gr)"), ft.TextField(label="Pes Final (gr)"), ft.TextField(label="Hores", value="1")
    res_tasa = ft.Text(size=18, weight="bold", color="orange")
    def calc_tasa(e):
        try:
            d = ((float(h_pi.value) - float(h_pf.value)) * 1000) / (1.4 * float(h_hr.value))
            res_tasa.value = f"RESULTAT: {round(d, 3)} mg/hdm2"; page.update()
        except: res_tasa.value = "Error"; page.update()
    col_tasa = ft.Column([ft.Text("TASA D'ATAC", size=20, weight="bold"), h_pi, h_pf, h_hr, ft.Row([ft.Button("Calcular", on_click=calc_tasa), ft.Button("Borrar", on_click=lambda _: netejar_camps([h_pi, h_pf, h_hr], res_tasa))]), res_tasa], visible=False)
    vistes_dict["4"] = {"col": col_tasa, "camps": [h_pi, h_pf, h_hr], "res": res_tasa, "func_calc": calc_tasa}

    # 5. PES CAPA
    p_pi, p_pf = ft.TextField(label="Pes Inicial (gr)"), ft.TextField(label="Pes Final (gr)")
    res_pes = ft.Text(size=18, weight="bold", color="purple")
    def calc_pes(e):
        try:
            d = ((float(p_pi.value) - float(p_pf.value)) * 1000) / 0.0196
            res_pes.value = f"RESULTAT: {round(d)} mg/m2"; page.update()
        except: res_pes.value = "Error"; page.update()
    col_pes = ft.Column([ft.Text("PES DE CAPA", size=20, weight="bold"), p_pi, p_pf, ft.Row([ft.Button("Calcular", on_click=calc_pes), ft.Button("Borrar", on_click=lambda _: netejar_camps([p_pi, p_pf], res_pes))]), res_pes], visible=False)
    vistes_dict["5"] = {"col": col_pes, "camps": [p_pi, p_pf], "res": res_pes, "func_calc": calc_pes}

    # 6. MORA
    m_edta, m_naoh, m_dens = ft.TextField(label="mL de EDTA"), ft.TextField(label="mL de NaOH"), ft.TextField(label="Densitat")
    res_mora = ft.Column(spacing=2)
    def calc_mora(e):
        try:
            A, P, D = float(m_edta.value), float(m_naoh.value), float(m_dens.value)
            c, b, q = A*1.27, A*3.74, P*21.75
            r = 1.9*(q-1.37*c)
            t = 600*(D-(1+((r+b)/1350)))
            res_mora.controls = [ft.Text(f"Cu: {round(c,1)} | PiroCu: {round(b,1)} | 4K: {round(r,1)}"), ft.Text(f"Orto: {round(t,1)}")]; page.update()
        except: res_mora.controls = [ft.Text("Error")]; page.update()
    col_mora = ft.Column([ft.Text("MORA", size=20, weight="bold"), m_edta, m_naoh, m_dens, ft.Row([ft.Button("Calcular", on_click=calc_mora), ft.Button("Borrar", on_click=lambda _: netejar_camps([m_edta, m_naoh, m_dens], res_mora))]), res_mora], visible=False)
    vistes_dict["6"] = {"col": col_mora, "camps": [m_edta, m_naoh, m_dens], "res": res_mora, "func_calc": calc_mora}

    # 7. BLUEPASS
    txt_cr_blue = ft.TextField(label="Concentració Cr (g/l)")
    res_blue = ft.Text(size=18, weight="bold", color="cyan")
    def calc_blue(e):
        try:
            y = 1.773 * float(txt_cr_blue.value) + 0.0719
            res_blue.value = f"RESULTAT: {round(y, 2)} % Bluepass"; page.update()
        except: res_blue.value = "Error"; page.update()
    col_blue = ft.Column([ft.Text("BLUEPASS", size=20, weight="bold"), txt_cr_blue, ft.Row([ft.Button("Calcular", on_click=calc_blue), ft.Button("Borrar", on_click=lambda _: netejar_camps([txt_cr_blue], res_blue))]), res_blue], visible=False)
    vistes_dict["7"] = {"col": col_blue, "camps": [txt_cr_blue], "res": res_blue, "func_calc": calc_blue}

    # 8. S.675
    txt_cr_s = ft.TextField(label="Concentració Cr (g/l)")
    res_s675 = ft.Text(size=18, weight="bold", color="teal")
    def calc_s675(e):
        try:
            y = 1.9761 * float(txt_cr_s.value) + 0.0402
            res_s675.value = f"RESULTAT: {round(y, 2)} % S.675"; page.update()
        except: res_s675.value = "Error"; page.update()
    col_s675 = ft.Column([ft.Text("S.675", size=20, weight="bold"), txt_cr_s, ft.Row([ft.Button("Calcular", on_click=calc_s675), ft.Button("Borrar", on_click=lambda _: netejar_camps([txt_cr_s], res_s675))]), res_s675], visible=False)
    vistes_dict["8"] = {"col": col_s675, "camps": [txt_cr_s], "res": res_s675, "func_calc": calc_s675}

    # 9. CLORURS (mV)
    txt_mv_input = ft.TextField(label="Valor mV", width=150)
    list_mv_view = ft.ListView(height=150, spacing=2)
    res_mv = ft.Column(spacing=2)
    def afegir_valor_mv(e):
        if txt_mv_input.value:
            try:
                val = float(txt_mv_input.value); mv_list.append(val)
                volum = (len(mv_list) - 1) * 0.5
                list_mv_view.controls.append(ft.Text(f"{volum} ml -> {val} mV"))
                txt_mv_input.value = ""; txt_mv_input.focus(); page.update()
            except: pass
    def calc_mv_logic(e):
        try:
            y_data = np.array(mv_list)
            if len(y_data) < 3: res_mv.controls = [ft.Text("Mínim 3 valors", color="red")]; page.update(); return
            x_data = np.arange(0, 10.5, 0.5)[:len(y_data)]
            dy = np.diff(y_data); i = np.argmax(np.abs(dy))
            d_ant = dy[i] - (dy[i-1] if i>0 else 0)
            d_post = dy[i] - (dy[i+1] if i<len(dy)-1 else 0)
            Cl = x_data[i] + ((0.5 * d_ant) / (d_ant + d_post))
            res_mv.controls = [ft.Text(f"Consum: {round(Cl, 2)} ml/l", weight="bold"), ft.Text(f"CLORURS: {round(Cl * 14.2, 1)} ppm", color="green", weight="bold")]; page.update()
        except: res_mv.controls = [ft.Text("Error")]; page.update()
    col_mv = ft.Column([ft.Text("CLORURS (mV)", size=20, weight="bold"), ft.Row([txt_mv_input, ft.Button("Afegir", on_click=afegir_valor_mv)]), list_mv_view, ft.Row([ft.Button("Calcular", on_click=calc_mv_logic), ft.Button("Borrar", on_click=lambda _: netejar_camps([txt_mv_input], res_mv))]), res_mv], visible=False)
    vistes_dict["9"] = {"col": col_mv, "camps": [txt_mv_input], "res": res_mv, "func_calc": calc_mv_logic}

    # 10. DILUCIÓ
    txt_dil_vol = ft.TextField(label="Volum inicial (ml)", width=200)
    txt_dil_nom = ft.TextField(label="Nom ingredient", width=150)
    txt_dil_pct = ft.TextField(label="% final", width=100)
    list_dil_view = ft.ListView(height=120, spacing=2)
    res_dil = ft.Column(spacing=2)
    def afegir_ingredient_dil(e):
        nom = txt_dil_nom.value.strip() or f"Ing {len(dil_list)+1}"
        try:
            pct = float(txt_dil_pct.value)
            if sum(item[1] for item in dil_list) + pct >= 100: res_dil.controls = [ft.Text("Suma > 100%", color="red")]
            else:
                dil_list.append((nom, pct))
                list_dil_view.controls.append(ft.Text(f"• {nom}: {pct}%"))
                txt_dil_nom.value = ""; txt_dil_pct.value = ""; txt_dil_nom.focus()
            page.update()
        except: pass
    def calc_dil_logic(e):
        try:
            vol = float(txt_dil_vol.value)
            v_fin = vol / (1 - sum(i[1] for i in dil_list) / 100)
            res = [ft.Text(f"Volum Final: {round(v_fin, 2)} ml", weight="bold", color="blue")]
            for n, p in dil_list: res.append(ft.Text(f"Afegir {n}: {round((p/100)*v_fin, 2)} ml"))
            res_dil.controls = res; page.update()
        except: res_dil.controls = [ft.Text("Error")]; page.update()
    col_dil = ft.Column([ft.Text("DILUCIÓ", size=20, weight="bold"), txt_dil_vol, ft.Row([txt_dil_nom, txt_dil_pct, ft.Button("Afegir", on_click=afegir_ingredient_dil)]), list_dil_view, ft.Row([ft.Button("Calcular", on_click=calc_dil_logic), ft.Button("Borrar", on_click=lambda _: netejar_camps([txt_dil_vol, txt_dil_nom, txt_dil_pct], res_dil))]), res_dil], visible=False)
    vistes_dict["10"] = {"col": col_dil, "camps": [txt_dil_vol, txt_dil_nom, txt_dil_pct], "res": res_dil, "func_calc": calc_dil_logic}

    # --- NAVEGACIÓ I MUNTATGE FINAL ---
    def nav(e):
        for k, v in vistes_dict.items(): v["col"].visible = (e.control.data == k)
        page.update()

    page.add(
        ft.Row(wrap=True, alignment="center", controls=[
            ft.ElevatedButton("ZINCATO", data="1", on_click=nav),
            ft.ElevatedButton("ZIRCONI", data="2", on_click=nav),
            ft.ElevatedButton("FLUX", data="3", on_click=nav),
            ft.ElevatedButton("T. ATAC", data="4", on_click=nav),
            ft.ElevatedButton("P. CAPA", data="5", on_click=nav),
            ft.ElevatedButton("MORA", data="6", on_click=nav),
            ft.ElevatedButton("BLUE", data="7", on_click=nav),
            ft.ElevatedButton("S.675", data="8", on_click=nav),
            ft.ElevatedButton("CLORURS", data="9", on_click=nav),
            ft.ElevatedButton("DILUCIÓ", data="10", on_click=nav),
        ]),
        ft.Divider(),
        # AQUÍ ESTAVA L'ERROR: Ara afegim TOTES les columnes al contenidor principal
        col_zincato, col_zirconi, col_flux, col_tasa, col_pes, col_mora, col_blue, col_s675, col_mv, col_dil
    )

ft.app(target=main)