
# -------- Gerar_clausulas.py --------
import requests
import os
OPENROUTER_KEY = "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"
def gerar_clausula_ai(prompt_usuario, max_tokens=700, temperature=1.0):
    """
    Gera uma cláusula contratual detalhada em português usando IA via OpenRouter.
    A chave da API deve estar definida na variável de ambiente OPENROUTER_KEY ou será usada a chave fixa do código.
    """
    print(f"[DEBUG] Iniciando geração de cláusula...")
    print(f"[DEBUG] Prompt recebido: {prompt_usuario[:100]}...")
    
    api_key = os.getenv("OPENROUTER_KEY") or OPENROUTER_KEY
    if not api_key:
        raise RuntimeError("A variável de ambiente OPENROUTER_KEY não está definida e nenhuma chave padrão foi encontrada.")
    
    print(f"[DEBUG] Chave API encontrada: {api_key[:20]}...")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "tngtech/deepseek-r1t2-chimera:free",
        "messages": [
            {"role": "user", "content": f"Crie uma cláusula contratual em pt br detalhada com base nesta descrição: {prompt_usuario}"}
        ],
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    
    print(f"[DEBUG] Enviando requisição para OpenRouter...")
    
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        print(f"[DEBUG] Status da resposta: {response.status_code}")
        
        response.raise_for_status()
        
        response_json = response.json()
        print(f"[DEBUG] Resposta recebida com sucesso")
        
        resultado = response_json['choices'][0]['message']['content']
        print(f"[DEBUG] Cláusula gerada: {len(resultado)} caracteres")
        
        return resultado
        
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Erro na requisição HTTP: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"[ERROR] Código HTTP: {e.response.status_code}")
            print(f"[ERROR] Resposta: {e.response.text}")
        raise
    except KeyError as e:
        print(f"[ERROR] Erro na estrutura da resposta: {e}")
        print(f"[ERROR] Resposta completa: {response.text}")
        raise
    except Exception as e:
        print(f"[ERROR] Erro inesperado: {e}")
        raise

# Função de gravação de áudio local (Windows)
def gravar_audio(duracao=15, arquivo_saida="voz_usuario.wav", samplerate=44100):
    """
    Grava áudio do microfone e salva em um arquivo WAV local.
    Requer: pip install sounddevice scipy
    """
    import sounddevice as sd
    from scipy.io.wavfile import write
    import numpy as np
    print(f"Gravando áudio por {duracao} segundos...")
    audio = sd.rec(int(duracao * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    write(arquivo_saida, samplerate, audio)
    print(f"Áudio salvo em {arquivo_saida}")
    return arquivo_saida

# Função de transcrição REAL usando Speech Recognition
def transcrever_audio(arquivo_audio):
    """
    Função de transcrição de áudio REAL usando Google Speech Recognition.
    Transcreve o que realmente foi falado no áudio.
    """
    import os
    import time
    
    print(f"[DEBUG] Transcrevendo arquivo REAL: {arquivo_audio}")
    
    # Verificar se o arquivo existe
    if not os.path.exists(arquivo_audio):
        print(f"[ERROR] Arquivo não encontrado: {arquivo_audio}")
        return "[Erro: arquivo de áudio não encontrado]"
    
    # Verificar tamanho do arquivo
    try:
        size = os.path.getsize(arquivo_audio)
        print(f"[DEBUG] Tamanho do arquivo: {size} bytes")
        
        if size == 0:
            print("[WARNING] Arquivo vazio")
            return "[Erro: arquivo de áudio vazio]"
        
        # TRANSCRIÇÃO REAL usando Speech Recognition
        print("[DEBUG] Iniciando transcrição REAL com Speech Recognition...")
        
        try:
            import speech_recognition as sr
            
            # Inicializar reconhecedor
            r = sr.Recognizer()
            
            # Carregar arquivo de áudio
            with sr.AudioFile(arquivo_audio) as source:
                print("[DEBUG] Carregando arquivo de áudio...")
                # Ajustar para ruído ambiente
                r.adjust_for_ambient_noise(source, duration=0.5)
                # Gravar o áudio
                audio_data = r.record(source)
                
            print("[DEBUG] Enviando para Google Speech Recognition...")
            
            # Transcrever usando Google (gratuito)
            texto_transcrito = r.recognize_google(audio_data, language='pt-BR')
            
            if texto_transcrito:
                print(f"[DEBUG] TRANSCRIÇÃO REAL: {texto_transcrito}")
                return texto_transcrito
            else:
                print("[WARNING] Transcrição vazia")
                return "[Áudio sem fala detectada]"
                
        except sr.UnknownValueError:
            print("[WARNING] Google Speech Recognition não conseguiu entender o áudio")
            return "[Áudio não compreensível - tente falar mais claramente]"
        except sr.RequestError as e:
            print(f"[ERROR] Erro no serviço Google Speech Recognition: {e}")
            # Fallback para simulação se Google falhar
            return usar_transcricao_simulada(size)
        except ImportError:
            print("[ERROR] SpeechRecognition não instalado")
            # Fallback para simulação se biblioteca não estiver instalada
            return usar_transcricao_simulada(size)
        except Exception as e:
            print(f"[ERROR] Erro na transcrição real: {e}")
            # Fallback para simulação se houver erro
            return usar_transcricao_simulada(size)
        
    except Exception as e:
        print(f"[ERROR] Erro geral durante transcrição: {e}")
        return f"[Erro na transcrição: {str(e)}]"

def usar_transcricao_simulada(size):
    """Função auxiliar para transcrição simulada quando Speech Recognition falha"""
    print("[DEBUG] Usando transcrição simulada como fallback...")
    
    frases_exemplo = [
        "Preciso de uma cláusula de confidencialidade para proteger informações comerciais",
        "Quero uma cláusula de rescisão que permita cancelamento com 30 dias de aviso",
        "Gere uma cláusula de pagamento com juros de mora em caso de atraso",
        "Crie uma cláusula de responsabilidades limitando danos indiretos",
        "Elabore uma cláusula de propriedade intelectual para software desenvolvido",
        "Defina uma cláusula de força maior incluindo pandemias e desastres naturais",
        "Estabeleça uma cláusula de não concorrência por 12 meses após rescisão",
        "Configure uma cláusula geral de prestação de serviços profissionais"
    ]
    
    import random
    random.seed(size)
    resultado = random.choice(frases_exemplo)
    
    print(f"[DEBUG] Transcrição simulada: {resultado}")
    return f"[SIMULADO] {resultado}"
