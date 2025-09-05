import unittest
from Model.Data import AppData
from Controller.Controller import AppController


class TestController(unittest.TestCase):
    def setUp(self):
        self.model = AppData()
        self.model.save_to_file = lambda path: None
        self.controller = AppController(self.model)

    def test_registrazione_e_autenticazione(self):
        esito_registrazione = self.controller.register("davidetraini", "password1")
        self.assertTrue(esito_registrazione)

        duplicato = self.controller.register("davidetraini", "password1")
        self.assertFalse(duplicato)

        login_valido = self.controller.login("davidetraini", "password1")
        self.assertTrue(login_valido)

        login_errato = self.controller.login("davidetraini", "altrapassword")
        self.assertFalse(login_errato)

    def test_logout(self):
        self.controller.register("davidetraini", "password1")
        self.controller.login("davidetraini", "password1")
        self.controller.logout()
        self.assertIsNone(self.controller.get_current_user())

    def test_aggiunta_articolo(self):
        self.controller.register("davidetraini", "password1")
        self.controller.login("davidetraini", "password1")

        esito = self.controller.add_article("Titolo di prova")
        self.assertTrue(esito)
        self.assertEqual(len(self.model.articles), 1)
        articolo = next(iter(self.model.articles.values()))
        self.assertEqual(articolo.title, "Titolo di prova")
        self.assertEqual(articolo.owner, "davidetraini")

    def test_aggiunta_articolo_senza_autenticazione(self):
        esito = self.controller.add_article("Articolo non autorizzato")
        self.assertFalse(esito)

    def test_eliminazione_articolo(self):
        self.controller.register("davidetraini", "password1")
        self.controller.login("davidetraini", "password1")
        self.controller.add_article("Articolo da eliminare")

        articolo_id = next(iter(self.model.articles.keys()))
        esito = self.controller.delete_article(articolo_id)
        self.assertTrue(esito)
        self.assertEqual(len(self.model.articles), 0)

    def test_eliminazione_non_autorizzata(self):
        self.controller.register("davidetraini", "password1")
        self.controller.register("altro_utente", "pass")
        self.controller.login("davidetraini", "password1")
        self.controller.add_article("Articolo di davidetraini")
        articolo_id = next(iter(self.model.articles.keys()))

        self.controller.logout()
        self.controller.login("altro_utente", "pass")
        esito = self.controller.delete_article(articolo_id)
        self.assertFalse(esito)

    def test_modifica_dati(self):   #testare se la mofifica va a buon fine
        self.controller.register("davidetraini","password1")
        self.controller.login("davidetraini","password1")
        esito = self.controller.modifica_user("davideTraini","password2")
        user = self.controller.get_current_user()
        self.assertTrue(esito)
        self.assertEqual(user.username,"davideTraini")
        self.assertEqual(user.password,"password2")
        #solo questo però non va a vedere se effettivamente sono cambiati i riferimenti degli articoli ai rispettivi owner -> il test sarebbe scritto male
        #potevo evitare ciò se non c'era associazione bidirezionale --> bastava che utente aveva una lista di articoli, non serviva che

        new_user = self.controller.get_current_user()

        article = next(iter(self.model.articles))
        self.assertEqual(article.owner,new_user.username)




if __name__ == '__main__':
    unittest.main()
