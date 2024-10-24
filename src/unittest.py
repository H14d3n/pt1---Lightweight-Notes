import unittest
from unittest.mock import patch, MagicMock
import customtkinter as ctk
from init import LightweightNotesApp

class TestLightweightNotesApp(unittest.TestCase):

    def setUp(self):
        # Set up a test instance of the application
        self.root = ctk.CTk()
        self.app = LightweightNotesApp(self.root)

    def tearDown(self):
        # Tear down the tkinter instance
        self.root.destroy()

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='uid:3;first_name:tst;password:tst')
    @patch('csv.DictReader')
    def test_check_credentials_valid(self, mock_csv_reader, mock_open):
        # Mock CSV reader with correct login credentials
        mock_csv_reader.return_value = [{'uid': '3', 'first_name': 'tst', 'password': 'tst'}]
        
        self.app.surname_entry = MagicMock()
        self.app.surname_entry.get.return_value = 'tst'
        self.app.password_entry = MagicMock()
        self.app.password_entry.get.return_value = 'tst'

        with patch.object(self.app, 'init_application') as mock_init_application:
            self.app.handle_login()
            mock_init_application.assert_called_once()

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='uid:3;first_name:tst;password:tst')
    @patch('csv.DictReader')
    def test_check_credentials_invalid(self, mock_csv_reader, mock_open):
        # Mock CSV reader with incorrect login credentials
        mock_csv_reader.return_value = [{'uid': '1', 'first_name': 'Test', 'password': '1234'}]

        self.app.surname_entry = MagicMock()
        self.app.surname_entry.get.return_value = 'WrongName'
        self.app.password_entry = MagicMock()
        self.app.password_entry.get.return_value = 'WrongPass'

        with patch.object(self.app, 'display_message') as mock_display_message:
            self.app.handle_login()
            mock_display_message.assert_called_with("Invalid credentials.")

    def test_clear_window(self):
        # Test if clear_window correctly removes all widgets
        label = ctk.CTkLabel(self.root, text="Test Label")
        label.pack()
        self.assertEqual(len(self.root.winfo_children()), 1)
        
        self.app.clear_window()
        self.assertEqual(len(self.root.winfo_children()), 0)

    @patch('tkinter.filedialog.asksaveasfilename', return_value='/test_path/test.pt1')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_create_document(self, mock_open, mock_save_dialog):
        # Test document creation
        self.app.uid = '1'
        
        with patch.object(self.app, 'edit_document') as mock_edit_document:
            self.app.create_document()
            mock_open.assert_called_once_with('/test_path/test.pt1', 'w')
            mock_edit_document.assert_called_once_with('/test_path/test.pt1')

    @patch('tkinter.filedialog.askopenfilename', return_value='/test_path/test.pt1')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_open_document(self, mock_open, mock_open_dialog):
        # Test document opening
        with patch.object(self.app, 'edit_document') as mock_edit_document:
            self.app.open_document()
            mock_open.assert_called_once_with('/test_path/test.pt1', 'w')
            mock_edit_document.assert_called_once_with('/test_path/test.pt1')

    def test_open_settings(self):
        # Test if the settings window opens correctly
        self.assertIsNone(self.app.settings_window)
        self.app.open_settings()
        self.assertIsNotNone(self.app.settings_window)
        
        # Simulate closing of the settings window
        self.app.on_settings_close()
        self.assertIsNone(self.app.settings_window)


if __name__ == "__main__":
    unittest.main()
