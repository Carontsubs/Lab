import flet as ft

def main(page: ft.Page):
    page.title = "Calculadora Lab"
    page.scroll = "adaptive"
    page.padding = 20

    vistes_dict = {}

    # --- FUNCIÓ DE NETEJA AMB FOCUS ---
    def netejar_camps(llista_camps, text_res):
        for camp in llista_camps:
            camp.value = ""
        
        if isinstance(text_res, ft.Text):
            text_res.value = ""
        elif isinstance(text_res, ft.Column):
            text_res.controls = []
        
        if llista_camps:
            llista_camps[0].focus()
            
        page.update()

    # --- ESCULTA DE TECLAT ---
    def on_keyboard(e: ft.KeyboardEvent):
        if e.key == "Backspace":
            for dades in vistes_dict.values():
                if dades["col"].visible:
                    netejar_camps(dades["camps"], dades["res"])
                    break
        elif e.key == "Enter":
            for dades in vistes_dict.values():
                if dades["col"].visible:
                    dades["func_calc"](None)
                    break

    page.on_keyboard_event = on_keyboard

    # --- 1. ZINCATO ---
    txt_a_z, txt_e_z = ft.TextField(label="Conc. Zincato (gr/l)"), ft.TextField(label="Conc. Zn Original (gr/l)")
    txt_c_z, txt_b_z = ft.TextField(label="Conc. Desitjada (gr/l)"), ft.TextField(label="Volum final (ml)", value="1000")
    res_zincato = ft.Text(size=18, weight="bold", color="blue")
    def calc_zincato(e):
        try:
            d = ((float(txt_c_z.value)-float(txt_e_z.value))/(float(txt_a_z.value)-float(txt_e_z.value)))*(float(txt_b_z.value)/1000)
            res_zincato.value = f"RESULTAT: {round(d*1000, 1)} mL"
        except: res_zincato.value = "Error"
        page.update()
    col_zincato = ft.Column([ft.Text("ZINCATO", size=20, weight="bold"), txt_a_z, txt_e_z, txt_c_z, txt_b_z, ft.Row([ft.Button("Calcular", on_click=calc_zincato), ft.Button("Borrar", on_click=lambda _: netejar_camps([txt_a_z, txt_e_z, txt_c_z, txt_b_z], res_zincato))]), res_zincato], visible=True)
    vistes_dict["1"] = {"col": col_zincato, "camps": [txt_a_z, txt_e_z, txt_c_z, txt_b_z], "res": res_zincato, "func_calc": calc_zincato}

    # --- 2. ZIRCONI ---
    txt_abs_zr = ft.TextField(label="Absorbància Zr")
    res_zirconi = ft.Text(size=18, weight="bold", color="green")
    def calc_zirconi(e):
        try:
            b = float(txt_abs_zr.value)-0.296
            res_zirconi.value = f"RESULTAT: {round(((b*158.2)+0.4)*10)} ppm" if b>0 else "Abs <= 0"
        except: res_zirconi.value = "Error"
        page.update()
    col_zirconi = ft.Column([ft.Text("ZIRCONI", size=20, weight="bold"), txt_abs_zr, ft.Row([ft.Button("Calcular", on_click=calc_zirconi), ft.Button("Borrar", on_click=lambda _: netejar_camps([txt_abs_zr], res_zirconi))]), res_zirconi], visible=False)
    vistes_dict["2"] = {"col": col_zirconi, "camps": [txt_abs_zr], "res": res_zirconi, "func_calc": calc_zirconi}

    # --- 3. FLUX ---
    txt_edta_f, txt_agno3 = ft.TextField(label="mL de EDTA"), ft.TextField(label="mL de AgNO3")
    res_flux = ft.Column(spacing=2)
    def calc_flux(e):
        try:
            A, P = float(txt_edta_f.value), float(txt_agno3.value)
            b, c = A*13, (A*13)*2.085
            r, s, t = 1.509*((P*7.08)-(c*0.52)), 2.55*((1.509*((P*7.08)-(c*0.52)))/c), c+(1.509*((P*7.08)-(c*0.52)))
            res_flux.controls = [ft.Text(f"Zn: {round(b,1)} | ZnCl2: {round(c,1)} | NH4Cl: {round(r,1)}"), ft.Text(f"Rel. Molar: {round(s,2)} | Sals Tot: {round(t,1)}")]
        except: res_flux.controls = [ft.Text("Error")]
        page.update()
    col_flux = ft.Column([ft.Text("FLUX / CLORURS", size=20, weight="bold"), txt_edta_f, txt_agno3, ft.Row([ft.Button("Calcular", on_click=calc_flux), ft.Button("Borrar", on_click=lambda _: netejar_camps([txt_edta_f, txt_agno3], res_flux))]), res_flux], visible=False)
    vistes_dict["3"] = {"col": col_flux, "camps": [txt_edta_f, txt_agno3], "res": res_flux, "func_calc": calc_flux}

    # --- 4. TASA ATAC ---
    h_pi, h_pf, h_hr = ft.TextField(label="Pes Inicial (gr)"), ft.TextField(label="Pes Final (gr)"), ft.TextField(label="Hores", value="1")
    res_tasa = ft.Text(size=18, weight="bold", color="orange")
    def calc_tasa(e):
        try:
            d = ((float(h_pi.value) - float(h_pf.value)) * 1000) / (1.4 * float(h_hr.value))
            res_tasa.value = f"RESULTAT: {round(d, 3)} mg/hdm2"
        except: res_tasa.value = "Error"
        page.update()
    col_tasa = ft.Column([ft.Text("TASA D'ATAC", size=20, weight="bold"), h_pi, h_pf, h_hr, ft.Row([ft.Button("Calcular", on_click=calc_tasa), ft.Button("Borrar", on_click=lambda _: netejar_camps([h_pi, h_pf, h_hr], res_tasa))]), res_tasa], visible=False)
    vistes_dict["4"] = {"col": col_tasa, "camps": [h_pi, h_pf, h_hr], "res": res_tasa, "func_calc": calc_tasa}

    # --- 5. PES CAPA ---
    p_pi, p_pf = ft.TextField(label="Pes Inicial (gr)"), ft.TextField(label="Pes Final (gr)")
    res_pes = ft.Text(size=18, weight="bold", color="purple")
    def calc_pes(e):
        try:
            d = ((float(p_pi.value) - float(p_pf.value)) * 1000) / 0.0196
            res_pes.value = f"RESULTAT: {round(d)} mg/m2"
        except: res_pes.value = "Error"
        page.update()
    col_pes = ft.Column([ft.Text("PES DE CAPA", size=20, weight="bold"), p_pi, p_pf, ft.Row([ft.Button("Calcular", on_click=calc_pes), ft.Button("Borrar", on_click=lambda _: netejar_camps([p_pi, p_pf], res_pes))]), res_pes], visible=False)
    vistes_dict["5"] = {"col": col_pes, "camps": [p_pi, p_pf], "res": res_pes, "func_calc": calc_pes}

    # --- 6. MORA ---
    m_edta, m_naoh, m_dens = ft.TextField(label="mL de EDTA"), ft.TextField(label="mL de NaOH"), ft.TextField(label="Densitat")
    res_mora = ft.Column(spacing=2)
    def calc_mora(e):
        try:
            A, P, D = float(m_edta.value), float(m_naoh.value), float(m_dens.value)
            c, b = A*1.27, A*3.74
            q, r = P*21.75, 1.9*(P*21.75-1.37*c)
            s, t = 1+((r+b)/1350), 600*(D-(1+((r+b)/1350)))
            res_mora.controls = [ft.Text(f"Cu: {round(c,1)} | PiroCu: {round(b,1)} | 4K: {round(r,1)}"), ft.Text(f"Orto: {round(t,1)}")]
        except: res_mora.controls = [ft.Text("Error")]
        page.update()
    col_mora = ft.Column([ft.Text("MORA", size=20, weight="bold"), m_edta, m_naoh, m_dens, ft.Row([ft.Button("Calcular", on_click=calc_mora), ft.Button("Borrar", on_click=lambda _: netejar_camps([m_edta, m_naoh, m_dens], res_mora))]), res_mora], visible=False)
    vistes_dict["6"] = {"col": col_mora, "camps": [m_edta, m_naoh, m_dens], "res": res_mora, "func_calc": calc_mora}

    # --- 7. BLUEPASS ---
    txt_cr_blue = ft.TextField(label="Concentració Cr (g/l)")
    res_blue = ft.Text(size=18, weight="bold", color="cyan")
    def calc_blue(e):
        try:
            y = 1.773 * float(txt_cr_blue.value) + 0.0719
            res_blue.value = f"RESULTAT: {round(y, 2)} % Bluepass"
        except: res_blue.value = "Error"
        page.update()
    col_blue = ft.Column([ft.Text("BLUEPASS", size=20, weight="bold"), txt_cr_blue, ft.Row([ft.Button("Calcular", on_click=calc_blue), ft.Button("Borrar", on_click=lambda _: netejar_camps([txt_cr_blue], res_blue))]), res_blue], visible=False)
    vistes_dict["7"] = {"col": col_blue, "camps": [txt_cr_blue], "res": res_blue, "func_calc": calc_blue}

    # --- 8. S.675 ---
    txt_cr_s = ft.TextField(label="Concentració Cr (g/l)")
    res_s675 = ft.Text(size=18, weight="bold", color="teal")
    def calc_s675(e):
        try:
            y = 1.9761 * float(txt_cr_s.value) + 0.0402
            res_s675.value = f"RESULTAT: {round(y, 2)} % S.675"
        except: res_s675.value = "Error"
        page.update()
    col_s675 = ft.Column([ft.Text("S.675", size=20, weight="bold"), txt_cr_s, ft.Row([ft.Button("Calcular", on_click=calc_s675), ft.Button("Borrar", on_click=lambda _: netejar_camps([txt_cr_s], res_s675))]), res_s675], visible=False)
    vistes_dict["8"] = {"col": col_s675, "camps": [txt_cr_s], "res": res_s675, "func_calc": calc_s675}

    # --- NAVEGACIÓ ---
    def nav(e):
        desti = e.control.data
        for k, v in vistes_dict.items():
            v["col"].visible = (desti == k)
        page.update()

    page.add(
        ft.Row(
            wrap=True,
            alignment="center",
            spacing=10,
            run_spacing=10,
            controls=[
                ft.ElevatedButton("ZINCATO", data="1", on_click=nav),
                ft.ElevatedButton("ZIRCONI", data="2", on_click=nav),
                ft.ElevatedButton("FLUX", data="3", on_click=nav),
                ft.ElevatedButton("T. ATAC", data="4", on_click=nav),
                ft.ElevatedButton("P. CAPA", data="5", on_click=nav),
                ft.ElevatedButton("MORA", data="6", on_click=nav),
                ft.ElevatedButton("BLUE", data="7", on_click=nav),
                ft.ElevatedButton("S.675", data="8", on_click=nav),
            ],
        ),
        ft.Divider(),
        col_zincato, col_zirconi, col_flux, col_tasa, col_pes, col_mora, col_blue, col_s675
    )

ft.app(target=main)