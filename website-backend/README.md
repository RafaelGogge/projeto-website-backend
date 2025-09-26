# RhythmBox - Spotify CRUD Web App

## Visão Geral
RhythmBox é um aplicativo web para busca, favoritos e gerenciamento de playlists do Spotify, com backend em Python/Flask e frontend moderno, responsivo e interativo.

---

## Tecnologias Utilizadas

### Backend
- **Python 3.13**  
  Linguagem principal do backend.
- **Flask**  
  Framework web para rotas, views e API.
- **Spotipy**  
  Integração com a API do Spotify.
- **python-dotenv**  
  Gerenciamento de variáveis de ambiente.
- **requests**  
  Requisições HTTP auxiliares.

### Frontend
- **Bootstrap 5**  
  Framework CSS para layout responsivo e componentes visuais.  
  **Utilizado em:** Todas as páginas (`index.html`, `favoritos.html`, `playlists.html`).
- **SweetAlert2**  
  Alertas e modais modernos para feedback ao usuário.  
  **Utilizado em:** Todas as páginas para confirmações, mensagens de sucesso/erro.
- **Axios**  
  Cliente HTTP para requisições AJAX.  
  **Utilizado em:** `index.html` (favoritar música), `playlists.html` (criar playlist via AJAX).

### Estrutura de Pastas
- **/templates/**  
  HTML das páginas (`index.html`, `favoritos.html`, `playlists.html`).
- **/static/css/**  
  CSS global (`root.css`) e específico de cada tela (`index.css`, `favoritos.css`, `playlists.css`).
- **/static/js/**  
  JS separado por tela (`index.js`, `favoritos.js`, `playlists.js`).
- **/src/**  
  Lógica Python: CRUD, integração Spotify, modelos.

---

## Resumo de Uso das Tecnologias por Página

| Página           | Bootstrap | SweetAlert2 | Axios | JS Custom | CSS Custom         |
|------------------|:--------:|:-----------:|:-----:|:---------:|:------------------:|
| index.html       |    ✔     |     ✔       |   ✔   |  index.js | index.css/playlists.css |
| favoritos.html   |    ✔     |     ✔       |   ✖   | favoritos.js | playlists.css      |
| playlists.html   |    ✔     |     ✔       |   ✔   | playlists.js | playlists.css      |

- **Bootstrap**: Layout, grid, botões, navbar, responsividade.
- **SweetAlert2**: Modais de confirmação, sucesso e erro.
- **Axios**: Requisições AJAX para favoritar músicas e criar playlists sem recarregar a página.
- **JS Custom**: Lógica de interação (favoritar, remover, criar playlist).
- **CSS Custom**: Visual moderno, cores, efeitos, responsividade.

---

## Observações
- O projeto está modularizado, com frontend e backend bem separados.
- O CSS e JS são organizados por tela para facilitar manutenção.
- Todas as integrações com Spotify são feitas via Spotipy.
- O sistema utiliza variáveis de ambiente para credenciais sensíveis.

---

Para dúvidas ou sugestões, abra uma issue ou entre em contato!
