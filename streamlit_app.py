import streamlit as st
import math

# ============================================================
# THERMOCALC
# Calculadora de Termodinâmica
# Desenvolvido por Horacio Arcenio Mbombi
# ============================================================

st.set_page_config(
    page_title="ThermoCalc - Calculadora de Termodinâmica",
    page_icon="🌡️",
    layout="wide"
)

# ============================================================
# FUNÇÕES
# ============================================================

# ------------------------------------------------------------
# Pressão de saturação
# ------------------------------------------------------------

def pressao_saturacao(T):
    """
    Calcula a pressão de saturação em mmHg.
    T em Kelvin.
    """
    return 10 ** (
        23.686185
        - 1691.8057 / T
        - 6.04560 * math.log10(T)
        + 0.00195754 * T
    )


def temperatura_da_pressao(p):
    """
    Calcula a temperatura em Kelvin a partir da pressão em mmHg
    usando o método da bisseção.
    """

    Tmin = 250.0
    Tmax = 700.0

    for _ in range(100):
        Tmed = (Tmin + Tmax) / 2
        pmed = pressao_saturacao(Tmed)

        if pmed < p:
            Tmin = Tmed
        else:
            Tmax = Tmed

    return (Tmin + Tmax) / 2


def converter_pressao_para_mmhg(valor, unidade):
    if unidade == "mmHg":
        return valor
    elif unidade == "kPa":
        return valor * 7.50061683
    elif unidade == "bar":
        return valor * 750.061683
    elif unidade == "atm":
        return valor * 760.0


def converter_mmhg(valor, unidade):
    if unidade == "mmHg":
        return valor
    elif unidade == "kPa":
        return valor / 7.50061683
    elif unidade == "bar":
        return valor / 750.061683
    elif unidade == "atm":
        return valor / 760.0


# ============================================================
# CABEÇALHO
# ============================================================

st.title("🌡️ ThermoCalc")

st.subheader("Calculadora de Termodinâmica")

st.markdown(
    "**Desenvolvido por Horacio Arcenio Mbombi**"
)

st.divider()


# ============================================================
# MENU
# ============================================================

st.sidebar.title("📚 Módulos")

modulo = st.sidebar.selectbox(
    "Escolha uma calculadora:",
    [
        "Pressão de saturação",
        "Gás ideal",
        "Primeira Lei da Termodinâmica",
        "Calor sensível",
        "Máquina de Carnot",
        "Processo isentrópico"
    ]
)


# ============================================================
# 1 - PRESSÃO DE SATURAÇÃO
# ============================================================

if modulo == "Pressão de saturação":

    st.header("💧 Pressão de Saturação")

    st.write(
        "Utilize a equação para calcular a pressão de saturação "
        "a partir da temperatura ou determinar a temperatura "
        "a partir da pressão."
    )

    operacao = st.radio(
        "Escolha o cálculo:",
        [
            "Temperatura → Pressão",
            "Pressão → Temperatura"
        ],
        horizontal=True
    )

    st.divider()

    # --------------------------------------------------------
    # Temperatura para pressão
    # --------------------------------------------------------

    if operacao == "Temperatura → Pressão":

        col1, col2 = st.columns(2)

        with col1:
            T = st.number_input(
                "Temperatura:",
                min_value=200.0,
                max_value=1000.0,
                value=373.15,
                step=1.0
            )

            unidade_T = st.selectbox(
                "Unidade da temperatura:",
                ["K", "°C"]
            )

        if unidade_T == "°C":
            T_K = T + 273.15
        else:
            T_K = T

        if st.button("Calcular pressão", type="primary"):

            p_mmhg = pressao_saturacao(T_K)

            with col2:
                st.metric(
                    "Temperatura em Kelvin",
                    f"{T_K:.2f} K"
                )

                st.metric(
                    "Pressão de saturação",
                    f"{p_mmhg:.4f} mmHg"
                )

                st.write(
                    f"**Pressão em kPa:** "
                    f"{converter_mmhg(p_mmhg, 'kPa'):.4f} kPa"
                )

                st.write(
                    f"**Pressão em bar:** "
                    f"{converter_mmhg(p_mmhg, 'bar'):.6f} bar"
                )

                st.write(
                    f"**Pressão em atm:** "
                    f"{converter_mmhg(p_mmhg, 'atm'):.6f} atm"
                )

    # --------------------------------------------------------
    # Pressão para temperatura
    # --------------------------------------------------------

    else:

        col1, col2 = st.columns(2)

        with col1:

            pressao = st.number_input(
                "Pressão:",
                min_value=0.001,
                value=760.0,
                step=1.0
            )

            unidade_P = st.selectbox(
                "Unidade da pressão:",
                ["mmHg", "kPa", "bar", "atm"]
            )

        if st.button("Calcular temperatura", type="primary"):

            p_mmhg = converter_pressao_para_mmhg(
                pressao,
                unidade_P
            )

            T_K = temperatura_da_pressao(p_mmhg)
            T_C = T_K - 273.15

            with col2:

                st.metric(
                    "Temperatura",
                    f"{T_K:.2f} K"
                )

                st.metric(
                    "Temperatura",
                    f"{T_C:.2f} °C"
                )

                st.write(
                    f"**Pressão utilizada:** "
                    f"{p_mmhg:.4f} mmHg"
                )


