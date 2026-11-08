# REVERSE_ENGINEERING_REPORT — movement-analysis

## A. Diagnóstico geral

### Arquitetura identificada
Projeto Python mínimo de análise estatística de movimento. Não há camada de aplicação, API, interface ou banco de dados. O fluxo é um único script `analysis.py` que:

1. Lê todos os arquivos CSV da pasta `data/` cujo nome bate no padrão `(?P<type>.*)_(?P<cam>.*)_formula.csv`.
2. Carrega cada CSV em um pandas DataFrame.
3. Agrupa registros por câmera (`cam`) e tipo (`active` / `inactive`).
4. Para cada câmera, aplica o teste de Mann-Whitney U (`scipy.stats.mannwhitneyu`, `alternative="greater"`) comparando as colunas `result` dos grupos ativo e inativo.
5. Imprime contagens, quantis e o resultado do teste.

Não há ponto de entrada web, não há rotas, não há componente frontend. É um script de análise off-line.

### Tecnologias e dependências
- Linguagem: Python 3.7 (declarado em `Pipfile`, já em fim de vida)
- Dependências de runtime: `pandas`, `scipy`
- Dependências de dev: `black`, `ipython`, `ipykernel`
- Gerenciador: Pipenv (`Pipfile` + `Pipfile.lock` commitados)
- Não há `requirements.txt`, não há `setup.py`/`pyproject.toml`, não há CI configurado.

### Estado de manutenção
Último commit: `e7863d7 Update README.md`. Histórico curto (4 commits). Branch padrão upstream: `master`. Repositório upstream: `https://github.com/fipu-lab/movement-analysis`. Não há issues nem PRs visíveis como atividade recente relevante. Projeto em baixa atividade.

### Mecanismos de testes existentes
Nenhum teste automatizado encontrado. Nenhuma pasta `tests/`, nenhum arquivo `test_*.py`, nenhuma configuração de pytest. Não há CI/CD (pasta `.github/workflows` inexistente).

### Limitações da investigação
- REA 6.7.0 não operacional via CLI neste ambiente (o arquivo `rea` é um vínculo/documento do ambiente PulsoGold, não um executável standalone; execução bloqueada). Análise feita por inspeção estática de código + leitura de dados + terminal.
- pandas/scipy não instalados nos intérpretes Python disponíveis; download pesado evitado conforme instrução. Resultados numéricos do README não foram reproduzidos por execução, apenas confrontados com contagens de linhas dos CSVs.
- Não houve acesso a dados privados; apenas dados sintéticos/públicos já presentes no repositório.

## B. Problemas encontrados

| ID | Título | Severidade | Status | Localização |
|----|--------|------------|--------|-------------|
| REA-001 | `fillna(0)` não é `inplace` nem atribuído | P2 | PROVÁVEL | `analysis.py:16` |
| REA-002 | `pattern.match(fname)` pode retornar `None` → `AttributeError` | P2 | PROVÁVEL | `analysis.py:17-19` |
| REA-003 | Acesso `record["active"]`/`record["inactive"]` sem checagem → `KeyError` | P2 | PROVÁVEL | `analysis.py:26-28` |
| REA-004 | README documenta apenas cam1/cam2; dados cam3 existem; resultados hardcoded | P3 | CONFIRMADO | `README.md`, `data/` |
| REA-005 | Inconsistência de schema entre CSVs (coluna `id` preenchida/vazia/ausente) | P3 | CONFIRMADO | `data/*.csv` |
| REA-006 | Ausência de testes, CI, requirements.txt; Python 3.7 EOL | P3 | CONFIRMADO | `Pipfile`, raiz do repo |

### Detalhes dos problemas confirmados

**REA-004 (CONFIRMADO)**: `README.md` registra análises apenas para `cam1` e `cam2`, mas a pasta `data/` contém `active_cam3_formula.csv` e `inactive_cam3_formula.csv` (25.779 linhas cada). O script `analysis.py` processaria cam3 se executado, mas o README não o menciona. Além disso, os valores de `pvalue` e `statistic` no README estão hardcoded (ex.: `pvalue=0.0` para cam1), não reproduzíveis automaticamente a partir do código.

Evidência: `README.md:7-27` menciona só cam1/cam2; `data/` possui 6 arquivos incluindo cam3.

