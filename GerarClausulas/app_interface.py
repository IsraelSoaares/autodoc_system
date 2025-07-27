import streamlit as st
from datetime import datetime
import pyaudio
import wave
import threading
try:
    from Gerar_clausulas import gerar_clausula_ai, transcrever_audio
except ImportError as e:
    st.error(f"Erro ao importar módulos: {e}")

# Configuração da página
st.set_page_config(
    page_title="AutoDoc AI - Gerador de Cláusulas",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    .success-card {
        background: linear-gradient(90deg, #56ab2f 0%, #a8e6cf 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: white;
    }
    .record-button {
        background: linear-gradient(90deg, #ff6b6b 0%, #ee5a52 100%);
        border: none;
        color: white;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-size: 1.2rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    .sidebar-content {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


# --- INÍCIO DA INTERFACE FUNCIONAL ---
st.markdown('<div class="feature-card">', unsafe_allow_html=True)
tipo_clausula = st.selectbox(
    "Tipo de cláusula:",
    [
        "Geral",
        "Confidencialidade",
        "Rescisão",
        "Pagamento",
        "Responsabilidades",
        "Força Maior",
        "Propriedade Intelectual",
        "Não Concorrência"
    ]
)

modo_entrada = st.radio("Modo de entrada:", ["💬 Texto", "🎤 Áudio"], horizontal=True)
texto_input = ""

if modo_entrada == "💬 Texto":
    st.markdown("**Digite sua descrição:**")
    texto_input = st.text_area(
        "",
        placeholder="Ex: Preciso de uma cláusula que proteja informações confidenciais compartilhadas durante o projeto...",
        height=150,
        key="texto_input"
    )
elif modo_entrada == "🎤 Áudio":
    st.markdown("**🎤 Gravação Simplificada - Grave e processe automaticamente:**")
    
    # Configurações de áudio
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 5  # Gravar por 5 segundos
    
    # Estados de gravação
    if "audio_gravado" not in st.session_state:
        st.session_state.audio_gravado = False
    if "transcricao_pronta" not in st.session_state:
        st.session_state.transcricao_pronta = ""
    
    def gravar_audio_simples():
        """Grava áudio por tempo fixo e retorna os frames"""
        try:
            p = pyaudio.PyAudio()
            stream = p.open(format=FORMAT,
                           channels=CHANNELS,
                           rate=RATE,
                           input=True,
                           frames_per_buffer=CHUNK)
            
            st.info("🔴 Gravando por 5 segundos... FALE AGORA!")
            
            frames = []
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK, exception_on_overflow=False)
                frames.append(data)
            
            stream.stop_stream()
            stream.close()
            p.terminate()
            
            # Salvar arquivo
            filename = "audio_gravado.wav"
            wf = wave.open(filename, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            
            return filename
            
        except Exception as e:
            st.error(f"Erro na gravação: {e}")
            return None
    
    # Interface mais simples
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎤 Gravar Áudio (5s)", key="record_button"):
            with st.spinner("🎤 Preparando gravação..."):
                filename = gravar_audio_simples()
                
                if filename:
                    st.success("✅ Gravação concluída!")
                    
                    # Transcrever imediatamente
                    with st.spinner("📝 Transcrevendo áudio..."):
                        texto_transcrito = transcrever_audio(filename)
                        st.session_state.transcricao_pronta = texto_transcrito
                        st.session_state.texto_input_audio = texto_transcrito
                        st.session_state.audio_gravado = True
                    
                    st.success(f"📝 Transcrição: {texto_transcrito}")
    
    with col2:
        if st.button("🤖 Gerar Cláusula", key="generate_clause", disabled=not st.session_state.audio_gravado):
            if st.session_state.transcricao_pronta:
                with st.spinner("🤖 Gerando cláusula com IA..."):
                    try:
                        prompt_personalizado = f"""
Tipo de cláusula: {tipo_clausula}
Descrição (por áudio): {st.session_state.transcricao_pronta}
\nPor favor, gere uma cláusula contratual profissional e detalhada.
"""
                        clausula = gerar_clausula_ai(prompt_personalizado)
                        st.session_state.ultima_clausula = clausula
                        st.session_state.clausulas_geradas = st.session_state.get('clausulas_geradas', 0) + 1
                        st.success("✅ Cláusula gerada com sucesso!")
                        
                        # Resetar para nova gravação
                        st.session_state.audio_gravado = False
                        st.session_state.transcricao_pronta = ""
                        
                    except Exception as e:
                        st.error(f"Erro ao gerar cláusula: {e}")
    
    # Mostrar status
    if st.session_state.audio_gravado:
        st.success("✅ Áudio gravado e transcrito! Clique em 'Gerar Cláusula' para continuar.")
    else:
        st.info("🎤 Clique em 'Gravar Áudio' para começar.")
    
    # Área de transcrição
    texto_input = st.text_area(
        "📝 Texto transcrito (edite se necessário):",
        value=st.session_state.get("texto_input_audio", ""),
        height=120,
        key="texto_input_audio",
        placeholder="O texto transcrito do seu áudio aparecerá aqui..."
    )
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("### 🚀 Ações")
st.markdown('<div class="feature-card">', unsafe_allow_html=True)

# Botão apenas para modo texto (modo áudio tem seus próprios botões)
if modo_entrada == "💬 Texto":
    if st.button("✨ Gerar Cláusula", disabled=not texto_input):
        if texto_input:
            with st.spinner("🤖 Gerando cláusula com IA..."):
                try:
                    prompt_personalizado = f"""
Tipo de cláusula: {tipo_clausula}
Descrição: {texto_input}
\nPor favor, gere uma cláusula contratual profissional e detalhada.
"""
                    clausula = gerar_clausula_ai(prompt_personalizado)
                    st.session_state.ultima_clausula = clausula
                    st.session_state.clausulas_geradas = st.session_state.get('clausulas_geradas', 0) + 1
                    st.success("✅ Cláusula gerada com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao gerar cláusula: {e}")
else:
    # Para modo áudio, mostrar informações
    st.info("🎤 **Modo Áudio**: Use os botões 'Gravar Áudio' e 'Gerar Cláusula' acima")

# Botão limpar sempre disponível
if st.button("🔄 Limpar Tudo"):
    # Limpar específicamente para cada modo
    if modo_entrada == "🎤 Áudio":
        st.session_state.audio_gravado = False
        st.session_state.transcricao_pronta = ""
    st.session_state.clear()
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Exibir cláusula gerada, se houver
if 'ultima_clausula' in st.session_state:
    st.markdown("### 📄 Cláusula Gerada")
    st.code(st.session_state.ultima_clausula, language=None)



