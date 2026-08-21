[🇹🇷 TR](README.md) | [🇺🇸 EN](README_en.md) | [🇩🇪 DE](README_de.md) | [🇷🇺 RU](README_ru.md) | [🇪🇸 ES](README_es.md) | [🇮🇹 IT](README_it.md) | [🇫🇷 FR](README_fr.md) | [🇸🇦 AR](README_ar.md) | [🇮🇷 FA](README_fa.md) | [🇦🇿 AZ](README_az.md) | [🇵🇹 PT](README_pt.md)

**Última atualização:** 21/08/2026

# 📺 Editor de Canais de TV

> **Editor de listas de canais de TV multimarcas** — Edite as suas listas de canais de TV Samsung, LG, Sony e Hisense através do navegador.

[![Demonstração ao vivo](https://img.shields.io/badge/🌐_Canlı_Demo-tvchanneleditor.onrender.com-blue)](https://tvchanneleditor.onrender.com)
[![Documentação da API](https://img.shields.io/badge/API-Swagger_UI-orange)](https://tvchanneleditor.onrender.com/api/docs)
[![CI](https://github.com/tarihcituranx/TVChanneleditor/actions/workflows/test.yml/badge.svg)](https://github.com/tarihcituranx/TVChanneleditor/actions)
[![Licença: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue)](https://python.org)

---

## ✨ Para que serve?

É uma ferramenta de código aberto que permite editar visualmente, no seu navegador, o ficheiro da lista de canais que a sua televisão transfere para uma pen USB, utilizando o método **arrastar e largar**. Não requer instalação, funciona diretamente no navegador ou através da API REST.

## 👤 Quem pode utilizar?

- Quem pretenda editar a lista de canais da TV Samsung a partir do computador
- Quem pretenda editar ficheiros XML `.tll` do LG GlobalClone
- Quem trabalhe com listas `sdb.xml` da Sony e `servicelist.db` da Hisense
- Desenvolvedores que pretendam alterar a lista de canais de forma programática
- Quem pretenda automatizar a lista de canais com agentes de inteligência artificial (AI Agent)

## 📺 Formatos suportados (Matriz de compatibilidade)

| Formato | Leitura | Edição | Recriação | Nota |
|--------|:---:|:---:|:---:|-----|
| **Samsung `.scm`** | ✅ | ✅ | ✅ | Séries E/F/H (Binário) |
| **Samsung Tizen `.zip`** | ✅ | ✅ | ✅ | Séries J/K/M/Q/R/T (SQLite) |
| **Sony `sdb.xml`** | ✅ | ✅ | ✅ | Série BRAVIA |
| **Hisense `servicelist.db`** | ✅ | ✅ | ✅ | Modelos de 2017 e 2021 |
| **LG XML `.tll`** | ✅ | ✅ | ✅ | Apenas GlobalClone XML (não é suportado em binário) |
| **Panasonic `svl.*`** | 🔜 | 🔜 | 🔜 | Planeado / Em fase de desenvolvimento |

> **⚠️ Nota importante sobre a compatibilidade com a LG:** Os ficheiros **binários .tll** da geração anterior da LG não são suportados. Apenas os ficheiros `.tll` da nova geração, baseados em XML (GlobalClone), podem ser processados. Para os ficheiros antigos, é necessário utilizar a aplicação para computador *ChanSort*.


## ⚠️ Restrições importantes

Antes de utilizar, tenha em conta as seguintes limitações técnicas:
- **LG Binary TLL:** Os ficheiros binários `.tll` de geração anterior não são suportados.
- **Panasonic SVL:** O suporte está em fase de desenvolvimento (previsto).
- **Verificação de frequência:** Está ativa apenas para dados do satélite Türksat.
- **Limite de tamanho do ficheiro:** Os ficheiros carregados podem ter, no máximo, **2 MB**.
- **Sessão temporária:** Os ficheiros não são guardados de forma permanente, sendo automaticamente apagados no final da sessão.

## 🚀 Início rápido

1. **Transferir da TV para a USB:** A partir do menu da TV (Transmissão > Definições Avançadas), transfira a lista de canais para uma USB formatada em FAT32.
2. **Carregar:** Arraste e solte o ficheiro da USB no site.
3. **Editar:** Ordene os itens com a função arrastar e largar, elimine os itens desnecessários ou utilize os 💡 Modelos Inteligentes.
4. **Descarregar:** Descarregue o ficheiro editado de volta para o seu computador.
5. **Carregue na TV:** Volte a ligar a pen USB à TV e importe a nova lista.

## 🛰️ Suporte a satélites e frequências

As listas de canais **DVB-S/S2** podem ser processadas sem problemas em termos de formato. **A funcionalidade de verificação automática de frequências (detecção de frequências antigas/erradas) está atualmente ativa apenas para dados do Türksat 4A/5B.** Outros satélites (Hotbird, Astra, etc.) são totalmente suportados para ordenação e edição.

---

## 🔌 Como funciona a API para programadores (REST)?

Existe um fluxo simples de 3 passos para agentes de IA e programadores. Para mais detalhes, consulte as ligações [Swagger UI](https://tvchanneleditor.onrender.com/api/docs) ou [Esquema OpenAPI](https://tvchanneleditor.onrender.com/api/openapi.txt).

**Passo 1: Carregamento (Upload)**
```http
POST /upload
Content-Type: multipart/form-data
```
*(Retorna como resposta um `session_id` e uma lista JSON dos canais)*

**Passo 2: Compilação (Build)**
```http
POST /build
Content-Type: application/json
{
  "session_id": "uuid-...",
  "channels": [ ... lista organizada ... ]
}
```
*(A resposta devolve o link `/download/...` onde o ficheiro pode ser descarregado)*

**Passo 3: Descarregar (Download)**
```http
GET /download/{session_id}/{filename}
```
*(O ficheiro binário/arquivo editado é descarregado)*

## 🔐 Privacidade e Segurança

- Existe um limite de tamanho de ficheiro de **2 MB**.
- **Os ficheiros não são armazenados permanentemente no servidor.** Os ficheiros carregados são processados no armazenamento temporário do servidor durante a sessão de edição, não são arquivados permanentemente e são automaticamente eliminados na totalidade quando a sessão expira (cerca de 1 hora).
- Não há qualquer registo de conta, adesão ou base de dados.
- As operações de análise de XML na API (contra ataques «Billion Laughs») estão protegidas pelo `defusedxml`.

## 🧪 Sistema de Testes (CI)

O projeto possui uma arquitetura de testes **Round-Trip (Ida e Volta)**.
- Utilizando ficheiros de teste do mundo real (fixtures), verifica-se se o código do motor, mesmo quando corrompido ou alterado, não corrompe as estruturas originais da base de dados de TV.
- Em cada operação `push` e `PR`, o ficheiro `tests/test_roundtrip.py` é executado automaticamente no GitHub Actions.

## 🌍 Suporte Linguístico

A interface e os manuais de utilização estão disponíveis em **11 idiomas**: turco, inglês, alemão, russo, espanhol, italiano, francês, árabe, persa, azerbaijano e português.

## 🏗️ Estrutura do projeto

```
├── app.py # Servidor Flask, rotas da API e i18n
├── scm_core.py # Motor SCM da Samsung
├── tizen_core.py # Motor SQLite da Samsung Tizen
├── lg_core.py # Motor XML da LG
├── sony_core.py # Motor XML da Sony
├── hisense_core.py     # Motor SQLite da Hisense
├── templates/ # Interfaces HTML Jinja2 (11 idiomas)
├── static/ # CSS, JS, esquemas YAML da OpenAPI
└── tests/
    ├── test_roundtrip.py  # Testes de ida e volta para todos os motores
    └── fixtures/ # Exemplos reais de bases de dados de TV para os testes
```

## 🙏 Agradecimentos

- **[İltekin/scm-editor](https://github.com/iltekin/scm-editor)** — Primeira fonte de inspiração
- **[PredatH0r/ChanSort](https://github.com/PredatH0r/ChanSort)** — Referência de engenharia reversa para formatos de várias marcas
- **[Türksat Uydu](https://uydu.turksat.com.tr/)** — Base de dados de frequências da Türksat

## 📄 Licença

Disponibilizado como código aberto sob a Licença MIT.
> «Samsung», «LG», «Sony», «Hisense», «Panasonic» e os respetivos logótipos são marcas registadas das respetivas empresas. Esta é uma ferramenta comunitária independente e de código aberto.
