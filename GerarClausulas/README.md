# 🤖 AutoDoc AI - Sistema de Geração de Cláusulas Contratuais

Sistema simplificado que usa IA para gerar cláusulas contratuais automaticamente com base em descrições por texto ou voz.

## ✨ Como Usar

### 💻 **No Computador** 
Duplo-clique em: `main.py`

### 📱 **No Celular (mesma rede Wi-Fi)**
Duplo-clique em: `FACIL.bat`
> Mostra o link para acessar no celular

### 🌍 **No Celular (qualquer lugar)**
Duplo-clique em: `CELULAR.bat`  
> Cria um túnel público para acesso de qualquer lugar

### 🛑 **Para Fechar o Servidor**
Duplo-clique em: `FECHAR.bat`

## 🎯 Funcionalidades

- ✅ **Texto**: Digite sua solicitação
- ✅ **Voz**: Grave 5 segundos de áudio (clique em "Gravar")
- ✅ **IA Avançada**: Usa modelo `deepseek-r1t2-chimera`
- ✅ **Interface Mobile**: Funciona perfeitamente no celular

## ⚙️ Primeira Configuração

1. **Instalar dependências**: Duplo-clique em `install_deps.bat`

2. **Configurar API**: 
   - Abra `Gerar_clausulas.py` no bloco de notas
   - Na linha 6, substitua `"SUA_CHAVE_AQUI"` pela sua chave do OpenRouter
   - Obtenha grátis em: https://openrouter.ai/

## 📁 Arquivos do Sistema

```
📂 GerarClausulas/
├── 🎯 main.py              # ← Executar aqui (principal)
├── 🌐 app_interface.py     # Interface web
├── 🤖 Gerar_clausulas.py   # IA e transcrição  
├── 🔧 install_deps.bat     # Instalar dependências
├── 📱 FACIL.bat           # Acesso local (Wi-Fi)
├── 🌍 CELULAR.bat         # Acesso público
├── 🛑 FECHAR.bat          # Fechar servidor
├── 📦 requirements.txt     # Lista de dependências
└── 📖 README.md           # Este arquivo
```

## 🆘 Solução de Problemas

**Erro de microfone?** → Execute `install_deps.bat` novamente

**Não gera cláusulas?** → Verifique se configurou a chave da API

**Não abre no celular?** → Use `CELULAR.bat` em vez de `FACIL.bat`
