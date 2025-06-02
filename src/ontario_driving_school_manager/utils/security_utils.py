"""
Security Utilities Module

This module provides security-related functionality.
It includes encryption, hashing, and token management.

Author: Rami Drive School
Date: 2024
"""

import os
import base64
import hashlib
import hmac
import secrets
import string
from typing import Dict, Any, Optional, Union, List, Tuple
from datetime import datetime, timedelta
import logging
import jwt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization

logger = logging.getLogger(__name__)

class SecurityError(Exception):
    """Security error."""
    pass

class SecurityManager:
    """Security manager."""
    
    def __init__(
        self,
        secret_key: Optional[str] = None,
        token_expiry: int = 3600,
        salt_length: int = 16,
        key_length: int = 32,
        iterations: int = 100000
    ):
        """Initialize security manager.
        
        Args:
            secret_key: Secret key for encryption
            token_expiry: Token expiry time in seconds
            salt_length: Salt length in bytes
            key_length: Key length in bytes
            iterations: Number of iterations for key derivation
        """
        self.secret_key = secret_key or os.urandom(32)
        self.token_expiry = token_expiry
        self.salt_length = salt_length
        self.key_length = key_length
        self.iterations = iterations
        
        # Initialize Fernet cipher
        self.cipher = Fernet(
            base64.urlsafe_b64encode(
                hashlib.sha256(self.secret_key).digest()
            )
        )
    
    def generate_salt(self) -> bytes:
        """Generate salt.
        
        Returns:
            Salt bytes
        """
        return os.urandom(self.salt_length)
    
    def derive_key(
        self,
        password: str,
        salt: Optional[bytes] = None
    ) -> Tuple[bytes, bytes]:
        """Derive key from password.
        
        Args:
            password: Password
            salt: Salt bytes
            
        Returns:
            Tuple of (key, salt)
        """
        if salt is None:
            salt = self.generate_salt()
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self.key_length,
            salt=salt,
            iterations=self.iterations
        )
        
        key = kdf.derive(password.encode())
        
        return key, salt
    
    def encrypt(
        self,
        data: Union[str, bytes],
        password: Optional[str] = None
    ) -> Tuple[bytes, bytes]:
        """Encrypt data.
        
        Args:
            data: Data to encrypt
            password: Password for encryption
            
        Returns:
            Tuple of (encrypted_data, salt)
        
        Raises:
            SecurityError: If encryption fails
        """
        try:
            if isinstance(data, str):
                data = data.encode()
            
            if password:
                key, salt = self.derive_key(password)
                cipher = Fernet(base64.urlsafe_b64encode(key))
            else:
                cipher = self.cipher
                salt = b""
            
            encrypted_data = cipher.encrypt(data)
            
            return encrypted_data, salt
        except Exception as e:
            raise SecurityError(f"Error encrypting data: {str(e)}")
    
    def decrypt(
        self,
        encrypted_data: bytes,
        password: Optional[str] = None,
        salt: Optional[bytes] = None
    ) -> bytes:
        """Decrypt data.
        
        Args:
            encrypted_data: Encrypted data
            password: Password for decryption
            salt: Salt bytes
            
        Returns:
            Decrypted data
        
        Raises:
            SecurityError: If decryption fails
        """
        try:
            if password:
                if salt is None:
                    raise SecurityError("Salt is required for password decryption")
                
                key, _ = self.derive_key(password, salt)
                cipher = Fernet(base64.urlsafe_b64encode(key))
            else:
                cipher = self.cipher
            
            decrypted_data = cipher.decrypt(encrypted_data)
            
            return decrypted_data
        except Exception as e:
            raise SecurityError(f"Error decrypting data: {str(e)}")
    
    def hash_password(
        self,
        password: str,
        salt: Optional[bytes] = None
    ) -> Tuple[str, bytes]:
        """Hash password.
        
        Args:
            password: Password to hash
            salt: Salt bytes
            
        Returns:
            Tuple of (hashed_password, salt)
        
        Raises:
            SecurityError: If hashing fails
        """
        try:
            if salt is None:
                salt = self.generate_salt()
            
            key, _ = self.derive_key(password, salt)
            
            hashed_password = base64.b64encode(key).decode()
            
            return hashed_password, salt
        except Exception as e:
            raise SecurityError(f"Error hashing password: {str(e)}")
    
    def verify_password(
        self,
        password: str,
        hashed_password: str,
        salt: bytes
    ) -> bool:
        """Verify password.
        
        Args:
            password: Password to verify
            hashed_password: Hashed password
            salt: Salt bytes
            
        Returns:
            True if password is valid, False otherwise
        
        Raises:
            SecurityError: If verification fails
        """
        try:
            key, _ = self.derive_key(password, salt)
            
            return base64.b64encode(key).decode() == hashed_password
        except Exception as e:
            raise SecurityError(f"Error verifying password: {str(e)}")
    
    def generate_token(
        self,
        data: Dict[str, Any],
        expiry: Optional[int] = None
    ) -> str:
        """Generate JWT token.
        
        Args:
            data: Token data
            expiry: Token expiry time in seconds
            
        Returns:
            JWT token
        
        Raises:
            SecurityError: If token generation fails
        """
        try:
            payload = {
                **data,
                "exp": datetime.utcnow() + timedelta(
                    seconds=expiry or self.token_expiry
                )
            }
            
            token = jwt.encode(
                payload,
                self.secret_key,
                algorithm="HS256"
            )
            
            return token
        except Exception as e:
            raise SecurityError(f"Error generating token: {str(e)}")
    
    def verify_token(
        self,
        token: str
    ) -> Dict[str, Any]:
        """Verify JWT token.
        
        Args:
            token: JWT token
            
        Returns:
            Token payload
        
        Raises:
            SecurityError: If token verification fails
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=["HS256"]
            )
            
            return payload
        except Exception as e:
            raise SecurityError(f"Error verifying token: {str(e)}")
    
    def generate_key_pair(
        self,
        key_size: int = 2048
    ) -> Tuple[bytes, bytes]:
        """Generate RSA key pair.
        
        Args:
            key_size: Key size in bits
            
        Returns:
            Tuple of (private_key, public_key)
        
        Raises:
            SecurityError: If key generation fails
        """
        try:
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=key_size
            )
            
            public_key = private_key.public_key()
            
            private_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            
            public_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            
            return private_pem, public_pem
        except Exception as e:
            raise SecurityError(f"Error generating key pair: {str(e)}")
    
    def encrypt_with_public_key(
        self,
        data: Union[str, bytes],
        public_key: bytes
    ) -> bytes:
        """Encrypt data with public key.
        
        Args:
            data: Data to encrypt
            public_key: Public key
            
        Returns:
            Encrypted data
        
        Raises:
            SecurityError: If encryption fails
        """
        try:
            if isinstance(data, str):
                data = data.encode()
            
            public_key = serialization.load_pem_public_key(public_key)
            
            encrypted_data = public_key.encrypt(
                data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            
            return encrypted_data
        except Exception as e:
            raise SecurityError(f"Error encrypting with public key: {str(e)}")
    
    def decrypt_with_private_key(
        self,
        encrypted_data: bytes,
        private_key: bytes
    ) -> bytes:
        """Decrypt data with private key.
        
        Args:
            encrypted_data: Encrypted data
            private_key: Private key
            
        Returns:
            Decrypted data
        
        Raises:
            SecurityError: If decryption fails
        """
        try:
            private_key = serialization.load_pem_private_key(
                private_key,
                password=None
            )
            
            decrypted_data = private_key.decrypt(
                encrypted_data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            
            return decrypted_data
        except Exception as e:
            raise SecurityError(f"Error decrypting with private key: {str(e)}")
    
    def generate_password(
        self,
        length: int = 12,
        use_uppercase: bool = True,
        use_lowercase: bool = True,
        use_digits: bool = True,
        use_special: bool = True
    ) -> str:
        """Generate password.
        
        Args:
            length: Password length
            use_uppercase: Whether to use uppercase letters
            use_lowercase: Whether to use lowercase letters
            use_digits: Whether to use digits
            use_special: Whether to use special characters
            
        Returns:
            Generated password
        
        Raises:
            SecurityError: If password generation fails
        """
        try:
            chars = ""
            
            if use_uppercase:
                chars += string.ascii_uppercase
            
            if use_lowercase:
                chars += string.ascii_lowercase
            
            if use_digits:
                chars += string.digits
            
            if use_special:
                chars += string.punctuation
            
            if not chars:
                raise SecurityError("No character sets selected")
            
            password = "".join(
                secrets.choice(chars)
                for _ in range(length)
            )
            
            return password
        except Exception as e:
            raise SecurityError(f"Error generating password: {str(e)}")
    
    def generate_hmac(
        self,
        data: Union[str, bytes],
        key: Optional[bytes] = None
    ) -> Tuple[str, bytes]:
        """Generate HMAC.
        
        Args:
            data: Data to hash
            key: HMAC key
            
        Returns:
            Tuple of (hmac, key)
        
        Raises:
            SecurityError: If HMAC generation fails
        """
        try:
            if isinstance(data, str):
                data = data.encode()
            
            if key is None:
                key = os.urandom(self.key_length)
            
            h = hmac.new(key, data, hashlib.sha256)
            
            return h.hexdigest(), key
        except Exception as e:
            raise SecurityError(f"Error generating HMAC: {str(e)}")
    
    def verify_hmac(
        self,
        data: Union[str, bytes],
        hmac_str: str,
        key: bytes
    ) -> bool:
        """Verify HMAC.
        
        Args:
            data: Data to verify
            hmac_str: HMAC string
            key: HMAC key
            
        Returns:
            True if HMAC is valid, False otherwise
        
        Raises:
            SecurityError: If HMAC verification fails
        """
        try:
            if isinstance(data, str):
                data = data.encode()
            
            h = hmac.new(key, data, hashlib.sha256)
            
            return h.hexdigest() == hmac_str
        except Exception as e:
            raise SecurityError(f"Error verifying HMAC: {str(e)}")
    
    def generate_csrf_token(self) -> str:
        """Generate CSRF token.
        
        Returns:
            CSRF token
        
        Raises:
            SecurityError: If token generation fails
        """
        try:
            return secrets.token_urlsafe(32)
        except Exception as e:
            raise SecurityError(f"Error generating CSRF token: {str(e)}")
    
    def verify_csrf_token(
        self,
        token: str,
        stored_token: str
    ) -> bool:
        """Verify CSRF token.
        
        Args:
            token: Token to verify
            stored_token: Stored token
            
        Returns:
            True if token is valid, False otherwise
        
        Raises:
            SecurityError: If token verification fails
        """
        try:
            return secrets.compare_digest(token, stored_token)
        except Exception as e:
            raise SecurityError(f"Error verifying CSRF token: {str(e)}")
    
    def sanitize_input(
        self,
        data: str
    ) -> str:
        """Sanitize input.
        
        Args:
            data: Input data
            
        Returns:
            Sanitized data
        
        Raises:
            SecurityError: If sanitization fails
        """
        try:
            # Remove HTML tags
            data = re.sub(r"<[^>]*>", "", data)
            
            # Remove special characters
            data = re.sub(r"[^\w\s-]", "", data)
            
            # Remove extra whitespace
            data = " ".join(data.split())
            
            return data
        except Exception as e:
            raise SecurityError(f"Error sanitizing input: {str(e)}")
    
    def validate_file_type(
        self,
        file_path: str,
        allowed_types: List[str]
    ) -> bool:
        """Validate file type.
        
        Args:
            file_path: File path
            allowed_types: List of allowed file types
            
        Returns:
            True if file type is valid, False otherwise
        
        Raises:
            SecurityError: If validation fails
        """
        try:
            import magic
            
            mime = magic.Magic(mime=True)
            file_type = mime.from_file(file_path)
            
            return file_type in allowed_types
        except Exception as e:
            raise SecurityError(f"Error validating file type: {str(e)}")
    
    def validate_file_size(
        self,
        file_path: str,
        max_size: int
    ) -> bool:
        """Validate file size.
        
        Args:
            file_path: File path
            max_size: Maximum file size in bytes
            
        Returns:
            True if file size is valid, False otherwise
        
        Raises:
            SecurityError: If validation fails
        """
        try:
            file_size = os.path.getsize(file_path)
            
            return file_size <= max_size
        except Exception as e:
            raise SecurityError(f"Error validating file size: {str(e)}")
    
    def validate_file_name(
        self,
        file_name: str
    ) -> bool:
        """Validate file name.
        
        Args:
            file_name: File name
            
        Returns:
            True if file name is valid, False otherwise
        
        Raises:
            SecurityError: If validation fails
        """
        try:
            # Check for path traversal
            if ".." in file_name or "/" in file_name or "\\" in file_name:
                return False
            
            # Check for invalid characters
            if re.search(r"[^\w\s.-]", file_name):
                return False
            
            return True
        except Exception as e:
            raise SecurityError(f"Error validating file name: {str(e)}")
    
    def validate_file_path(
        self,
        file_path: str
    ) -> bool:
        """Validate file path.
        
        Args:
            file_path: File path
            
        Returns:
            True if file path is valid, False otherwise
        
        Raises:
            SecurityError: If validation fails
        """
        try:
            # Check for path traversal
            if ".." in file_path:
                return False
            
            # Check for invalid characters
            if re.search(r"[^\w\s./\\-]", file_path):
                return False
            
            return True
        except Exception as e:
            raise SecurityError(f"Error validating file path: {str(e)}")
    
    def validate_url(
        self,
        url: str
    ) -> bool:
        """Validate URL.
        
        Args:
            url: URL
            
        Returns:
            True if URL is valid, False otherwise
        
        Raises:
            SecurityError: If validation fails
        """
        try:
            # Check for invalid characters
            if re.search(r"[^\w\s./\\-:?=&]", url):
                return False
            
            # Check for protocol
            if not url.startswith(("http://", "https://")):
                return False
            
            return True
        except Exception as e:
            raise SecurityError(f"Error validating URL: {str(e)}")
    
    def validate_email(
        self,
        email: str
    ) -> bool:
        """Validate email.
        
        Args:
            email: Email address
            
        Returns:
            True if email is valid, False otherwise
        
        Raises:
            SecurityError: If validation fails
        """
        try:
            # Check for invalid characters
            if re.search(r"[^\w\s.@-]", email):
                return False
            
            # Check for @ symbol
            if "@" not in email:
                return False
            
            # Check for domain
            if "." not in email.split("@")[1]:
                return False
            
            return True
        except Exception as e:
            raise SecurityError(f"Error validating email: {str(e)}")
    
    def validate_phone(
        self,
        phone: str
    ) -> bool:
        """Validate phone number.
        
        Args:
            phone: Phone number
            
        Returns:
            True if phone number is valid, False otherwise
        
        Raises:
            SecurityError: If validation fails
        """
        try:
            # Remove non-digit characters
            digits = re.sub(r"\D", "", phone)
            
            # Check length
            if len(digits) < 10 or len(digits) > 15:
                return False
            
            return True
        except Exception as e:
            raise SecurityError(f"Error validating phone number: {str(e)}")
    
    def validate_postal_code(
        self,
        postal_code: str
    ) -> bool:
        """Validate postal code.
        
        Args:
            postal_code: Postal code
            
        Returns:
            True if postal code is valid, False otherwise
        
        Raises:
            SecurityError: If validation fails
        """
        try:
            # Check format
            if not re.match(r"^[A-Z]\d[A-Z] \d[A-Z]\d$", postal_code):
                return False
            
            return True
        except Exception as e:
            raise SecurityError(f"Error validating postal code: {str(e)}")
    
    def validate_credit_card(
        self,
        credit_card: str
    ) -> bool:
        """Validate credit card number.
        
        Args:
            credit_card: Credit card number
            
        Returns:
            True if credit card number is valid, False otherwise
        
        Raises:
            SecurityError: If validation fails
        """
        try:
            # Remove non-digit characters
            digits = re.sub(r"\D", "", credit_card)
            
            # Check length
            if len(digits) < 13 or len(digits) > 19:
                return False
            
            # Check Luhn algorithm
            total = 0
            for i, digit in enumerate(reversed(digits)):
                if i % 2 == 1:
                    digit *= 2
                    if digit > 9:
                        digit -= 9
                total += digit
            
            return total % 10 == 0
        except Exception as e:
            raise SecurityError(f"Error validating credit card number: {str(e)}")
    
    def validate_password_strength(
        self,
        password: str,
        min_length: int = 8,
        require_uppercase: bool = True,
        require_lowercase: bool = True,
        require_digits: bool = True,
        require_special: bool = True
    ) -> bool:
        """Validate password strength.
        
        Args:
            password: Password
            min_length: Minimum length
            require_uppercase: Whether to require uppercase letters
            require_lowercase: Whether to require lowercase letters
            require_digits: Whether to require digits
            require_special: Whether to require special characters
            
        Returns:
            True if password is strong, False otherwise
        
        Raises:
            SecurityError: If validation fails
        """
        try:
            # Check length
            if len(password) < min_length:
                return False
            
            # Check uppercase
            if require_uppercase and not re.search(r"[A-Z]", password):
                return False
            
            # Check lowercase
            if require_lowercase and not re.search(r"[a-z]", password):
                return False
            
            # Check digits
            if require_digits and not re.search(r"\d", password):
                return False
            
            # Check special characters
            if require_special and not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
                return False
            
            return True
        except Exception as e:
            raise SecurityError(f"Error validating password strength: {str(e)}")
    
    def validate_username(
        self,
        username: str,
        min_length: int = 3,
        max_length: int = 16
    ) -> bool:
        """Validate username.
        
        Args:
            username: Username
            min_length: Minimum length
            max_length: Maximum length
            
        Returns:
            True if username is valid, False otherwise
        
        Raises:
            SecurityError: If validation fails
        """
        try:
            # Check length
            if len(username) < min_length or len(username) > max_length:
                return False
            
            # Check characters
            if not re.match(r"^[a-zA-Z0-9_-]+$", username):
                return False
            
            return True
        except Exception as e:
            raise SecurityError(f"Error validating username: {str(e)}")
    
    def validate_ip(
        self,
        ip: str
    ) -> bool:
        """Validate IP address.
        
        Args:
            ip: IP address
            
        Returns:
            True if IP address is valid, False otherwise
        
        Raises:
            SecurityError: If validation fails
        """
        try:
            # Check format
            if not re.match(
                r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
                ip
            ):
                return False
            
            return True
        except Exception as e:
            raise SecurityError(f"Error validating IP address: {str(e)}")
    
    def validate_mac(
        self,
        mac: str
    ) -> bool:
        """Validate MAC address.
        
        Args:
            mac: MAC address
            
        Returns:
            True if MAC address is valid, False otherwise
        
        Raises:
            SecurityError: If validation fails
        """
        try:
            # Check format
            if not re.match(
                r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$",
                mac
            ):
                return False
            
            return True
        except Exception as e:
            raise SecurityError(f"Error validating MAC address: {str(e)}")
    
    def validate_uuid(
        self,
        uuid_str: str
    ) -> bool:
        """Validate UUID.
        
        Args:
            uuid_str: UUID
            
        Returns:
            True if UUID is valid, False otherwise
        
        Raises:
            SecurityError: If validation fails
        """
        try:
            # Check format
            if not re.match(
                r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
                uuid_str
            ):
                return False
            
            return True
        except Exception as e:
            raise SecurityError(f"Error validating UUID: {str(e)}")
    
    def validate_hex_color(
        self,
        hex_color: str
    ) -> bool:
        """Validate hex color.
        
        Args:
            hex_color: Hex color
            
        Returns:
            True if hex color is valid, False otherwise
        
        Raises:
            SecurityError: If validation fails
        """
        try:
            # Check format
            if not re.match(
                r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$",
                hex_color
            ):
                return False
            
            return True
        except Exception as e:
            raise SecurityError(f"Error validating hex color: {str(e)}")
    
    def validate_html_tag(
        self,
        html_tag: str
    ) -> bool:
        """Validate HTML tag.
        
        Args:
            html_tag: HTML tag
            
        Returns:
            True if HTML tag is valid, False otherwise
        
        Raises:
            SecurityError: If validation fails
        """
        try:
            # Check format
            if not re.match(
                r"^<([a-z1-6]+)([^<]+)*(?:>(.*)<\/\1>|\s+\/>)$",
                html_tag
            ):
                return False
            
            return True
        except Exception as e:
            raise SecurityError(f"Error validating HTML tag: {str(e)}")
    
    def validate_json(
        self,
        json_str: str
    ) -> bool:
        """Validate JSON.
        
        Args:
            json_str: JSON string
            
        Returns:
            True if JSON is valid, False otherwise
        
        Raises:
            SecurityError: If validation fails
        """
        try:
            # Check format
            if not re.match(r"^\{.*\}$", json_str):
                return False
            
            # Check syntax
            json.loads(json_str)
            
            return True
        except Exception as e:
            raise SecurityError(f"Error validating JSON: {str(e)}")
    
    def validate_xml(
        self,
        xml_str: str
    ) -> bool:
        """Validate XML.
        
        Args:
            xml_str: XML string
            
        Returns:
            True if XML is valid, False otherwise
        
        Raises:
            SecurityError: If validation fails
        """
        try:
            # Check format
            if not re.match(r"^<[^>]+>.*<\/[^>]+>$", xml_str):
                return False
            
            return True
        except Exception as e:
            raise SecurityError(f"Error validating XML: {str(e)}")
    
    def validate_base64(
        self,
        base64_str: str
    ) -> bool:
        """Validate Base64.
        
        Args:
            base64_str: Base64 string
            
        Returns:
            True if Base64 is valid, False otherwise
        
        Raises:
            SecurityError: If validation fails
        """
        try:
            # Check format
            if not re.match(r"^[A-Za-z0-9+/]+={0,2}$", base64_str):
                return False
            
            return True
        except Exception as e:
            raise SecurityError(f"Error validating Base64: {str(e)}")
    
    def validate_md5(
        self,
        md5_str: str
    ) -> bool:
        """Validate MD5.
        
        Args:
            md5_str: MD5 string
            
        Returns:
            True if MD5 is valid, False otherwise
        
        Raises:
            SecurityError: If validation fails
        """
        try:
            # Check format
            if not re.match(r"^[a-f0-9]{32}$", md5_str):
                return False
            
            return True
        except Exception as e:
            raise SecurityError(f"Error validating MD5: {str(e)}")
    
    def validate_sha1(
        self,
        sha1_str: str
    ) -> bool:
        """Validate SHA1.
        
        Args:
            sha1_str: SHA1 string
            
        Returns:
            True if SHA1 is valid, False otherwise
        
        Raises:
            SecurityError: If validation fails
        """
        try:
            # Check format
            if not re.match(r"^[a-f0-9]{40}$", sha1_str):
                return False
            
            return True
        except Exception as e:
            raise SecurityError(f"Error validating SHA1: {str(e)}")
    
    def validate_sha256(
        self,
        sha256_str: str
    ) -> bool:
        """Validate SHA256.
        
        Args:
            sha256_str: SHA256 string
            
        Returns:
            True if SHA256 is valid, False otherwise
        
        Raises:
            SecurityError: If validation fails
        """
        try:
            # Check format
            if not re.match(r"^[a-f0-9]{64}$", sha256_str):
                return False
            
            return True
        except Exception as e:
            raise SecurityError(f"Error validating SHA256: {str(e)}")
    
    def validate_sha512(
        self,
        sha512_str: str
    ) -> bool:
        """Validate SHA512.
        
        Args:
            sha512_str: SHA512 string
            
        Returns:
            True if SHA512 is valid, False otherwise
        
        Raises:
            SecurityError: If validation fails
        """
        try:
            # Check format
            if not re.match(r"^[a-f0-9]{128}$", sha512_str):
                return False
            
            return True
        except Exception as e:
            raise SecurityError(f"Error validating SHA512: {str(e)}") 