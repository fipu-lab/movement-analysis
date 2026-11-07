import re
import unittest

# Mesmo padrão utilizado em analysis.py (duplicado aqui para evitar a
# dependência de pandas/scipy neste teste de unidade leve).
PATTERN = re.compile(r"(?P<type>.*)_(?P<cam>.*)_formula.csv")


class TestFilenameParsing(unittest.TestCase):
    def test_nome_valido_extrai_tipo_e_camera(self):
        for nome, tipo_esperado, cam_esperado in [
            ("active_cam1_formula.csv", "active", "cam1"),
            ("inactive_cam2_formula.csv", "inactive", "cam2"),
            ("active_cam3_formula.csv", "active", "cam3"),
        ]:
            match = PATTERN.match(nome)
            self.assertIsNotNone(match, f"{nome} deveria bater no padrão")
            self.assertEqual(match.group("type"), tipo_esperado)
            self.assertEqual(match.group("cam"), cam_esperado)

    def test_nome_invalido_retorna_none_nao_quebra(self):
        # Comportamento esperado após a correção REA-002: arquivos que
        # não batem no padrão são ignorados (match is None -> continue),
        # evitando AttributeError em match.group(...).
        for nome in [
            "README.md",
            ".DS_Store",
            "dados_brutos.csv",
            "active_cam1.xlsx",
            "outro_arquivo.txt",
        ]:
            match = PATTERN.match(nome)
            self.assertIsNone(match, f"{nome} não deveria bater no padrão")


if __name__ == "__main__":
    unittest.main()
