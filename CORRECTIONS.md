# CORRECTIONS.md — movement-analysis

Projeto: fipu-lab/movement-analysis
Branch base analisada: master (commit e7863d7)
Fork de destino: https://github.com/admeduardovieira/movement-analysis (a ser criado se não existir)

## Correções propostas (não implementadas ainda — Fase 1 concluída)

| ID | Título | Severidade | Status | Risco | Arquivos envolvidos |
|----|--------|------------|--------|-------|---------------------|
| REA-001 | `fillna(0)` não é `inplace` nem atribuído | P2 | PROPONDO | Baixo | `analysis.py` |
| REA-002 | `pattern.match(fname)` pode retornar `None` → `AttributeError` | P2 | PROPONDO | Baixo | `analysis.py` |
| REA-003 | Acesso `record["active"]`/`record["inactive"]` sem checagem → `KeyError` | P2 | PROPONDO | Baixo | `analysis.py` |
| REA-004 | README incompleto (cam3 ausente) e resultados hardcoded | P3 | PROPONDO | Baixo | `README.md` |
| REA-005 | Inconsistência de schema entre CSVs | P3 | PROPONDO | Baixo | `data/*.csv` (documentação apenas) |
| REA-006 | Sem testes, CI, requirements.txt; Python 3.7 EOL | P3 | PROPONDO | Médio | `Pipfile`, `requirements.txt` (novo), `tests/` (novo), `.github/workflows/` (novo) |

## Detalhe das correções propostas

### REA-001 — fillna(0) não persistido
**Problema:** `record.df.fillna(0)` não modifica o DataFrame original.  
**Correção:** alterar para `record.df.fillna(0, inplace=True)` ou `record.df = record.df.fillna(0)`.  
**Teste de validação:** criar CSV com `result` contendo célula vazia/NaN, executar o script e confirmar que não há exceção e que o valor é tratado como 0.

### REA-002 — match pode ser None
**Problema:** arquivo em `data/` fora do padrão causa `AttributeError`.  
**Correção:** filtrar arquivos com `if match is None: continue` antes de acessar `.group()`.  
**Teste de validação:** adicionar arquivo estranho em `data/` e confirmar que o script continua sem erro.

### REA-003 — grupos ausentes causam KeyError
**Problema:** `record["active"]` / `record["inactive"]` sem checagem.  
**Correção:** verificar se ambas as chaves existem antes de prosseguir; caso contrário, imprimir aviso e pular a câmera.  
**Teste de validação:** criar pasta `data/` com câmera que tenha apenas um grupo e confirmar comportamento gracioso.

### REA-004 — README incompleto
**Problema:** README documenta só cam1/cam2; cam3 existe nos dados. Resultados hardcoded.  
**Correção:** adicionar seção de cam3 ao README (ou gerar dinamicamente); manter nota de que valores são ilustrativos.  
**Teste de validação:** conferir que README menciona cam1, cam2 e cam3.

### REA-005 — Schema inconsistente nos CSVs
**Problema:** `active_cam*` têm `id` preenchido; `inactive_cam*` têm `id` vazio; `inactive_cam3` falta `id`.  
**Correção:** documentar a variação no README; não alterar dados (evitar destruir informação). Considerar padronizar em futuras coleta.  
**Teste de validação:** conferir cabeçalhos de todos os CSVs.

### REA-006 — Base de reprodução e CI
**Problema:** sem testes, sem CI, sem `requirements.txt`, Python 3.7 EOL.  
**Correção:** adicionar `requirements.txt` (pandas, scipy), testes unitários com pytest, workflow GitHub Actions, atualizar `python_version` no `Pipfile` para 3.10+.  
**Teste de validação:** `pytest` passa; workflow CI executa em push/PR.

## Correções a evitar por falta de evidência
Nenhuma das acima é evitada; todas têm evidência técnica ou são melhorias de qualidade justificadas. Não há alterações propositadas sem fundamento.

## Plano de publicação
- Criar fork `admeduardovieira/movement-analysis`.
- Criar branch `fix/rea-001-003-robustness` para REA-001..003.
- Criar branch `docs/rea-004-readme` para REA-004.
- Commit com identidade `admeduardovieira <admeduardovieira@users.noreply.github.com>`.
- Abrir PRs para `fipu-lab/movement-analysis` branch `master`.
- Adicionar REVERSE_ENGINEERING_REPORT.md e CORRECTIONS.md + traduções EN/UK ao fork.
