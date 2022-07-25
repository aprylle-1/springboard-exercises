from unittest import TestCase
from urllib import response
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):
    def test_initialize_board(self):
        """Checks that root route will initialize board"""
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<button id="btn-submit-word">Submit Word</button>', html)

    def test_check_word_without_board(self):
        """Checks if user goes to route check-word without a board, user gets redirected to root"""
        with app.test_client() as client:
            resp = client.get("/check-word")

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "http://localhost/")

    def test_check_word_valid(self):
        """Checks if word is valid and is in board"""
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['board'] = [["D", "A", "D", "O", "I"],
                                    ["D", "A", "D", "O", "I"],
                                    ["D", "A", "D", "O", "I"],
                                    ["D", "A", "D", "O", "I"],
                                    ["D", "A", "D", "O", "I"]]
            resp = client.get("/check-word?word=dad")
            self.assertEqual(resp.json['result'], 'ok')

    def test_check_word_valid_not_on_board(self):
        """Checks if word is valid but is not on board"""
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['board'] = [["D", "A", "D", "O", "I"],
                                    ["D", "A", "D", "O", "I"],
                                    ["D", "A", "D", "O", "I"],
                                    ["D", "A", "D", "O", "I"],
                                    ["D", "A", "D", "O", "I"]]
            resp = client.get("/check-word?word=cat")
            self.assertEqual(resp.json['result'], 'not-on-board')
    
    def test_check_word_invalid(self):
        """Checks for invalid word"""
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['board'] = [["D", "A", "D", "O", "I"],
                                    ["D", "A", "D", "O", "I"],
                                    ["D", "A", "D", "O", "I"],
                                    ["D", "A", "D", "O", "I"],
                                    ["D", "A", "D", "O", "I"]]
            resp = client.get("/check-word?word=xyz")
            self.assertEqual(resp.json['result'], 'not-word')
    
    def test_reset_board(self):
        """Checks if route resets session board to none"""
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['board'] = [["D", "A", "D", "O", "I"],
                                    ["D", "A", "D", "O", "I"],
                                    ["D", "A", "D", "O", "I"],
                                    ["D", "A", "D", "O", "I"],
                                    ["D", "A", "D", "O", "I"]]
            resp = client.get("/reset-board")
            self.assertEqual(resp.status_code, 302)