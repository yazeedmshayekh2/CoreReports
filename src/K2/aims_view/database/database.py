import cx_Oracle
import os
import pandas as pd
import re
import logging
import hashlib
import time

from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

db_host = os.getenv('DB_SERVER_CORE')
db_service = os.getenv('DB_SERVICE_CORE')
db_user = os.getenv('DB_USER_CORE')
db_password = os.getenv('DB_PASSWORD_CORE')
db_port = os.getenv('DB_PORT_CORE')

class SecurityException(Exception):
    """Custom exception for security-related errors"""
    pass

class InputValidator:
    """Centralized input validation and sanitization"""
    
    @staticmethod
    def validate_national_id(national_id: str) -> str:
        """Validate and sanitize national ID"""
        if not national_id or not isinstance(national_id, str):
            raise SecurityException("National ID must be a non-empty string")
        
        # Remove any whitespace
        national_id = national_id.strip()
        
        # Check length (adjust based on your country's format)
        if len(national_id) != 11:
            raise SecurityException("National ID length is invalid")
        
        # Allow only alphanumeric characters (adjust regex based on your format)
        if not re.match(r'^[0-9]+$', national_id):
            raise SecurityException("National ID contains invalid characters")
        
        return national_id
    
    @staticmethod
    def validate_phone_number(phone: str) -> str:
        """Validate and sanitize phone number"""
        if not phone or not isinstance(phone, str):
            raise SecurityException("Phone number must be a non-empty string")
        
        # Remove whitespace and common separators
        phone = re.sub(r'[\s\-\(\)\+]', '', phone)
        
        # Check length
        if len(phone) < 8 or len(phone) > 10:
            raise SecurityException("Phone number length is invalid")
        
        # Allow only digits
        if not re.match(r'^[0-9]+$', phone):
            raise SecurityException("Phone number contains invalid characters")
        
        return phone
    
    @staticmethod
    def validate_customer_name(name: str) -> str:
        """Validate and sanitize customer name"""
        if not name or not isinstance(name, str):
            raise SecurityException("Customer name must be a non-empty string")
        
        # Remove leading/trailing whitespace
        name = name.strip()
        
        # Check length (increased for business names)
        if len(name) < 2 or len(name) > 120:
            raise SecurityException("Customer name length is invalid")
        
        # Allow letters, numbers, spaces, common business characters: &, (, ), ,, ., -, ', /, +, #, :, ;
        if not re.match(r"^[a-zA-Z0-9\s\-\'\.&,\(\)\/\+#:;]+$", name):
            raise SecurityException("Customer name contains invalid characters")
        
        # Prevent SQL injection patterns
        dangerous_patterns = [
            r'(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE)\b)',
            r'(--|/\*|\*/)',
            r'(\bUNION\b)',
            r'(\bOR\b.*=.*\bOR\b)',
            r'(\'.*\')',
            r'(;)'
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, name.upper()):
                raise SecurityException("Customer name contains potentially dangerous content")
        
        return name
    
    @staticmethod
    def validate_arabic_name(name: str) -> str:
        """Validate Arabic customer name with basic security checks"""
        if not name or not isinstance(name, str):
            raise SecurityException("Customer name must be a non-empty string")
        
        # Remove leading/trailing whitespace
        name = name.strip()
        
        # Check length (increased for business names)
        if len(name) < 2 or len(name) > 120:
            raise SecurityException("Customer name length is invalid")
        
        # Prevent SQL injection patterns (same as English validation)
        dangerous_patterns = [
            r'(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE)\b)',
            r'(--|/\*|\*/)',
            r'(\bUNION\b)',
            r'(\bOR\b.*=.*\bOR\b)',
            r'(\'.*\')',
            r'(;)'
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, name.upper()):
                raise SecurityException("Customer name contains potentially dangerous content")
        
        return name
    
    @staticmethod
    def validate_sql_query(sql: str, allowed_operations: list = None) -> str:
        """Validate SQL query for read_the_view method"""
        if not sql or not isinstance(sql, str):
            raise SecurityException("SQL query must be a non-empty string")
        
        # Default allowed operations (only SELECT for safety)
        if allowed_operations is None:
            allowed_operations = ['SELECT']
        
        sql = sql.strip().upper()
        
        # Check if query starts with allowed operations
        if not any(sql.startswith(op) for op in allowed_operations):
            raise SecurityException(f"SQL query must start with one of: {allowed_operations}")
        
        # Dangerous patterns to block
        dangerous_patterns = [
            r'\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE|EXEC|EXECUTE)\b',
            r'\b(GRANT|REVOKE)\b',
            r'\b(DECLARE|CURSOR)\b',
            r'(;.*SELECT|SELECT.*;)',  # Multiple statements
            r'(--|/\*)',  # SQL comments
            r'\b(xp_|sp_)\w+',  # System procedures
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, sql):
                raise SecurityException("SQL query contains prohibited operations")
        
        return sql

class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self):
        self.requests = {}
    
    def is_allowed(self, identifier: str, limit: int = 100, window: int = 3600) -> bool:
        """Check if request is allowed based on rate limiting"""
        now = time.time()
        if identifier not in self.requests:
            self.requests[identifier] = []
        
        # Clean old requests
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier] 
            if now - req_time < window
        ]
        
        # Check limit
        if len(self.requests[identifier]) >= limit:
            return False
        
        # Add current request
        self.requests[identifier].append(now)
        return True

