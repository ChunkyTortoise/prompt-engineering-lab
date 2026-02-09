"""Prompt safety checker for injection detection, PII masking, and content policy."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

_DEFAULT_INJECTION_PATTERNS: list[str] = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"disregard\s+(all\s+)?(previous|above|prior)",
    r"you\s+are\s+now",
    r"^system\s*:",
    r"act\s+as\s+(a\s+)?different",
    r"forget\s+(everything|all|your)\s+(you|instructions|rules)",
    r"new\s+instructions?\s*:",
    r"override\s+(your|the)\s+(instructions|rules|prompt)",
    r"pretend\s+(you\s+are|to\s+be)",
    r"switch\s+(to|into)\s+.*(mode|role)",
]

_BLOCKED_TERMS: list[str] = [
    "hack",
    "exploit",
    "malware",
    "ransomware",
    "phishing",
    "keylogger",
]

_PII_PATTERNS: dict[str, str] = {
    "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
    "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
}


@dataclass
class SafetyResult:
    """Result of a prompt safety check."""

    safe: bool
    violations: list[str] = field(default_factory=list)
    sanitized: str = ""
    risk_score: float = 0.0


class PromptSafetyChecker:
    """Checks prompts for injection attempts, PII, and policy violations."""

    def __init__(self, custom_patterns: list[str] | None = None) -> None:
        self._injection_patterns = [re.compile(p, re.IGNORECASE) for p in _DEFAULT_INJECTION_PATTERNS]
        if custom_patterns:
            self._injection_patterns.extend(re.compile(p, re.IGNORECASE) for p in custom_patterns)

    def check(self, text: str) -> SafetyResult:
        """Run all safety checks and return combined result."""
        violations: list[str] = []

        if self.detect_injection(text):
            violations.append("injection_attempt")

        policy_violations = self.check_content_policy(text)
        violations.extend(policy_violations)

        pii_found = bool(
            re.search(_PII_PATTERNS["email"], text)
            or re.search(_PII_PATTERNS["phone"], text)
            or re.search(_PII_PATTERNS["ssn"], text)
        )
        if pii_found:
            violations.append("pii_detected")

        risk_score = min(len(violations) * 0.3, 1.0)
        sanitized = self.sanitize(text)

        return SafetyResult(
            safe=len(violations) == 0,
            violations=violations,
            sanitized=sanitized,
            risk_score=round(risk_score, 2),
        )

    def detect_injection(self, text: str) -> bool:
        """Detect prompt injection attempts."""
        return any(p.search(text) for p in self._injection_patterns)

    def mask_pii(self, text: str) -> str:
        """Mask PII patterns (emails, phones, SSNs)."""
        result = text
        result = re.sub(_PII_PATTERNS["email"], "[EMAIL]", result)
        result = re.sub(_PII_PATTERNS["ssn"], "[SSN]", result)
        result = re.sub(_PII_PATTERNS["phone"], "[PHONE]", result)
        return result

    def check_content_policy(self, text: str) -> list[str]:
        """Check for blocked content terms."""
        violations: list[str] = []
        lower = text.lower()
        for term in _BLOCKED_TERMS:
            if term in lower:
                violations.append(f"blocked_term:{term}")
        return violations

    def sanitize(self, text: str) -> str:
        """Strip dangerous patterns and PII from text."""
        result = text
        for pattern in self._injection_patterns:
            result = pattern.sub("", result)
        result = self.mask_pii(result)
        return result.strip()
