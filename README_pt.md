**Última atualização:** 21/08/2026

# 📺 TV Channel Editor

> **Editor de listas de canais de TV multimarcas** — Uma única plataforma para Samsung, LG, Sony, Hisense e muito mais.

[![Demonstração ao vivo](https://img.shields.io/badge/🌐_Canlı_Demo-tvchanneleditor.onrender.com-blue)](https://tvchanneleditor.onrender.com)
[![Licença: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENÇA)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue)](https://python.org)

---

## 🎯 O que faz?

Pode editar visualmente no navegador, através de **arrastar e largar**, o ficheiro com a lista de canais que a sua televisão transferiu para a porta USB e, em seguida, carregá-lo novamente na televisão. **Os dados são armazenados apenas temporariamente (RAM/Temp) durante o processo, não sendo guardados de forma permanente.**

---

## 📺 Marcas de televisores compatíveis

| Marca | Formato | Estado |
|-------|--------|-------|
| **Samsung** (Séries E/F/H) | `.scm` | ✅ Suporte total |
| **Samsung** (J/K/M/Q/R/T - Tizen) | `.zip` (SQLite) | ✅ Suporte total |
| **LG** (webOS 5+) | `.tll` (XML) | ✅ Suporte total |
| **Sony BRAVIA** | `sdb.xml` | ✅ Suporte completo |
| **Hisense** (2017+) | `servicelist.db` | ✅ Suporte completo |
| **Panasonic VIERA** | `svl.db / svl.bin` | 🔄 Beta |
| Philips, Toshiba, Grundig... | `*.db / *.xml` | 🔜 Em breve |

## 🛰️ Satélites suportados

**Türksat 4A/5B** · **Hotbird 13E** · **Astra 19.2E** · e todos os outros satélites DVB-S

---

## ✨ Funcionalidades

- **🪄 Varinha Mágica** — Aplica os modelos Geral / Notícias / Desporto com um único clique
- **🛠️ Criador de Modelos** — Cria e guarda a tua lista ideal
- **📱 Transferência para o dispositivo através de código** — Transfira facilmente a lista de canais do telemóvel, ao lado da TV, para o computador através de um código de 8 caracteres
- **🔍 Verificação automática de frequências** — Deteta automaticamente frequências antigas ou erradas (Türksat)
- **⭐ Favoritos e Bloqueio** — Organização dos Favoritos 1-5 e do bloqueio infantil
- **🗑️ Ações em massa** — Apague em massa canais codificados, estações de rádio ou itens selecionados
- **🌙 Tema Escuro/Claro e 👁️ Modo de daltonismo** — Interface acessível a todos
- **🌐 11 opções de idioma** — Suporte para turco e inglês
- **📊 Privacidade total (análise sem cookies)** — Estatísticas integradas que não utilizam cookies nem dados pessoais
- **📱 Totalmente responsivo** — Compatível com computador, tablet e telemóvel

---

## 🚀 Utilização em tempo real

Utilize diretamente no navegador, sem necessidade de instalação:

👉 **[tvchanneleditor.onrender.com](https://tvchanneleditor.onrender.com)**

---

## 💻 Instalação Local

```bash
git clone https://github.com/tarihcituranx/TVChanneleditor.git
cd TVChanneleditor
pip install -r requirements.txt
python3 app.py
```

Aceda ao endereço `http://127.0.0.1:5000` no navegador.

---

## 🏗️ Estrutura do projeto

```
├── app.py # Aplicação principal do Flask e cabeçalhos de segurança
├── scm_core.py # Motor SCM (binário) da Samsung
├── tizen_core.py # Motor SQLite do Tizen da Samsung
├── lg_core.py # Motor XML do GlobalClone da LG
├── sony_core.py # Motor sdb.xml da Sony
├── hisense_core.py     # Motor SQLite da Hisense
├── templates/ # Modelos HTML do Jinja2 (11 idiomas)
├── static/
│   ├── css/style.css   # Tema escuro/claro + todos os estilos
│   ├── js/app.js # Frontend (arrastar e largar, renderização de canais, modelo)
│   └── data/ # frequências.json, modelos.json
```

---

## 🔐 Segurança

- Todos os cabeçalhos de segurança estão ativos (CSP, HSTS, CORP, COOP, Referrer-Policy...)
- Limite de tamanho de ficheiro: 2 MB
- Os ficheiros carregados são eliminados após serem processados
- Nenhum dado dos canais é registado no servidor
- Contacto de segurança: `tarihcituranx@proton.me`

---

## 🤖 Guia de Inteligência Artificial

Se estiver a desenvolver com o assistente de IA, leia o ficheiro [AI_INSTRUCTIONS.md](AI_INSTRUCTIONS.md).

---

## 🔌 Utilização da API para Desenvolvedores e dos Agentes de IA (Developer API)

Este projeto não é apenas um site, mas também foi concebido como uma **REST API** completa, que pode ser utilizada diretamente por agentes de inteligência artificial (AI Agents) e por desenvolvedores através de código.

> 🧑‍💻 **Para programadores:** Pode consultar a documentação interativa do Swagger UI em [tvchanneleditor.onrender.com/api/docs](https://tvchanneleditor.onrender.com/api/docs).
> 
> 🤖 **Para Agentes de IA (ChatGPT, Claude, etc.):** Pode fornecer à IA o esquema OpenAPI em texto simples (Plain-Text), legível por máquina, através desta ligação: [tvchanneleditor.onrender.com/api/openapi.txt](https://tvchanneleditor.onrender.com/api/openapi.txt)



### Verificação da Versão e da Implementação (Version Check)
Para verificar instantaneamente se o servidor de renderização publicou o commit mais recente do GitHub ou se ainda se encontra no cache:
```bash
curl -sS https://tvchanneleditor.onrender.com/api/version
```
```json
{
  "status": "online",
  "version": "1.0.0",
  "commit": "abc1234...",
  "deployed_at": "2026-08-21T19:00:51.123Z"
}
```

---

## 🙏 Obrigado

- **[İltekin/scm-editor](https://github.com/iltekin/scm-editor)** — Primeira fonte de inspiração
- **[PredatH0r/ChanSort](https://github.com/PredatH0r/ChanSort)** — Referência de engenharia inversa para SCM + formatos de várias marcas
- **[Türksat Uydu](https://uydu.turksat.com.tr/)** — Base de dados de verificação de frequências da Türksat

---

## 📄 Licença

Disponibilizado como código aberto ao abrigo da Licença MIT.

> «Samsung», «LG», «Sony», «Hisense», «Panasonic» e os respetivos logótipos são marcas registadas das empresas em questão. Esta é uma ferramenta comunitária independente e de código aberto.