# ============================================================
# 2 - GÁS IDEAL
# ============================================================

elif modulo == "Gás ideal":

    st.header("💨 Equação dos Gases Ideais")

    st.latex(r"PV = mRT")

    st.write(
        "Calcule uma das propriedades utilizando "
        "a equação dos gases ideais."
    )

    grandeza = st.selectbox(
        "O que deseja calcular?",
        [
            "Pressão (P)",
            "Volume (V)",
            "Massa (m)",
            "Temperatura (T)"
        ]
    )

    col1, col2 = st.columns(2)

    with col1:

        R = st.number_input(
            "Constante dos gases R:",
            value=0.287,
            step=0.001,
            format="%.4f",
            help="Para ar: R ≈ 0,287 kJ/(kg·K)"
        )

        if grandeza != "Pressão (P)":
            P = st.number_input(
                "Pressão P (kPa):",
                min_value=0.001,
                value=100.0
            )

        if grandeza != "Volume (V)":
            V = st.number_input(
                "Volume V (m³):",
                min_value=0.001,
                value=1.0
            )

        if grandeza != "Massa (m)":
            m = st.number_input(
                "Massa m (kg):",
                min_value=0.001,
                value=1.0
            )

        if grandeza != "Temperatura (T)":
            T = st.number_input(
                "Temperatura T (K):",
                min_value=0.1,
                value=300.0
            )

    if st.button("Calcular", type="primary"):

        if grandeza == "Pressão (P)":
            resultado = m * R * T / V
            unidade = "kPa"

        elif grandeza == "Volume (V)":
            resultado = m * R * T / P
            unidade = "m³"

        elif grandeza == "Massa (m)":
            resultado = P * V / (R * T)
            unidade = "kg"

        else:
            resultado = P * V / (m * R)
            unidade = "K"

        with col2:
            st.success(
                f"Resultado: **{resultado:.6f} {unidade}**"
            )


# ============================================================
# 3 - PRIMEIRA LEI
# ============================================================

elif modulo == "Primeira Lei da Termodinâmica":

    st.header("⚙️ Primeira Lei da Termodinâmica")

    st.latex(r"\Delta U = Q - W")

    st.write(
        "Determine a variação da energia interna, "
        "o calor ou o trabalho."
    )

    calcular = st.selectbox(
        "O que deseja calcular?",
        [
            "ΔU",
            "Q",
            "W"
        ]
    )

    col1, col2 = st.columns(2)

    with col1:

        if calcular != "ΔU":
            Q = st.number_input(
                "Calor Q (kJ):",
                value=0.0
            )

        if calcular != "Q":
            W = st.number_input(
                "Trabalho W (kJ):",
                value=0.0
            )

        if calcular != "W":
            dU = st.number_input(
                "Variação de energia interna ΔU (kJ):",
                value=0.0
            )

    if st.button("Calcular", type="primary"):

        if calcular == "ΔU":
            resultado = Q - W
            unidade = "kJ"

        elif calcular == "Q":
            resultado = dU + W
            unidade = "kJ"

        else:
            resultado = Q - dU
            unidade = "kJ"

        with col2:
            st.success(
                f"Resultado: **{resultado:.4f} {unidade}**"
            )


