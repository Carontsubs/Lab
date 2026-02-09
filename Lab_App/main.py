import flet as ft

def main(page: ft.Page):
    page.title = "Calculadora Lab"
    page.scroll = "adaptive"
    page.padding = 20

    # --- FUNCIONS DE NETEJA GENÈRIQUES ---
    def netejar_camps(llista_camps, text_res):
        for camp in llista_camps:
            camp.value = ""
        if isinstance(text_res, ft.Text):
            text_res.value = ""
        elif isinstance(text_res, ft.Column):
            text_res.controls = []
        page.update()

    # --- 1. ZINCATO ---
    txt_a_z = ft.TextField(label="Conc. Zincato (gr/l)")
    txt_e_z = ft.TextField(label="Conc. Zn Original (gr/l)")
    txt_c_z = ft.TextField(label="Conc. Desitjada (gr/l)")
    txt_b_z = ft.TextField(label="Volum final (ml)", value="1000")
    res_zincato = ft.Text(size=18, weight="bold", color="blue")
    
    def calc_zincato(e):
        try:
            d = ((float(txt_c_z.value)-float(txt_e_z.value))/(float(txt_a_z.value)-float(txt_e_z.value)))*(float(txt_b_z.value)/1000)
            res_zincato.value = f"RESULTAT: {round(d*1000, 1)} mL"
        except: res_zincato.value = "Error dades"
        page.update()

    col_zincato = ft.Column([
        ft.Text("ZINCATO", size=20, weight="bold"),
        txt_a_z, txt_e_z, txt_c_z, txt_b_z,
        ft.Row([
            ft.Button(content=ft.Text("Calcular"), on_click=calc_zincato),
            ft.Button(content=ft.Text("Borrar"), on_click=lambda _: netejar_camps([txt_a_z, txt_e_z, txt_c_z, txt_b_z], res_zincato))
        ]),
        res_zincato
    ], visible=True)

    # --- 2. ZIRCONI ---
    txt_abs_zr = ft.TextField(label="Absorbància Zr")
    res_zirconi = ft.Text(size=18, weight="bold", color="green")
    
    def calc_zirconi(e):
        try:
            b = float(txt_abs_zr.value)-0.296
            res_zirconi.value = f"RESULTAT: {round(((b*158.2)+0.4)*10)} ppm" if b>0 else "Abs <= 0"
        except: res_zirconi.value = "Error"
        page.update()

    col_zirconi = ft.Column([
        ft.Text("ZIRCONI", size=20, weight="bold"),
        txt_abs_zr,
        ft.Row([
            ft.Button(content=ft.Text("Calcular"), on_click=calc_zirconi),
            ft.Button(content=ft.Text("Borrar"), on_click=lambda _: netejar_camps([txt_abs_zr], res_zirconi))
        ]),
        res_zirconi
    ], visible=False)

    # --- 3. FLUX ---
    txt_edta_f = ft.TextField(label="mL de EDTA")
    txt_agno3 = ft.TextField(label="mL de AgNO3")
    res_flux = ft.Column(spacing=2)
    
    def calc_flux(e):
        try:
            A, P = float(txt_edta_f.value), float(txt_agno3.value)
            b, c = A*13, (A*13)*2.085
            r, s, t = 1.509*((P*7.08)-(c*0.52)), 2.55*((1.509*((P*7.08)-(c*0.52)))/c), c+(1.509*((P*7.08)-(c*0.52)))
            y = (450-t)*70 if (t<450 and c<250 and r<200) else 0
            u = (r*1.21-c)*70 if (c<250 and r > 200) else 0
            v = (200-r) * 70 if (r < 200 and c > 250) else 0
            res_flux.controls = [
                ft.Text(f"Zn: {round(b,1)} | ZnCl2: {round(c,1)} | NH4Cl: {round(r,1)}"),
                ft.Text(f"Rel. Molar: {round(s,2)} | Sals Tot: {round(t,1)}"),
                ft.Text(f"Faltes: ZnCl2:{round(u)}g, NH4Cl:{round(v)}g, Tot:{round(y)}g", color="red", weight="bold")
            ]
        except: res_flux.controls = [ft.Text("Error dades")]
        page.update()

    col_flux = ft.Column([
        ft.Text("FLUX / CLORURS", size=20, weight="bold"),
        txt_edta_f, txt_agno3,
        ft.Row([
            ft.Button(content=ft.Text("Calcular"), on_click=calc_flux),
            ft.Button(content=ft.Text("Borrar"), on_click=lambda _: netejar_camps([txt_edta_f, txt_agno3], res_flux))
        ]),
        res_flux
    ], visible=False)

    # --- 4. TASA D'ATAC ---
    h_pi = ft.TextField(label="Pes Inicial (gr)")
    h_pf = ft.TextField(label="Pes Final (gr)")
    h_hr = ft.TextField(label="Hores", value="1")
    res_tasa = ft.Text(size=18, weight="bold", color="orange")
    
    def calc_tasa(e):
        try:
            d = ((float(h_pi.value) - float(h_pf.value)) * 1000) / (1.4 * float(h_hr.value))
            res_tasa.value = f"RESULTAT: {round(d, 3)} mg/hdm2"
        except: res_tasa.value = "Error dades"
        page.update()

    col_tasa = ft.Column([
        ft.Text("TASA D'ATAC", size=20, weight="bold"),
        h_pi, h_pf, h_hr,
        ft.Row([
            ft.Button(content=ft.Text("Calcular"), on_click=calc_tasa),
            ft.Button(content=ft.Text("Borrar"), on_click=lambda _: netejar_camps([h_pi, h_pf, h_hr], res_tasa))
        ]),
        res_tasa
    ], visible=False)

    # --- 5. PES DE CAPA ---
    p_pi = ft.TextField(label="Pes Inicial (gr)")
    p_pf = ft.TextField(label="Pes Final (gr)")
    res_pes = ft.Text(size=18, weight="bold", color="purple")
    
    def calc_pes(e):
        try:
            d = ((float(p_pi.value) - float(p_pf.value)) * 1000) / 0.0196
            res_pes.value = f"RESULTAT: {round(d)} mg/m2"
        except: res_pes.value = "Error dades"
        page.update()

    col_pes = ft.Column([
        ft.Text("PES DE CAPA", size=20, weight="bold"),
        p_pi, p_pf,
        ft.Row([
            ft.Button(content=ft.Text("Calcular"), on_click=calc_pes),
            ft.Button(content=ft.Text("Borrar"), on_click=lambda _: netejar_camps([p_pi, p_pf], res_pes))
        ]),
        res_pes
    ], visible=False)

    # --- 6. MORA (Pirofosfats) ---
    m_edta = ft.TextField(label="mL de EDTA")
    m_naoh = ft.TextField(label="mL de NaOH")
    m_dens = ft.TextField(label="Densitat")
    res_mora = ft.Column(spacing=2)

    def calc_mora(e):
        try:
            A, P, D = float(m_edta.value), float(m_naoh.value), float(m_dens.value)
            c = A * 1.27                 # Cu g/l
            b = A * 3.74                 # PiroCu g/l
            q = P * 21.75                # Piro Total
            r = 1.9 * (q - 1.37 * c)     # Piro tetrapotasic
            s = 1 + ((r + b)/1350)       # Densitat teorica
            t = 600 * (D - s)            # Ortofosfat
            
            res_mora.controls = [
                ft.Text(f"Cu: {round(c, 1)} g/l", weight="bold"),
                ft.Text(f"PiroCu: {round(b, 1)} g/l"),
                ft.Text(f"4K: {round(r, 1)} g/l"),
                ft.Text(f"Orto: {round(t, 1)} g/l"),
                ft.Text(f"Dens. Teòrica: {round(s, 3)}", size=12, color="grey")
            ]
        except: res_mora.controls = [ft.Text("Error dades")]
        page.update()

    col_mora = ft.Column([
        ft.Text("MORA (PIROFOSFATS)", size=20, weight="bold"),
        m_edta, m_naoh, m_dens,
        ft.Row([
            ft.Button(content=ft.Text("Calcular"), on_click=calc_mora),
            ft.Button(content=ft.Text("Borrar"), on_click=lambda _: netejar_camps([m_edta, m_naoh, m_dens], res_mora))
        ]),
        res_mora
    ], visible=False)

    # --- NAVEGACIÓ ---
    def nav(e):
        desti = e.control.data
        col_zincato.visible = (desti == "1")
        col_zirconi.visible = (desti == "2")
        col_flux.visible = (desti == "3")
        col_tasa.visible = (desti == "4")
        col_pes.visible = (desti == "5")
        col_mora.visible = (desti == "6")
        page.update()

    page.add(
        ft.Column([
            ft.Row([
                ft.Button(content=ft.Text("ZINCATO"), data="1", on_click=nav),
                ft.Button(content=ft.Text("ZIRCONI"), data="2", on_click=nav),
                ft.Button(content=ft.Text("FLUX"), data="3", on_click=nav),
            ], alignment="center"),
            ft.Row([
                ft.Button(content=ft.Text("TASA ATAC"), data="4", on_click=nav),
                ft.Button(content=ft.Text("PES CAPA"), data="5", on_click=nav),
                ft.Button(content=ft.Text("MORA"), data="6", on_click=nav),
            ], alignment="center"),
        ]),
        ft.Divider(),
        col_zincato, col_zirconi, col_flux, col_tasa, col_pes, col_mora
    )

ft.app(target=main)