class SecureOracleDBUtils:
    
    def __init__(self, connection_string: dict = None):
        if not connection_string:
            self.connection_string = {
                "user": db_user, 
                "password": db_password, 
                "host": db_host, 
                "port": db_port,  
                "service_name": db_service  
            }
        else:
            self.connection_string = connection_string
        
        # Initialize security components
        self.validator = InputValidator()
        self.rate_limiter = RateLimiter()
        
        # Validate connection parameters
        self._validate_connection_params()
    
    def _validate_connection_params(self):
        """Validate that all required connection parameters are present."""
        required_params = ["user", "password", "host", "port", "service_name"]
        missing_params = []
        
        for param in required_params:
            if not self.connection_string.get(param):
                missing_params.append(param)
        
        if missing_params:
            raise ValueError(f"Missing required connection parameters: {missing_params}")
    
    def _check_rate_limit(self, identifier: str) -> None:
        """Check rate limiting for requests"""
        if not self.rate_limiter.is_allowed(identifier):
            logger.warning(f"Rate limit exceeded for identifier: {hashlib.sha256(identifier.encode()).hexdigest()[:8]}")
            raise SecurityException("Rate limit exceeded. Please try again later.")
    
    def get_connection_string(self):
        """Return a copy without the password for security"""
        conn_copy = self.connection_string.copy()
        conn_copy["password"] = "***"
        return conn_copy
    
    def connect_to_database(self, debug_mode: bool = False):
        """Create database connection with security enhancements and Unicode support"""
        try:
            dsn = cx_Oracle.makedsn(
                self.connection_string["host"],
                int(self.connection_string["port"]),
                service_name=self.connection_string["service_name"]
            )
            
            connection = cx_Oracle.connect(
                user=self.connection_string["user"],
                password=self.connection_string["password"],
                dsn=dsn,
                encoding="UTF-8",
                nencoding="UTF-8"
            )
            
            # Try to set session parameters for Unicode and Arabic support
            try:
                cursor = connection.cursor()
                # Set character set parameters to support Unicode/Arabic
                cursor.execute("ALTER SESSION SET NLS_LANGUAGE = 'AMERICAN'")
                cursor.execute("ALTER SESSION SET NLS_TERRITORY = 'AMERICA'")
                cursor.execute("ALTER SESSION SET NLS_CHARACTERSET = 'AL32UTF8'")
                cursor.close()
            except cx_Oracle.Error as session_error:
                # Log warning but don't fail the connection
                if debug_mode:
                    logger.warning(f"Could not set Unicode session parameters: {session_error}")
                pass
            
            return connection
            
        except cx_Oracle.Error as e:
            # Enhanced error logging for debugging
            full_error = str(e)
            error_code = full_error.split(':')[0] if ':' in full_error else 'Unknown'
            
            if debug_mode:
                logger.error(f"Database connection failed. Full error: {full_error}")
                logger.error(f"Connection parameters: host={self.connection_string['host']}, "
                           f"port={self.connection_string['port']}, "
                           f"service={self.connection_string['service_name']}, "
                           f"user={self.connection_string['user']}")
            else:
                logger.error(f"Database connection failed with error code: {error_code}")
            
            # Don't mask the error in debug mode
            if debug_mode:
                raise e
            else:
                raise SecurityException("Database connection failed. Please contact administrator.")
        except Exception as e:
            logger.error(f"Unexpected error during database connection: {type(e).__name__}")
            if debug_mode:
                raise e
            else:
                raise SecurityException("Database connection failed due to unexpected error.")
    
    def _safe_execute_query(self, sql: str, params: dict = None) -> pd.DataFrame:
        """Safely execute a query with proper error handling and Unicode support"""
        connection = None
        cursor = None
        try:
            connection = self.connect_to_database(debug_mode=False)
            cursor = connection.cursor()
            
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
                
            columns = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()
            df = pd.DataFrame(data, columns=columns)
            
            return df
            
        except cx_Oracle.Error as e:
            error_code = str(e).split(':')[0] if ':' in str(e) else 'Unknown'
            logger.error(f"Query execution failed with error code: {error_code}")
            raise SecurityException("Query execution failed. Please contact administrator.")
        except UnicodeError as e:
            logger.error(f"Unicode encoding error during query execution: {e}")
            raise SecurityException("Query failed due to character encoding issues. Please check the text format.")
        except Exception as e:
            logger.error(f"Unexpected error during query execution: {type(e).__name__}")
            raise SecurityException("Query execution failed due to unexpected error.")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    def test_connection(self, debug_mode: bool = False) -> bool:
        """Test the database connection with optional debug information."""
        try:
            connection = self.connect_to_database(debug_mode=debug_mode)
            cursor = connection.cursor()
            cursor.execute("SELECT 1 FROM DUAL")
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            logger.info("Database connection test successful")
            return True
        except cx_Oracle.Error as e:
            if debug_mode:
                logger.error(f"Database connection test failed with Oracle error: {e}")
            else:
                logger.error("Database connection test failed due to security error")
            return False
        except SecurityException:
            logger.error("Database connection test failed due to security error")
            return False
        except Exception as e:
            if debug_mode:
                logger.error(f"Database connection test failed with unexpected error: {e}")
            else:
                logger.error(f"Database connection test failed: {type(e).__name__}")
            return False
        
class DomainKnowledge(SecureOracleDBUtils):
    """Domain knowledge for the AIMS database"""
    
    def __init__(self):
        super().__init__()
    
    def dynamic_branches(self):
        """Get the dynamic branches for the AIMS database"""
        query = """
        SELECT DISTINCT DOC_BRANCH, DOC_BRANCH_NAME FROM insmv.AIMS_ALL_DATA
        """
        df = self._safe_execute_query(query)
        zip_df = zip(df['DOC_BRANCH'], df['DOC_BRANCH_NAME'])
        list_zip_df = list(zip_df)
        knowledge = {
            "dynamic_branches": list_zip_df
        }
        return knowledge