# ============================================================
# 4 - CALOR SENSÍVEL
# ============================================================

elif modulo == "Calor sensível":

    st.header("🔥 Calor Sensível")

    st.latex(r"Q = mc(T_2-T_1)")

    m = st.number_input(
        "Massa m (kg):",
        min_value=0.001,
        value=1.0
    )

    c = st.number_input(
        "Calor específico c (kJ/kg·K):",
        min_value=0.001,
        value=4.18
    )

    T1 = st.number_input(
        "Temperatura inicial T₁ (°C):",
        value=20.0
    )

    T2 = st.number_input(
        "Temperatura final T₂ (°C):",
        value=100.0
    )

    if st.button("Calcular calor", type="primary"):

        Q = m * c * (T2 - T1)

        st.success(
            f"Calor necessário: **{Q:.4f} kJ**"
        )

        if Q > 0:
            st.info("O sistema recebeu calor.")

        elif Q < 0:
            st.info("O sistema perdeu calor.")

        else:
            st.info("Não houve transferência líquida de calor.")


# ============================================================
# 5 - MÁQUINA DE CARNOT
# ============================================================

elif modulo == "Máquina de Carnot":

    st.header("♻️ Máquina de Carnot")

    st.latex(r"\eta = 1-\frac{T_c}{T_h}")

    Th = st.number_input(
        "Temperatura da fonte quente Th (K):",
        min_value=0.1,
        value=600.0
    )

    Tc = st.number_input(
        "Temperatura da fonte fria Tc (K):",
        min_value=0.1,
        value=300.0
    )

    if st.button("Calcular rendimento", type="primary"):

        if Tc >= Th:
            st.error(
                "A temperatura da fonte fria deve ser menor "
                "que a temperatura da fonte quente."
            )
        else:

            eficiencia = 1 - Tc / Th

            st.success(
                f"Rendimento de Carnot: "
                f"**{eficiencia * 100:.2f}%**"
            )


# ============================================================
# 6 - PROCESSO ISENTRÓPICO
# ============================================================

else:

    st.header("🔄 Processo Isentrópico")

    st.latex(
        r"\frac{T_2}{T_1}"
        r"="
        r"\left(\frac{P_2}{P_1}\right)"
        r"^{\frac{\gamma-1}{\gamma}}"
    )

    T1 = st.number_input(
        "Temperatura inicial T₁ (K):",
        min_value=0.1,
        value=300.0
    )

    P1 = st.number_input(
        "Pressão inicial P₁ (kPa):",
        min_value=0.001,
        value=100.0
    )

    P2 = st.number_input(
        "Pressão final P₂ (kPa):",
        min_value=0.001,
        value=500.0
    )

    gamma = st.number_input(
        "Razão de calores específicos γ:",
        min_value=1.001,
        value=1.4,
        step=0.01
    )

    if st.button("Calcular temperatura final", type="primary"):

        T2 = T1 * (P2 / P1) ** (
            (gamma - 1) / gamma
        )

        st.success(
            f"Temperatura final: **{T2:.4f} K**"
        )

        st.write(
            f"Temperatura final em °C: "
            f"**{T2 - 273.15:.4f} °C**"
        )


# ============================================================
# RODAPÉ
# ============================================================

st.divider()

st.caption(
    "🌡️ ThermoCalc • Desenvolvido por Horacio Arcenio Mbombi"
)

st.caption(
    "Calculadora de Termodinâmica para estudantes e engenharia. "
    "Verifique sempre as hipóteses e as unidades utilizadas."
)
