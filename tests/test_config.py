"""
Tests for configuration utilities.
"""

import unittest
import os
import configparser
from telegram_toolkit.utils.config import check_config_exists, save_config, load_config

class TestConfig(unittest.TestCase):
    """Test configuration utilities."""
    
    def setUp(self):
        """Set up test environment."""
        # Remove config file if it exists
        if os.path.exists('config.data'):
            os.rename('config.data', 'config.data.bak')
        if os.path.exists('.env'):
            os.rename('.env', '.env.bak')
    
    def tearDown(self):
        """Clean up after tests."""
        # Remove test config file
        if os.path.exists('config.data'):
            os.remove('config.data')
        if os.path.exists('.env'):
            os.remove('.env')
        
        # Restore original config if it existed
        if os.path.exists('config.data.bak'):
            os.rename('config.data.bak', 'config.data')
        if os.path.exists('.env.bak'):
            os.rename('.env.bak', '.env')
    
    def test_check_config_exists(self):
        """Test check_config_exists function."""
        # Config should not exist initially
        self.assertFalse(check_config_exists())
        
        # Create empty config file
        with open('config.data', 'w') as f:
            pass
        
        # Config should exist now
        self.assertTrue(check_config_exists())
    
    def test_save_and_load_config(self):
        """Test saving and loading configuration."""
        # Save test configuration
        save_config('12345', 'abcdef1234567890', '+1234567890')
        
        # Check if config file was created
        self.assertTrue(os.path.exists('config.data'))
        self.assertTrue(os.path.exists('.env'))
        
        # Load configuration
        config = load_config()
        
        # Verify loaded configuration
        self.assertIsNotNone(config)
        self.assertEqual(config['cred']['id'], '12345')
        self.assertEqual(config['cred']['hash'], 'abcdef1234567890')
        self.assertEqual(config['cred']['phone'], '+1234567890')

if __name__ == '__main__':
    unittest.main()