**REA-005 (CONFIRMADO)**: Os CSVs não compartilham o mesmo schema. `active_cam1/2/3` têm colunas `timestamp,id,result` com `id` preenchido. `inactive_cam1/2` têm `timestamp,id,result` com `id` vazio (`, ,valor`). `inactive_cam3` tem apenas `timestamp,result` (sem coluna `id`). O script lê apenas `result`, então não quebra, mas é uma inconsistência de dados.

Evidência: cabeçalho de `inactive_cam3_formula.csv` = `timestamp,result`; cabeçalho de `active_cam1_formula.csv` = `timestamp,id,result`.

**REA-006 (CONFIRMADO)**: Não há testes automatizados, nem CI, nem `requirements.txt`. O `Pipfile` declara `python_version = "3.7"` (fim de vida desde 2023-06-27).

### Detalhes dos problemas prováveis (não reproduzidos nos dados atuais)

**REA-001 (PROVÁVEL)**: `record.df.fillna(0)` (linha 16) não passa `inplace=True` nem atribui o resultado de volta (`record.df = record.df.fillna(0)`). O `fillna` padrão retorna um novo DataFrame. Se `result` contiver `NaN`, eles não serão preenchidos e `mannwhitneyu` poderá falhar ou retornar `NaN`. Nos CSVs atuais a coluna `result` está preenchida, então não se manifesta, mas é um bug latente.

**REA-002 (PROVÁVEL)**: `match = pattern.match(fname)` (linha 17). Se houver qualquer arquivo em `data/` que não bata no padrão (ex.: `.DS_Store`, `README`, arquivo temporário), `match` será `None` e `match.group("type")` lançará `AttributeError`, interrompendo todo o script. Não há filtragem de arquivos nem tratamento de exceção.

**REA-003 (PROVÁVEL)**: Linhas 26-28 acessam `record["active"]` e `record["inactive"]` diretamente. Se uma câmera possuir apenas um dos grupos (ex.: só `active`), ocorre `KeyError`.

## C. Problemas recorrentes
Nenhum issue ou PR público recorrente encontrado para este repositório (atividade muito baixa, histórico curto). Não há regressões documentadas.

## D. Erros não documentados
Todos os itens da seção B são problemas não documentados anteriormente pelo projeto (nenhum issue/PR relacionado encontrado).

## E. Performance
Não há oportunidades de performance significativas identificadas: o script processa um volume modesto de dados (máximo ~52 mil linhas por arquivo) em memória única, uma única vez. Não há laços aninhados, requisições de rede, ou re-renderizações. A leitura de todos os CSVs em dicionários aninhados é adequada ao escopo.

## F. Melhorias técnicas
- Adicionar `inplace=True` ou reatribuição no `fillna(0)` (REA-001).
- Filtrar apenas arquivos que batem no padrão e tratar `match is None` (REA-002).
- Verificar existência de ambos os grupos antes de acessar (REA-003).
- Atualizar README para incluir cam3 e/ou gerar resultados dinamicamente (REA-004).
- Padronizar schema dos CSVs ou documentar a variação (REA-005).
- Adicionar `requirements.txt`, testes unitários com `pytest`, CI GitHub Actions, atualizar versão do Python no `Pipfile` (REA-006).

## G. Plano de execução
Correções independentes e de baixo risco (podem ser PRs separados):
1. REA-001, REA-002, REA-003 — robustez do `analysis.py` (baixo risco, teste reproduzível).
2. REA-004 — atualização do README.
3. REA-005 — documentação/padronização de schema dos dados.
4. REA-006 — `requirements.txt`, testes, CI, versão do Python (mais envolvido).

Todas são independentes entre si.

## H. Resultado esperado
Tornar o script robusto a entradas inesperadas (arquivos estranhos, grupos ausentes, NaN), documentar corretamente todas as câmeras e estabelecer uma base testável para contribuições futuras.

---

**Ferramentas usadas:** git, gh (autenticado como admeduardovieira), PowerShell/terminal, inspeção de código.  
**Limitação:** REA 6.7.0 não operacional neste ambiente; pandas/scipy não instalados (execução numérica não realizada).  
**Ambiente:** Windows, PowerShell 5.1, `C:\Users\User\audit-repos\movement-analysis` (clone do upstream, branch `master`, commit `e7863d7`).
