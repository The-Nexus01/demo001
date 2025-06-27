"""
Session String Validator for Nexus v2.0
Validate and analyze Pyrogram session strings
Created by: The Nexus Team
GitHub: https://github.com/The-Nexus-Bot/Nexus-Userbot
License: MIT
"""

import base64
import logging
from typing import Dict, Any, Optional
import struct

logger = logging.getLogger(__name__)

class SessionValidator:
    """Advanced session string validator and analyzer"""
    
    @staticmethod
    def validate_format(session_string: str) -> Dict[str, Any]:
        """
        Validate session string format and extract basic information
        
        Args:
            session_string: The session string to validate
            
        Returns:
            Dict containing validation results and analysis
        """
        result = {
            "valid": False,
            "error": None,
            "info": {},
            "warnings": []
        }
        
        if not session_string:
            result["error"] = "Session string is empty"
            return result
        
        if not isinstance(session_string, str):
            result["error"] = "Session string must be a string"
            return result
        
        # Check length (Pyrogram session strings are typically 350+ characters)
        if len(session_string) < 300:
            result["error"] = "Session string too short (likely invalid)"
            return result
        
        if len(session_string) > 2000:
            result["warnings"].append("Session string unusually long")
        
        try:
            # Attempt to decode base64
            # Add padding if needed
            padding_needed = 4 - (len(session_string) % 4)
            if padding_needed != 4:
                padded_session = session_string + ("=" * padding_needed)
            else:
                padded_session = session_string
                
            decoded_data = base64.b64decode(padded_session)
            
            # Basic structure validation
            if len(decoded_data) < 350:
                result["error"] = "Decoded session data too short"
                return result
            
            # Extract basic information (this is a simplified analysis)
            result["info"] = {
                "string_length": len(session_string),
                "decoded_length": len(decoded_data),
                "estimated_type": "pyrogram_session"
            }
            
            # Try to extract DC ID (first few bytes usually contain this info)
            try:
                # This is a simplified extraction - actual Pyrogram format is more complex
                dc_id = struct.unpack('<H', decoded_data[0:2])[0]
                if 1 <= dc_id <= 5:  # Valid Telegram DC IDs
                    result["info"]["dc_id"] = dc_id
                else:
                    result["warnings"].append("Unusual DC ID detected")
            except:
                result["warnings"].append("Could not extract DC ID")
            
            result["valid"] = True
            
        except Exception as e:
            result["error"] = f"Base64 decode failed: {str(e)}"
            return result
        
        return result
    
    @staticmethod
    def quick_validate(session_string: str) -> bool:
        """
        Quick validation for session string
        
        Args:
            session_string: The session string to validate
            
        Returns:
            True if session appears valid, False otherwise
        """
        result = SessionValidator.validate_format(session_string)
        return result["valid"]
    
    @staticmethod
    def analyze_session(session_string: str) -> Dict[str, Any]:
        """
        Comprehensive analysis of session string
        
        Args:
            session_string: The session string to analyze
            
        Returns:
            Detailed analysis results
        """
        result = SessionValidator.validate_format(session_string)
        
        if not result["valid"]:
            return result
        
        # Additional analysis
        analysis = {
            "security_score": 0,
            "recommendations": [],
            "compatibility": {
                "pyrogram": True,
                "telethon": False  # This validator is Pyrogram-specific
            }
        }
        
        # Security scoring
        string_length = result["info"]["string_length"]
        
        if string_length >= 400:
            analysis["security_score"] += 30
        elif string_length >= 350:
            analysis["security_score"] += 20
        else:
            analysis["security_score"] += 10
        
        if len(result["warnings"]) == 0:
            analysis["security_score"] += 30
        else:
            analysis["security_score"] += 10
        
        # Basic entropy check (simplified)
        unique_chars = len(set(session_string))
        if unique_chars > 50:
            analysis["security_score"] += 25
        elif unique_chars > 30:
            analysis["security_score"] += 15
        else:
            analysis["security_score"] += 5
            analysis["recommendations"].append("Session string has low entropy")
        
        # Check for obvious patterns
        if session_string.count("A") > len(session_string) * 0.1:
            analysis["recommendations"].append("High repetition detected - verify session quality")
        
        # Recommendations based on score
        if analysis["security_score"] < 50:
            analysis["recommendations"].append("Consider regenerating session string")
        elif analysis["security_score"] < 75:
            analysis["recommendations"].append("Session appears functional but could be improved")
        else:
            analysis["recommendations"].append("Session string appears to be high quality")
        
        result["analysis"] = analysis
        return result
    
    @staticmethod
    def compare_sessions(session1: str, session2: str) -> Dict[str, Any]:
        """
        Compare two session strings
        
        Args:
            session1: First session string
            session2: Second session string
            
        Returns:
            Comparison results
        """
        result1 = SessionValidator.validate_format(session1)
        result2 = SessionValidator.validate_format(session2)
        
        comparison = {
            "session1_valid": result1["valid"],
            "session2_valid": result2["valid"],
            "identical": session1 == session2,
            "differences": []
        }
        
        if result1["valid"] and result2["valid"]:
            # Compare basic properties
            info1 = result1["info"]
            info2 = result2["info"]
            
            if info1["string_length"] != info2["string_length"]:
                comparison["differences"].append("Different string lengths")
            
            if info1["decoded_length"] != info2["decoded_length"]:
                comparison["differences"].append("Different decoded lengths")
            
            # Check if they might be from the same account
            if "dc_id" in info1 and "dc_id" in info2:
                if info1["dc_id"] != info2["dc_id"]:
                    comparison["differences"].append("Different data centers")
                else:
                    comparison["same_dc"] = True
        
        return comparison

def validate_session_string(session_string: str) -> bool:
    """
    Convenience function for quick session validation
    
    Args:
        session_string: Session string to validate
        
    Returns:
        True if valid, False otherwise
    """
    return SessionValidator.quick_validate(session_string)

def get_session_info(session_string: str) -> Dict[str, Any]:
    """
    Convenience function to get session information
    
    Args:
        session_string: Session string to analyze
        
    Returns:
        Session analysis results
    """
    return SessionValidator.analyze_session(session_string)
