#!/usr/bin/env python3
"""
Development tools installation script for Ontario Driving School Manager.
Installs required development tools and dependencies.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
from typing import List, Dict, Optional

class DevToolsInstaller:
    """Installs development tools and dependencies."""

    def __init__(self):
        self.system = platform.system()
        self.python_version = "3.9.0"
        self.node_version = "18.0.0"
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def install_python_tools(self) -> bool:
        """Install Python development tools."""
        print("Installing Python development tools...")
        
        try:
            # Install pip tools
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "setuptools", "wheel"])

            # Install development dependencies
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements-dev.txt"])

            # Install pre-commit
            subprocess.run([sys.executable, "-m", "pip", "install", "pre-commit"])
            subprocess.run(["pre-commit", "install"])

            return True
        except subprocess.CalledProcessError as e:
            self.errors.append(f"Failed to install Python tools: {str(e)}")
            return False

    def install_node_tools(self) -> bool:
        """Install Node.js development tools."""
        print("Installing Node.js development tools...")
        
        try:
            # Install npm packages
            subprocess.run(["npm", "install"])

            # Install global tools
            subprocess.run(["npm", "install", "-g", "typescript", "ts-node", "nodemon"])

            return True
        except subprocess.CalledProcessError as e:
            self.errors.append(f"Failed to install Node.js tools: {str(e)}")
            return False

    def install_git_tools(self) -> bool:
        """Install Git tools and hooks."""
        print("Installing Git tools...")
        
        try:
            # Install Git LFS
            if self.system == "Darwin":
                subprocess.run(["brew", "install", "git-lfs"])
            elif self.system == "Linux":
                subprocess.run(["sudo", "apt-get", "install", "git-lfs"])
            elif self.system == "Windows":
                subprocess.run(["git", "lfs", "install"])

            # Initialize Git LFS
            subprocess.run(["git", "lfs", "install"])

            return True
        except subprocess.CalledProcessError as e:
            self.errors.append(f"Failed to install Git tools: {str(e)}")
            return False

    def install_vscode_extensions(self) -> bool:
        """Install VS Code extensions."""
        print("Installing VS Code extensions...")
        
        extensions = [
            "ms-python.python",
            "ms-python.vscode-pylance",
            "dbaeumer.vscode-eslint",
            "esbenp.prettier-vscode",
            "ms-azuretools.vscode-docker",
            "eamodio.gitlens",
            "ms-vscode.vscode-typescript-next",
            "ms-python.black-formatter",
            "ms-python.flake8"
        ]

        try:
            for extension in extensions:
                subprocess.run(["code", "--install-extension", extension])
            return True
        except subprocess.CalledProcessError as e:
            self.errors.append(f"Failed to install VS Code extensions: {str(e)}")
            return False

    def setup_environment(self) -> bool:
        """Set up development environment."""
        print("Setting up development environment...")
        
        try:
            # Create necessary directories
            directories = [
                "logs",
                "data",
                "tests",
                "docs",
                "scripts"
            ]

            for directory in directories:
                Path(directory).mkdir(exist_ok=True)

            # Create configuration files if they don't exist
            self._create_config_files()

            return True
        except Exception as e:
            self.errors.append(f"Failed to set up environment: {str(e)}")
            return False

    def _create_config_files(self) -> None:
        """Create configuration files if they don't exist."""
        config_files = {
            ".env.example": """
# Database
DATABASE_URL=sqlite:///./ontario_driving_school.db

# Security
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret

# API
API_HOST=localhost
API_PORT=8000

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
""",
            ".pre-commit-config.yaml": """
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-added-large-files

-   repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
    -   id: black

-   repo: https://github.com/PyCQA/flake8
    rev: 6.0.0
    hooks:
    -   id: flake8
""",
            ".editorconfig": """
root = true

[*]
end_of_line = lf
insert_final_newline = true
charset = utf-8
trim_trailing_whitespace = true

[*.{py,js,jsx,ts,tsx}]
indent_style = space
indent_size = 4

[*.{json,yml,yaml,md}]
indent_style = space
indent_size = 2
""",
            ".prettierrc": """
{
    "semi": true,
    "trailingComma": "es5",
    "singleQuote": true,
    "printWidth": 100,
    "tabWidth": 2
}
""",
            ".eslintrc.js": """
module.exports = {
    env: {
        browser: true,
        es2021: true,
        node: true,
    },
    extends: [
        'eslint:recommended',
        'plugin:react/recommended',
        'plugin:@typescript-eslint/recommended',
    ],
    parser: '@typescript-eslint/parser',
    parserOptions: {
        ecmaFeatures: {
            jsx: true,
        },
        ecmaVersion: 12,
        sourceType: 'module',
    },
    plugins: ['react', '@typescript-eslint'],
    rules: {
        'react/react-in-jsx-scope': 'off',
    },
    settings: {
        react: {
            version: 'detect',
        },
    },
};
"""
        }

        for file_path, content in config_files.items():
            if not Path(file_path).exists():
                with open(file_path, 'w') as f:
                    f.write(content.strip())

    def run_installation(self) -> bool:
        """Run all installation steps."""
        steps = [
            self.install_python_tools,
            self.install_node_tools,
            self.install_git_tools,
            self.install_vscode_extensions,
            self.setup_environment
        ]

        success = all(step() for step in steps)

        if self.errors:
            print("\nErrors:")
            for error in self.errors:
                print(f"  - {error}")

        if self.warnings:
            print("\nWarnings:")
            for warning in self.warnings:
                print(f"  - {warning}")

        return success

def main():
    """Main entry point."""
    installer = DevToolsInstaller()
    success = installer.run_installation()
    
    if success:
        print("\nDevelopment tools installation successful!")
        sys.exit(0)
    else:
        print("\nDevelopment tools installation failed!")
        sys.exit(1)

if __name__ == '__main__':
    main() 